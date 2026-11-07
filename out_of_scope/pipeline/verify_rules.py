#!/usr/bin/env python3
"""Integrity checks on the rule table. Run this before trusting it as ground truth.

    python out_of_scope/pipeline/verify_rules.py
    python out_of_scope/pipeline/verify_rules.py --with-quotes   # also check every verbatim_quote
                                                   # against the downloaded originals

Exit code 0 = clean, 1 = problems found. Safe to run in CI.

The check that actually matters is --with-quotes: every extracted rule must carry a
verbatim quote that provably occurs in its stored source document. Without it,
extraction errors are silent, and a wrong row becomes ground truth. It needs
sources/originals/ populated first:

    python out_of_scope/pipeline/fetch_originals.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import constants as C

try:
    import openpyxl
except ImportError:
    sys.exit("needs openpyxl:  pip install openpyxl")

ROOT = C.ROOT
WORKBOOK = C.RULES_XLSX
ORIGINALS = C.ORIGINALS_DIR
MANIFEST = C.MANIFEST_CSV

RULE_ID = C.RULE_ID_PATTERN

TIME_TOKEN = re.compile(
    r"^("
    r"none|prohibited|any_time|n/a"
    r"|not_before=\d{2}:\d{2}"
    r"|window=\d{2}:\d{2}-\d{2}:\d{2}"
    r"|restricted_window=\d{2}:\d{2}-\d{2}:\d{2}"
    r"|soft_prefer_not_before=\d{2}:\d{2}"
    r"|not_within=.+|not_near=.+|not_when=.+|prohibited_in=.+"
    r"|days=.+|except_days=.+|unless=.+|requires=.+|gate=.+|override=.+"
    r"|annual_quota=.+|sub_quota=.+|standard=.+|frequency_cap=.+|exempt=.+"
    r"|see=.+|judgment:.+|framework:.+|precedent=.+"
    r")$")

ENUMS = {
    "country": {"UK", "FR", "EU"},
    "determinacy": set(C.DETERMINACY),
    "ambiguity_flag": {"clear", "conflicting_sources", "translation_uncertain",
                       "unverified", "out_of_scope_for_asset_decision"},
    "human_review_required": {"yes", "no"},
    "use_for_decision": {"yes", "definition_only", "framework_only", "pointer",
                         "scope_rule", "no_out_of_scope"},
    "extraction_confidence": {"high", "medium", "low"},
    "quote_lang": {"EN", "FR", ""},
}

REQUIRED_NON_EMPTY = ("rule_id", "country", "regulator", "source_type", "authority_rank",
                      "use_for_decision", "service_type", "content_category",
                      "threshold_description", "determinacy", "ambiguity_flag",
                      "source_doc", "clause_ref", "source_url")


def load_rules() -> list[dict]:
    ws = openpyxl.load_workbook(WORKBOOK, data_only=True)["Rules"]
    header = [c.value for c in ws[1]]
    rows = []
    for r in ws.iter_rows(min_row=2):
        vals = [c.value for c in r]
        if all(v is None for v in vals):
            continue
        rows.append({k: ("" if v is None else str(v)) for k, v in zip(header, vals)})
    return rows


def check(rows: list[dict]) -> list[str]:
    bad: list[str] = []
    ids = [r["rule_id"] for r in rows]

    for i in {x for x in ids if ids.count(x) > 1}:
        bad.append(f"duplicate rule_id: {i}")
    for i in ids:
        if not RULE_ID.match(i):
            bad.append(f"malformed rule_id: {i!r} (expect (UK|FR|EU)-[A-Z]{{2,4}}-nnn)")

    for r in rows:
        rid = r["rule_id"]

        for col in REQUIRED_NON_EMPTY:
            if not r.get(col, "").strip():
                bad.append(f"{rid}: {col} is empty")

        for col, allowed in ENUMS.items():
            v = r.get(col, "")
            if v and v not in allowed:
                bad.append(f"{rid}: {col}={v!r} not in {sorted(allowed)}")

        if not r["source_url"].startswith("https://"):
            bad.append(f"{rid}: source_url is not https: {r['source_url'][:60]!r}")

        if r["authority_rank"] not in {str(n) for n in range(1, 8)}:
            bad.append(f"{rid}: authority_rank={r['authority_rank']!r} not 1-7")

        # a live row cannot have an extraction that is still in doubt
        if C.is_live(r) and r["ambiguity_flag"] in {
                "translation_uncertain", "unverified", "conflicting_sources"}:
            bad.append(f"{rid}: live but ambiguity_flag="
                       f"{r['ambiguity_flag']} - resolve or close")

        # anything needing review must say why
        if r["human_review_required"] == "yes" and not r["ambiguity_note"].strip():
            bad.append(f"{rid}: human_review_required=yes but ambiguity_note is empty")

        # flagged rows must carry a note
        if r["ambiguity_flag"] != "clear" and not r["ambiguity_note"].strip():
            bad.append(f"{rid}: ambiguity_flag={r['ambiguity_flag']} but no note")

        for part in (p.strip() for p in r["time_rule_machine"].split(";")):
            if part and not TIME_TOKEN.match(part):
                bad.append(f"{rid}: unparseable time_rule_machine token {part!r}")
            if part.startswith("see=") and part[4:] not in ids:
                bad.append(f"{rid}: see= points at missing rule {part[4:]!r}")

        # an absolute prohibition must not also carry a permissive time window
        if r["time_rule_machine"].strip() == "prohibited" and r["classification"] not in {
                "prohibited", "V_-18", "n/a"}:
            bad.append(f"{rid}: time_rule_machine=prohibited but "
                       f"classification={r['classification']!r}")

    return bad


def check_manifest_coverage(rows: list[dict]) -> list[str]:
    if not MANIFEST.exists():
        return [f"missing {MANIFEST.relative_to(ROOT)}"]
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        manifest = {r["doc_id"] for r in csv.DictReader(fh)}

    bad = []
    for r in rows:
        # source_doc may be compound, e.g. "FR-R1 (as amd. FR-A2)" or "UK-S1 + UK-M1"
        refs = C.RULE_ID_IN_TEXT.findall(r["source_doc"])
        if not refs:
            bad.append(f"{r['rule_id']}: source_doc {r['source_doc']!r} names no doc_id")
        for ref in refs:
            if ref not in manifest:
                bad.append(f"{r['rule_id']}: source_doc references {ref!r}, "
                           "which is not in sources/originals/MANIFEST.csv")
    return bad


def check_quotes(rows: list[dict]) -> list[str]:
    """THE key control. Every verbatim_quote must occur in its stored source document."""
    if not MANIFEST.exists():
        return [f"missing {MANIFEST.relative_to(ROOT)}"]
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        man = list(csv.DictReader(fh))
    files = {r["doc_id"]: ORIGINALS / r["target_filename"] for r in man}
    # A row's source_url is the authoritative pointer to the text that actually
    # holds its quote, and after the provenance fix that URL is often the
    # consolidated edition (FR-R1c/FR-R1d) rather than the doc named in
    # source_doc. Resolve by URL as well, or every French quote is skipped.
    by_url = {r["url"]: r["doc_id"] for r in man}

    def fold(t: str) -> str:
        """Compare accent- and case-insensitively.

        The table stores quotes ASCII-folded so the CSV mirrors stay pure ASCII and
        diff cleanly, but the sources are accented French. Without folding both
        sides, every French quote fails spuriously - which is exactly what the first
        run of this check reported.
        """
        for a, b in (("\u0153", "oe"), ("\u0152", "OE"), ("\u00e6", "ae"),
                     ("\u00c6", "AE"), ("\u2014", "-"), ("\u2013", "-"),
                     ("\u2019", "'"), ("\u2018", "'"), ("\u00a0", " ")):
            t = t.replace(a, b)
        t = unicodedata.normalize("NFKD", t)
        t = "".join(c for c in t if not unicodedata.combining(c))
        return re.sub(r"\s+", " ", t).casefold()

    cache: dict[str, str | None] = {}

    def text_of(doc_id: str) -> str | None:
        if doc_id in cache:
            return cache[doc_id]
        path = files.get(doc_id)
        if path is None or not path.exists():
            cache[doc_id] = None
            return None
        raw = path.read_bytes()
        if path.suffix == ".pdf":
            try:
                import pypdf
                import io
                txt = "\n".join(
                    (p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(raw)).pages)
            except ImportError:
                cache[doc_id] = None
                print("  (pip install pypdf to check quotes inside PDFs)", file=sys.stderr)
                return None
        else:
            txt = raw.decode("utf-8", "replace")
            txt = re.sub(r"<[^>]+>", " ", txt)          # crude de-tag
        txt = fold(re.sub(r"\s+", " ", txt))
        cache[doc_id] = txt
        return txt

    bad, checked, skipped = [], 0, 0
    inconclusive: list[str] = []
    for r in rows:
        q = r["verbatim_quote"].strip()
        if not q:
            continue
        refs = C.RULE_ID_IN_TEXT.findall(r["source_doc"])
        if r["source_url"] in by_url:
            refs.append(by_url[r["source_url"]])
        refs = [d for i, d in enumerate(refs) if d in files and d not in refs[:i]]
        hays = [(d, t) for d, t in ((d, text_of(d)) for d in refs) if t]
        if not hays:
            skipped += 1
            continue
        complete = len(hays) == len(refs)
        # A quote may legitimately live in any one of a row's cited sources, so a
        # hit in ANY of them passes. Quotes use "..." where text was elided.
        frags = [f.strip() for f in q.split("...") if len(f.strip()) >= 12]
        if not frags:
            continue
        found = any(all(fold(re.sub(r"\s+", " ", fr)) in hay for fr in frags)
                    for _, hay in hays)
        if found:
            checked += 1
        elif complete:
            # every cited source is on disk and none contains the quote -> defect
            bad.append(f"{r['rule_id']}: quote not found in "
                       f"{[d for d, _ in hays]}: {frags[0][:70]!r}")
            checked += 1
        else:
            # a cited source is missing, so absence here proves nothing
            missing = [d for d in refs if d not in {x for x, _ in hays}]
            inconclusive.append(f"{r['rule_id']}: not in {[d for d, _ in hays]}, "
                                f"but {missing} not downloaded")
    # Report the DENOMINATOR. This line used to count only the rules that happened to carry
    # a quote, so it read as full coverage while half the table had never been checked.
    _approved = [r for r in rows if C.is_live(r)]
    _noq = [r["rule_id"] for r in _approved if not r["verbatim_quote"].strip()]
    print(f"  quote check: {checked - len(bad)} VERIFIED against the stored source, "
          f"{len(bad)} FAILED, {len(inconclusive)} inconclusive, "
          f"{skipped} skipped (no source on disk)")
    print(f"  COVERAGE:    {len(_approved) - len(_noq)} of {len(_approved)} approved rules "
          f"carry a quote; {len(_noq)} carry NONE and are never checked.")
    _abs = [r for r in _noq if r in ABSOLUTE]
    if _abs:
        print(f"  WARNING:     {len(_abs)} unquoted rules are ABSOLUTE PROHIBITIONS, the "
              f"rules no argument may override: {' '.join(_abs)}")
    # Coverage reached 102/102 on 2026-11-07. It is now a RATCHET: an approved rule with no
    # quote fails the build. The gap existed for weeks precisely because nothing failed - the
    # unquoted rules were not passing the check, they were never being shown to it.
    if _noq:
        bad.extend(f"{rid}: approved with NO verbatim_quote, so it is never checked"
                   for rid in _noq)
    for line in inconclusive:
        print(f"    inconclusive: {line}")
    if skipped and not checked:
        print("  -> run  python out_of_scope/pipeline/fetch_originals.py  first "
              "(see conflict C-04 in sources/99_EXTRACTION_NOTES_AND_LIMITS.md)")
    return bad


# Controlled vocabulary for service_type. Added after test TC-02 found that two spellings of
# the same service ("premium_subscription" vs "premium_subscription_film") caused the rule
# DEFINING mandatory restricted access to be silently dropped from every decision slice that
# asked for the other spelling. Nothing failed - the slice was simply missing a rule, which is
# the worst kind of defect because the output still looks complete.
SERVICE_VOCAB = {
    "all_linear_tv", "all_avms", "bbc_odps", "free_to_air", "premium_subscription_film",
    "pay_per_view", "cinema_channels", "other_than_cinema_channels", "music_channels",
    "scheduled_channels_with_mdp", "high_production_commitment_channels", "pay_tv_bundles",
    "per_channel",
}


def clock_times(s: str) -> set[str]:
    """Every clock time in a string, in any spelling the sources use."""
    out: set[str] = set()
    s = s or ""
    for m in re.finditer(r"(\d{1,2})\s*h\s*(\d{2})?", s):          # 22 h 30, 22h
        out.add(f"{int(m.group(1)):02d}:{m.group(2) or '00'}")
    for m in re.finditer(r"\b(\d{1,2}):(\d{2})\b", s):             # 21:00
        out.add(f"{int(m.group(1)):02d}:{m.group(2)}")
    for m in re.finditer(r"\b([01]\d|2[0-3])([0-5]\d)\b", s):      # 2100, 0530
        out.add(f"{m.group(1)}:{m.group(2)}")
    return out


def check_times_against_quotes(rows: list[dict]) -> tuple[list[str], int, int]:
    """Do the HOURS in a row actually appear in the quote that is meant to prove them?

    This closes the hole that made the quote check weaker than it read. Verifying that a
    quote exists in the source proves the quote is real. It proves nothing about the row
    around it, and the row is what the decision engine uses. A reviewer demonstrated this by
    changing a watershed from 21:00 to 19:00, leaving the quote untouched, and watching
    `--with-quotes` pass. It did, because nothing compared the two.

    Running it for the first time found a real defect: UK-SCH-003 sets a 20:00 watershed for
    unprotected premium film services and quoted the sentence saying 2100. The rule was
    right and its evidence was the wrong sentence.

    Scope, stated because the denominator is the point: this can only check rows where BOTH
    the quote and the machine field contain a time. That is a minority of the table, and a
    row whose quote carries no time is not verified by this, merely unexamined.
    """
    bad, checkable = [], 0
    for r in rows:
        want = clock_times(r["time_rule_machine"])
        have = clock_times(r["verbatim_quote"])
        if not want or not have:
            continue
        checkable += 1
        # A row may legitimately carry a bound that its own sentence does not state, where
        # the bound comes from a general rule in the same instrument. UK-SCH-003 is the
        # case: the source gives premium film services a 2000 watershed and says nothing
        # about when it ends, because the end is the general 0530. That is allowed, but it
        # has to be DECLARED in the row rather than assumed by the checker, so the exemption
        # is visible to a reader of the table and not buried in this file.
        have |= clock_times(
            " ".join(re.findall(r"inherits_time=(\S+)", r["exceptions_conditions"] or "")))
        missing = sorted(want - have)
        if missing:
            bad.append(f"{r['rule_id']}: time_rule_machine claims {sorted(want)} but its "
                       f"quote only supports {sorted(have)}. Unsupported: {missing}. "
                       f"Either the hours are wrong or the quote is the wrong sentence.")
    return bad, checkable, len(rows)


def check_precheck_agrees(rows: list[dict]) -> list[str]:
    """precheck.py names prohibitions that need a judgement. The table must agree.

    These two files encoded the same fact independently and drifted: precheck listed
    FR-PRO-001 and FR-PRO-003 as judgements, and the table called them bright lines. Neither
    was wrong on its own terms, which is why nothing caught it, and the table's version
    inflated the count of rules that can be applied mechanically.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_precheck", Path(__file__).resolve().parent / "precheck.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    by_id = {r["rule_id"]: r for r in rows}
    bad = []
    for rid in getattr(mod, "PROHIBITIONS_NEEDING_CONTENT", {}):
        row = by_id.get(rid)
        if row is None:
            bad.append(f"{rid}: the gate names it, the table does not have it")
        elif "prohibited" not in (row["time_rule_machine"] or "").lower():
            bad.append(f"{rid}: the gate treats it as an absolute prohibition, the table "
                       f"says time_rule_machine={row['time_rule_machine']!r}. One is wrong.")
    return bad


