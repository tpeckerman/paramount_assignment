#!/usr/bin/env python3
"""Check that the outcomes claimed in tests/CASES.md are really in the stored sources.

A back-test is only worth anything if the "known outcome" is actually known. TC-01 claims a
regulator reached a particular decision, and that claim carries the whole case: if it is
wrong, the test measures nothing and looks like the strongest evidence in the repo.

So the claim is treated the same way as a rule. Quote the source, store the source, and check
the quote mechanically. This is the same check `verify_rules.py --with-quotes` runs over the
rules table, pointed at the test cases instead.

usage: python out_of_scope/pipeline/verify_cases.py
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C


# (case, source file on disk, phrases that must appear in it verbatim)
CLAIMS = [
    ("TC-01", "out_of_scope/sources/originals/UK-P1_ofcom_decision_toofan.pdf", [
        "Breach of Rule 1.3 of the Code.",
        "did not pursue the investigation further under Rule 2.3",
        "sufficiently contextualised within the film",
    ]),
]


def text_of(path: pathlib.Path) -> str:
    if path.suffix.lower() == ".pdf":
        import pypdf
        raw = "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(str(path)).pages)
    else:
        raw = path.read_text(encoding="utf-8", errors="replace")
    # PDF extraction inserts line breaks mid-sentence, so compare on collapsed whitespace.
    return re.sub(r"\s+", " ", raw)


# Categories that describe something appearing IN CONTENT, as opposed to structural ones
# like `definition` or `legal_basis` that describe the table itself. Only these can be
# exercised by a test case.
CONTENT_CATEGORIES = {
    "violence", "sexual_content", "nudity", "strong_language", "fear_distress",
    "imitable_behaviour", "suicide_self_harm", "drugs_alcohol_smoking",
    "hatred_discrimination", "occult_paranormal", "religion",
}


def category_coverage() -> tuple[set[str], set[str], dict[str, int]]:
    """Which content categories the case list exercises, and which have rules and no test."""
    with C.RULES_CSV.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["content_category"]] = counts.get(r["content_category"], 0) + 1

    cases = C.CASES_MD.read_text(encoding="utf-8")
    summary = cases.split("| # | Content")[1].split("The category column")[0]
    used = set(re.findall(r"`([a-z_]+)`", summary))

    with_rules = {c for c in CONTENT_CATEGORIES if counts.get(c)}
    return used & with_rules, with_rules - used, counts


def doc_count_claims() -> list[str]:
    """Numbers asserted in prose that no longer match the table.

    A count written into a sentence goes stale the moment a rule is added, and prose is
    exactly where nobody looks. Three were stale when this check was written.
    """
    with C.RULES_CSV.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    live = {
        "judgment-based": sum(1 for r in rows if r["determinacy"] == C.JUDGMENT_DETERMINACY),
        "bright lines": sum(1 for r in rows if r["determinacy"] == "bright_line"),
    }
    total = len(rows)
    wrong = []

    # Bare totals: "103 rules", "103 approved". A reviewer changed the README to say
    # "104 rules" and this check passed, because it only matched the "N of M rules are X"
    # shape. A narrow check that reports success is the defect this repo keeps finding.
    for doc in sorted(C.ROOT.rglob("*.md")):
        if "originals" in str(doc):
            continue
        text = doc.read_text(encoding="utf-8")
        for m in re.finditer(r"\b(\d{2,4}) rules\b", text):
            n = int(m.group(1))
            # Only flag numbers close enough to be a claim about the table's size; a
            # sentence like "35 rules carried no quote" is a real subset, not a total.
            if abs(n - total) <= 10 and n != total:
                wrong.append(f"{C.relative(doc)}: says {m.group(0)!r}, table holds {total}")
        for m in re.finditer(r"\b(\d{2,4}) approved\b", text):
            n = int(m.group(1))
            live_approved = sum(1 for r in rows if r["status"] == C.USABLE_STATUS)
            if abs(n - live_approved) <= 10 and n != live_approved:
                wrong.append(f"{C.relative(doc)}: says {m.group(0)!r}, "
                             f"table has {live_approved} approved")

    # Any bare "N of <total>" or "all N <verb>" where N is close to the live total. These
    # forms slipped a blanket renumber and left "105 rules, all 105 approved ... all 103
    # carry a verbatim quote" sitting in a deliverable: one sentence, both numbers, one of
    # them wrong.
    live_total = len([r for r in rows if r["status"] == C.USABLE_STATUS])
    for doc in sorted(C.ROOT.rglob("*.md")):
        if "originals" in str(doc):
            continue
        text = doc.read_text(encoding="utf-8")
        for m in re.finditer(rf"\b(\d{{2,4}}) of {live_total}\b", text):
            if int(m.group(1)) > live_total:
                wrong.append(f"{C.relative(doc)}: says {m.group(0)!r}, which is more than "
                             f"the {live_total} rules that exist")
        # IGNORECASE matters: the sentence this was written for begins "All 105 carry",
        # and a lowercase-only pattern silently matched nothing.
        for m in re.finditer(r"\ball (\d{2,4}) (?:approved )?(?:rules? )?"
                             r"(carry|verify|are approved)\b", text, re.I):
            n = int(m.group(1))
            if abs(n - live_total) <= 10 and n != live_total:
                wrong.append(f"{C.relative(doc)}: says {m.group(0)!r}, table has {live_total}")

    # A file count in prose drifts the first time a script is added or deleted.
    words = {13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
             17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}
    n_py = len(list(C.PIPELINE_DIR.glob("*.py")))
    readme = C.ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for n, word in words.items():
            if n != n_py and re.search(rf"\b{word} Python files\b", text, re.I):
                wrong.append(f"README.md: says {word!r} Python files, out_of_scope/pipeline/ holds "
                             f"{n_py}")
    # The N-of-M scan used to miss three real stale counts, each by a different dodge:
    #   "38 of 103 current rules are judgment-based"  - a filler word before "rules"
    #   "38 of 103 rules are `judgment_based`"        - backticks and an underscore
    #   "38 of 103 rules are judgement calls"         - British spelling, different noun
    # So normalise the prose before matching rather than widening the pattern each time a
    # new phrasing turns up. A check that only catches the spelling I happened to use is
    # the same bug as no check at all.
    def normalise(s: str) -> str:
        s = s.replace("`", "").replace("_", "-")
        s = re.sub(r"\bjudgement\b", "judgment", s, flags=re.I)
        s = re.sub(r"\bjudgment(?:-based| calls?| rules?)\b", "judgment-based", s, flags=re.I)
        s = re.sub(r"\bbright(?:-| )lines?\b", "bright-line", s, flags=re.I)
        return s

    for doc in sorted(C.ROOT.rglob("*.md")):
        if "originals" in str(doc):
            continue
        text = normalise(doc.read_text(encoding="utf-8"))
        for phrase, want in live.items():
            key = normalise(phrase)
            # (\d+) of (\d+) [optional adjectives] rules are [optional words] <phrase>
            for m in re.finditer(
                    rf"(\d+) of (\d+)(?: [a-z]+){{0,2}} rules are(?: [a-z]+){{0,2}}[ -]*"
                    rf"{re.escape(key)}", text):
                if int(m.group(1)) != want or int(m.group(2)) != total:
                    wrong.append(f"{C.relative(doc)}: says {m.group(0)!r}, "
                                 f"table says {want} of {total}")
    return wrong


def dead_links() -> list[str]:
    """Every relative markdown link must point at a file that exists.

    This exists because reorganising folders rewrote link LABELS and left the TARGETS
    behind, so a line read `[out_of_scope/TASK1_WRITEUP.md](TASK1_WRITEUP.md)` and looked correct while
    pointing nowhere. It also guards the harder requirement: a deliverable folder has to
    stand on its own, so a copy that still links back to a file left outside the folder is
    a broken handover even though the link works in the full repo.
    """
    import urllib.parse
    bad = []
    for md in sorted(C.ROOT.rglob("*.md")):
        if ".git/" in str(md):
            continue
        for m in re.finditer(r"\[([^\]]*)\]\(([^)\s]+)\)", md.read_text(encoding="utf-8")):
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = urllib.parse.unquote(target.split("#")[0])
            if not rel:
                continue
            resolved = (md.parent / rel).resolve()
            if not resolved.exists():
                bad.append(f"{C.relative(md)}: [{m.group(1)[:40]}] points at {target!r}, "
                           f"which is not there")
                continue
            # A deliverable folder is handed over on its own, so a link that resolves only
            # because the rest of the repository happens to sit around it is still broken
            # for whoever receives just the folder.
            for box in (C.ROOT / "deliverables" / "task1", C.ROOT / "deliverables" / "task2"):
                if box in md.parents and box not in resolved.parents and resolved != box:
                    bad.append(f"{C.relative(md)}: [{m.group(1)[:40]}] points at {target!r}, "
                               f"which is outside {box.name}/ and would not travel with it")
    return bad


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    failures = []
    checked = 0
    for case, rel, phrases in CLAIMS:
        path = C.ROOT / rel
        if not path.is_file():
            failures.append(f"{case}: source not on disk: {rel}")
            continue
        body = text_of(path)
        for phrase in phrases:
            checked += 1
            if re.sub(r"\s+", " ", phrase) not in body:
                failures.append(f"{case}: not found in {path.name}: {phrase!r}")

    if failures:
        print("CASE CLAIMS THAT DO NOT HOLD UP:")
        for f in failures:
            print(f"  - {f}")
        print("\nA back-test whose 'known outcome' is not in the source is not a back-test.")
        return 1

    print(f"{checked} quoted claim(s) across {len(CLAIMS)} case(s) verify against the "
          f"stored sources.")
    print("This checks the OUTCOME is quoted correctly. It does not check that the case "
          "description matches the content the regulator actually saw.")

    stale = doc_count_claims()
    if stale:
        print("\nSTALE NUMBERS IN THE DOCUMENTS:")
        for s in stale:
            print(f"  - {s}")
        print("  A count written into prose goes stale the moment a rule is added, and prose "
              "is where nobody looks.")
        return 1

    broken = dead_links()
    if broken:
        print("\nLINKS THAT POINT AT NOTHING:")
        for b in broken:
            print(f"  - {b}")
        print("  A deliverable folder has to stand on its own. A link to a file that is not "
              "there is a dead end for whoever opens it.")
        return 1

    covered, untested, counts = category_coverage()
    total = len(covered) + len(untested)
    print(f"\nCATEGORY COVERAGE: the cases exercise {len(covered)} of {total} content "
          f"categories that have rules.")
    if untested:
        print("  Rules exist and no case touches them:")
        for c in sorted(untested, key=lambda c: (-counts[c], c)):
            print(f"    {c:24} {counts[c]} rule(s)")
        print("  Not a failure, but a pass rate measured on these cases is a pass rate on "
              "the covered categories only. Print the denominator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
