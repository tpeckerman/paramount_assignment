#!/usr/bin/env python3
"""Assemble the RUN 2 context for a decision: prompt + the rule slice that applies.

This is the "compile once, query many" payoff. RUN 2 never reads a regulatory source
document. It reads rows from rules/csv/Rules.csv, which were compiled from those documents
once and are quote-checked against them. Three things follow:

  1. The decision context is small enough to be reliable. Feeding whole codes to a model
     and asking for a rating puts the extraction and the application in one step, where a
     wrong reading is invisible because nothing separates "what the rule says" from
     "what I decided".
  2. Updating a rule is a row edit with a provenance trail, not a re-read of everything.
  3. Every decision cites a rule_id that resolves to a row, a clause and a verbatim quote.

Usage:
    python3 run_decision.py --countries UK FR --service free_to_air --categories violence
    python3 run_decision.py --stage1 tests/case01.stage1.json --countries UK FR
    python3 run_decision.py --countries UK --measure
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import constants as C

ROOT = C.ROOT
RULES = C.RULES_CSV
DECIDE_PROMPT = C.DECISION_PROMPT

# Columns RUN 2 is given. Deliberately not every column: last_checked, extraction_confidence
# and quote_lang are provenance for humans and auditors, not inputs to a decision. Sending
# them invites the model to reason about its own confidence instead of about the rule.
DECISION_COLS = [
    "rule_id", "country", "regulator", "authority_rank", "service_type",
    "content_category", "classification", "threshold_description",
    "time_restriction_text", "time_rule_machine", "exceptions_conditions",
    "determinacy", "human_review_required", "clause_ref", "verbatim_quote",
]

# Categories that must travel with every request regardless of what RUN 1 saw. These carry
# the scheme itself, the scheduling frame and the definitions. Filtering them out produces a
# model that knows a title has violence in it but not what a watershed is.
ALWAYS_INCLUDE = {
    "scheduling_general", "definition", "classification_scheme", "legal_basis",
    "scope", "signage", "film_carryover",
    # Added after test case TC-02 failed. These categories describe HOW a programme may be
    # delivered, not what is in it, so no content description ever mentions them - which meant
    # the category filter dropped them every single time. UK-ACC-001, the rule that DEFINES
    # mandatory restricted access, never reached the decision engine, while the rules granting
    # an any-hour permission *conditional on that access* did. The engine could therefore read
    # "any_time; requires=mandatory_daytime_protection" with no row explaining what the
    # requirement means or how to tell whether it is satisfied.
    #
    # The general lesson, which matters more than the fix: filtering rules by the categories
    # present in the CONTENT silently removes every rule about DELIVERY. Any future country's
    # access, signage, warning and trailer rules must be force-included for the same reason.
    "access_control", "audience_information", "trailers",
    # Absolute prohibitions. These were being filtered by content_category like ordinary
    # rules, so the extreme-violence ban only arrived if the description happened to be
    # tagged `violence`, and the R18 ban only if tagged `sexual_content`. They are the rules
    # no contextual argument may override, so they cannot be gated on retrieval: a decision
    # that never saw them cannot have applied them.
    "human_dignity", "serious_harm",
}

# Always in the slice regardless of category or service. Over-retrieval here is safe - the
# engine reads each rule's threshold and will see that a ban on pornography depicting minors
# does not bite on an adult drama. Under-retrieval is not safe, because a rule absent from
# the slice is indistinguishable from a rule that did not apply.
ALWAYS_RULE_IDS = {
    "UK-GEN-001", "UK-SEX-001", "UK-FLM-001", "UK-FLM-006",
    "FR-LAW-001", "FR-PRO-001", "FR-PRO-002", "FR-PRO-003",
}


def load_rules() -> list[dict]:
    if not RULES.exists():
        sys.exit(f"missing {RULES} - run pipeline/build_rules_table.py first")
    with RULES.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def service_matches(rule_scope: str, requested: str | None) -> bool:
    """A rule binds if its scope names the requested service, or is service-agnostic.

    When the service is unknown we return True for everything: RUN 2 is instructed to
    branch and label, and withholding rows here would silently narrow the branches it can
    see. Dropping a rule because we cannot confirm it applies is how a pipeline produces a
    confident answer that omits the rule that mattered.
    """
    if requested in (None, "", "not_stated"):
        return True
    tokens = {t.strip() for t in rule_scope.split(";") if t.strip()}
    if {"all_linear_tv", "all_avms", "all_linear_tv_default"} & tokens:
        return True
    return requested in tokens


def select(rules, countries, service=None, categories=None):
    out, dropped = [], []
    wanted = set(categories or []) | ALWAYS_INCLUDE if categories else None
    for r in rules:
        if r["status"] != C.USABLE_STATUS:
            dropped.append((r["rule_id"], f"status={r['status']}"))
            continue
        if r["country"] not in countries:
            continue
        if not service_matches(r["service_type"], service):
            dropped.append((r["rule_id"], f"service_type={r['service_type']}"))
            continue
        if (wanted and r["content_category"] not in wanted
                and r["rule_id"] not in ALWAYS_RULE_IDS):
            dropped.append((r["rule_id"], f"category={r['content_category']}"))
            continue
        out.append(r)
    # Lower authority_rank first: RUN 2 resolves conflicts by rank, so presenting the rows
    # in rank order means the binding instrument is read before the guidance about it.
    out.sort(key=lambda r: (r["country"], int(r["authority_rank"] or 9), r["rule_id"]))
    return out, dropped


def build(selected: list[dict]) -> str:
    rows = [{c: r.get(c, "") for c in DECISION_COLS} for r in selected]
    return json.dumps(rows, ensure_ascii=False, indent=1)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--countries", nargs="+", default=["UK", "FR"])
    p.add_argument("--service", default=None)
    p.add_argument("--categories", nargs="*", default=None)
    p.add_argument("--stage1", type=pathlib.Path,
                   help="RUN 1 JSON; categories are taken from its observations")
    p.add_argument("--measure", action="store_true",
                   help="report the size of the rule slice against the source corpus")
    p.add_argument("-o", "--out", type=pathlib.Path)
    a = p.parse_args()

    rules = load_rules()
    cats = a.categories
    obs_block = ""
    if a.stage1:
        s1 = json.loads(a.stage1.read_text(encoding="utf-8"))
        cats = sorted({o["category"] for o in s1.get("observations", [])})
        obs_block = json.dumps(s1, ensure_ascii=False, indent=1)
        print(f"categories from {a.stage1.name}: {cats or '(none)'}", file=sys.stderr)

    sel, dropped = select(rules, set(a.countries), a.service, cats)
    slice_json = build(sel)

    print(f"selected {len(sel)} of {len(rules)} rules "
          f"({len(dropped)} filtered out)", file=sys.stderr)
    for c in a.countries:
        n = sum(1 for r in sel if r["country"] == c)
        hr = sum(1 for r in sel if r["country"] == c and r["human_review_required"] == "yes")
        jb = sum(1 for r in sel if r["country"] == c and r["determinacy"] == C.JUDGMENT_DETERMINACY)
        print(f"  {c}: {n} rules, {jb} judgment_based, {hr} needing human review",
              file=sys.stderr)
    if not sel:
        print("  WARNING: empty slice. RUN 2 is instructed to stop rather than fall back "
              "on general knowledge.", file=sys.stderr)

    if a.measure:
        corpus = sum(f.stat().st_size for f in (ROOT / "sources/originals").glob("*.txt"))
        corpus += sum(f.stat().st_size for f in (ROOT / "sources/originals").glob("*.pdf"))
        print(f"\n  rule slice     : {len(slice_json):>9,} bytes", file=sys.stderr)
        print(f"  source corpus  : {corpus:>9,} bytes (downloaded so far, "
              f"of 20 documents)", file=sys.stderr)
        if corpus:
            print(f"  ratio          : {corpus / len(slice_json):>9.1f}x smaller, and the "
                  f"corpus is still incomplete", file=sys.stderr)

    doc = DECIDE_PROMPT.read_text(encoding="utf-8")
    # Emit the delimiters RUN_2 declares. The prompt tells the model that everything inside
    # <observations> is data rather than instructions; that promise is only real if the
    # assembler actually wraps the content.
    parts = [doc, "\n\n---\n\n<rules>\n" + slice_json + "\n</rules>\n"]
    if obs_block:
        parts.append("\n<observations>\n" + obs_block + "\n</observations>\n")
    parts.append("\n<request>\n" + json.dumps({
        "countries": a.countries,
        "service_type": a.service or "not_stated",
        "intended_slot": "not_stated",
        "intended_date": "not_stated",  # RUN_2 checks the calendar, not only the clock
    }, indent=1) + "\n</request>\n")
    assembled = "".join(parts)

    if a.out:
        a.out.write_text(assembled, encoding="utf-8")
        print(f"wrote {a.out} ({len(assembled):,} bytes)", file=sys.stderr)
    else:
        sys.stdout.write(assembled)


if __name__ == "__main__":
    raise SystemExit(main())