EXCEPTION_WORDS = ("unless", "except", "save ", "other than", "provided", "sauf", "hormis",
                   "réserve", "justified", "justifié", "derogat", "dérogat", "where ")


def check_exception_evidence(rows: list[dict]) -> tuple[list[str], int, int]:
    """Does a rule's QUOTE support the exception its machine field claims?

    Reported, not failed, and the distinction is deliberate. An exception often lives in a
    different sentence from the one that states the rule, so a missing exception word in the
    quote is not proof of error. It is proof that **nothing has checked it**, which is a
    different and still important thing.

    The hours check closed one half of this hole: a row's times are now compared against its
    quote. This is the other half, and it is wider. An external reviewer found it by reading
    the table, which is the only way it could have been found, because no check looked.
    """
    flagged, checkable = [], 0
    for r in rows:
        machine = (r["time_rule_machine"] or "").lower()
        if not re.search(r"unless=|requires=|except", machine):
            continue
        checkable += 1
        quote = (r["verbatim_quote"] or "").lower()
        if not any(w in quote for w in EXCEPTION_WORDS):
            flagged.append(r["rule_id"])
    return flagged, checkable, len(rows)


def check_service_vocab(rows):
    bad = []
    for r in rows:
        for tok in (x.strip() for x in r["service_type"].split(";")):
            if tok and tok not in SERVICE_VOCAB:
                bad.append((r["rule_id"], tok))
    return bad

