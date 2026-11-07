#!/usr/bin/env python3
"""Check that the outcomes claimed in tests/CASES.md are really in the stored sources.

A back-test is only worth anything if the "known outcome" is actually known. TC-01 claims a
regulator reached a particular decision, and that claim carries the whole case: if it is
wrong, the test measures nothing and looks like the strongest evidence in the repo.

So the claim is treated the same way as a rule. Quote the source, store the source, and check
the quote mechanically. This is the same check `verify_rules.py --with-quotes` runs over the
rules table, pointed at the test cases instead.

usage: python pipeline/verify_cases.py
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (case, source file on disk, phrases that must appear in it verbatim)
CLAIMS = [
    ("TC-01", "sources/originals/UK-P1_ofcom_decision_toofan.pdf", [
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
    with (ROOT / "rules/csv/Rules.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["content_category"]] = counts.get(r["content_category"], 0) + 1

    cases = (ROOT / "tests/CASES.md").read_text(encoding="utf-8")
    summary = cases.split("| # | Content")[1].split("The category column")[0]
    used = set(re.findall(r"`([a-z_]+)`", summary))

    with_rules = {c for c in CONTENT_CATEGORIES if counts.get(c)}
    return used & with_rules, with_rules - used, counts


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    failures = []
    checked = 0
    for case, rel, phrases in CLAIMS:
        path = ROOT / rel
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
