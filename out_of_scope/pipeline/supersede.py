#!/usr/bin/env python3
"""Close out the rules that came from a document a regulator has replaced.

THE RULE THIS ENFORCES: never delete a row.

When a source document is amended, the old rules do not become wrong, they become **wrong as
of a date**. If a regulator asks in two years why a programme went out when it did, the answer
has to be the rule as it stood on the day of broadcast. Delete the row and that question
cannot be answered at all.

So an amendment closes rows rather than removing them: `valid_to` gets the date, `status`
becomes `superseded`, and the decision engine stops selecting them because it only reads
`approved`. The row stays readable forever.

HONEST NOTE ON MATURITY

No rule in this table has been through this. Nothing was amended during the project, so every
row is a first version and `superseded` has never had anything in it. This file exists so
that path is real code with a dry run and a test, rather than a paragraph in a document
claiming the system supports versioning.

usage:
  python out_of_scope/pipeline/supersede.py FR-R2                 show what would change, write nothing
  python out_of_scope/pipeline/supersede.py FR-R2 --apply         write it
  python out_of_scope/pipeline/supersede.py FR-R2 --apply --as-of 2026-03-01
"""
from __future__ import annotations

import argparse
import csv
import datetime
import pathlib
import sys

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C



def load() -> tuple[list[dict], list[str]]:
    with C.RULES_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader), list(reader.fieldnames or [])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source_doc", help="the source_doc value whose rules are superseded")
    ap.add_argument("--apply", action="store_true",
                    help="write the change. Without this it is a dry run.")
    ap.add_argument("--as-of", default=datetime.date.today().isoformat(),
                    help="the date the old wording stopped applying (default: today)")
    args = ap.parse_args()

    try:
        datetime.date.fromisoformat(args.as_of)
    except ValueError:
        print(f"--as-of must be YYYY-MM-DD, got {args.as_of!r}")
        return 2

    rows, fields = load()
    if not rows:
        print("no rules on disk")
        return 2

    known = {r["source_doc"] for r in rows}
    if args.source_doc not in known:
        print(f"no rules cite source_doc {args.source_doc!r}.")
        print(f"known: {', '.join(sorted(known))}")
        return 2

    # "Live" means still in force: not already closed and not already superseded.
    hits = [r for r in rows
            if r["source_doc"] == args.source_doc
            and r["status"] != C.SUPERSEDED_STATUS
            and (r["valid_to"] or C.OPEN_VALID_TO) == C.OPEN_VALID_TO]

    if not hits:
        print(f"{args.source_doc}: nothing live to close. Already superseded, or the rows "
              f"carry a valid_to date.")
        return 0

    print(f"{args.source_doc}: {len(hits)} live rule(s) would be closed as of {args.as_of}")
    for r in hits:
        print(f"  {r['rule_id']:12} {r['clause_ref'][:34]:34} "
              f"status {r['status']} -> superseded")

    if not args.apply:
        print("\nDry run. Re-run with --apply to write it.")
        print("Then extract the replacement rules from the new document and add them as NEW "
              "rows. Do not edit the closed ones; the point of keeping them is that a past "
              "decision can still be explained.")
        return 0

    closed = {r["rule_id"] for r in hits}
    for r in rows:
        if r["rule_id"] in closed:
            r["valid_to"] = args.as_of
            r["status"] = C.SUPERSEDED_STATUS

    with C.RULES_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nwrote {C.relative(C.RULES_CSV)}: {len(closed)} row(s) superseded.")
    print("The spreadsheet is generated from build_rules_table.py, so update its source "
          "rows there too, or the next build will undo this.")
    print("Then run: python out_of_scope/pipeline/verify_rules.py --with-quotes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