def check_sources_tab(rows):
    """Every collected document must appear in the Sources tab.

    The tab also lists sources considered and rejected, which is useful context, so this is
    one-directional. It exists because the two lists drifted: the tab carried nine documents
    that had been removed from the manifest and was missing four that had been added.

    READS THE WORKBOOK, NOT A CSV MIRROR. It used to read rules/csv/Sources.csv, and only
    two of the six tabs are ever mirrored to CSV, so that file has never existed. The check
    opened with `if not src.exists(): return []` and therefore passed silently every single
    run, from the commit that added it onward. The drift it was written to catch could have
    come straight back without anything going red.
    """
    import csv as _csv
    man = C.MANIFEST_CSV
    if not man.exists():
        return []
    wb = openpyxl.load_workbook(WORKBOOK, read_only=True, data_only=True)
    if "Sources" not in wb.sheetnames:
        return ["the workbook has no Sources tab"]
    ws = wb["Sources"]
    head = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    col = head.index("source_id")
    have = {r[col].value for r in ws.iter_rows(min_row=2) if r[col].value}
    need = {r["doc_id"] for r in _csv.DictReader(man.open(encoding="utf-8"))}
    return sorted(need - have)

def check_inert_rules_do_not_demand_review(rows):
    """A rule that cannot change an answer must not demand a person decide it.

    The deciding prompt reserves `basis` for rules that set or move the hours, fix the
    classification, or impose a condition. A row whose time_rule_machine is "n/a" with no
    `requires=` clause does none of those: it is a definition or a lens, and it can only
    ever colour how some OTHER rule is read. That other rule carries its own review flag.

    Marking the lens itself human_review_required=yes double-counts, and when the lens
    applies to every decision the whole system escalates by construction. UK-CTX-010 (audience
    size, a definition) was flagged yes and turned up in 9 of 17 escalation reasons while
    being incapable of changing any of them.

    NARROWED ONCE ALREADY. The first version asked only whether time_rule_machine was "n/a",
    which conflates "sets no HOUR" with "restricts nothing". It flagged FR-CV-005 and
    FR-CV-006, a quota cap and a set of marketing conditions: both are real operative
    restrictions that happen not to be about the clock, and both rightly need a person. What
    actually distinguishes an inert row is that it is a DEFINITION, which defines a term
    rather than restricting anything.
    """
    bad = []
    for r in rows:
        tok = (r["time_rule_machine"] or "").strip()
        inert = (r["content_category"] == "definition"
                 and tok.startswith("n/a") and "requires=" not in tok)
        if inert and r["human_review_required"] == "yes":
            bad.append(f"{r['rule_id']}: time_rule_machine={tok!r} cannot change an answer, "
                       f"so it must not carry human_review_required='yes'. The operative rule "
                       f"it informs is what needs the review.")
    return bad


ABSOLUTE = {"UK-GEN-001", "UK-SEX-001", "UK-FLM-001", "UK-FLM-006",
            "FR-LAW-001", "FR-PRO-001", "FR-PRO-002", "FR-PRO-003", "FR-CV-003"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--with-quotes", action="store_true",
                    help="also check verbatim_quote against sources/originals/")
    args = ap.parse_args()

    if not WORKBOOK.exists():
        sys.exit(f"missing {WORKBOOK.relative_to(ROOT)}")

    rows = load_rules()
    print(f"loaded {len(rows)} rules from {WORKBOOK.relative_to(ROOT)}")

    problems = check(rows) + check_manifest_coverage(rows)
    problems += check_inert_rules_do_not_demand_review(rows)
    problems += [f"{d}: collected but missing from the Sources tab"
                 for d in check_sources_tab(rows)]
    problems += [f"{rid}: service_type '{tok}' is not in the controlled vocabulary"
                 for rid, tok in check_service_vocab(rows)]

    # Always on, not gated behind --with-quotes: this compares two fields of the same row
    # and needs no source document, so there is no reason for it ever to be skipped.
    time_bad, time_checkable, time_total = check_times_against_quotes(rows)
    problems += time_bad
    problems += check_precheck_agrees(rows)

    exc_flagged, exc_checkable, _ = check_exception_evidence(rows)

    if args.with_quotes:
        problems += check_quotes(rows)

    from collections import Counter
    print("  by country   :", dict(Counter(r["country"] for r in rows)))
    print("  by determinacy:", dict(Counter(r["determinacy"] for r in rows)))
    print("  needs review :", sum(1 for r in rows if r["human_review_required"] == "yes"))
    print(f"  EXCEPTIONS:  {len(exc_flagged)} of {exc_checkable} rules that claim an exception "
          f"or condition have a quote that does not contain one. NOT a failure, because an "
          f"exception often sits in a different sentence, but nothing has checked them "
          f"(C-18).")
    print(f"  HOURS vs QUOTE: {time_checkable} of {time_total} rules have a time in both "
          f"the machine field and the quote, so only those were compared. The other "
          f"{time_total - time_checkable} are NOT verified on this axis, merely unexamined.")
    print("  LIVE RULES:", sum(1 for r in rows if C.is_live(r)))

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1

    print("\nAll checks passed.")
    if not args.with_quotes:
        print("NOTE: quote integrity NOT checked. Run with --with-quotes once "
              "sources/originals/ is populated - that is the check that catches "
              "silent extraction errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
