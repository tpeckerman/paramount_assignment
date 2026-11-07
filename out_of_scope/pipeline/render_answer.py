#!/usr/bin/env python3
"""Turn a decision into the one table someone actually wants: country by country, when can
this go out.

This is the end of the line. Everything else in this repo exists to make this table
trustworthy, and the table is what a scheduler reads.

WHY THIS IS HARDER THAN "A TIME PER COUNTRY"

The obvious shape is one row per country and one time in it. That shape is wrong, and
building it would quietly throw away most of what the system worked out:

1. **One country here issues no age rating for broadcast at all.** A rating column that must
   be filled will be filled with something invented. The cell has to be able to say "this
   country does not do that".

2. **The permitted hours depend on the service**, so the same programme has different answers
   on a free-to-air channel and a premium one. A single row per country cannot hold that, so
   the table is country BY SERVICE, and a request that did not say which service gets a row
   per plausible service rather than a guess.

3. **Hours and conditions are traded against each other.** "Any time, behind a PIN" and "not
   before 22:00" can both be true of one programme, and reporting the hours without the
   condition is wrong in a way that costs money, while reporting a bar without the available
   condition is wrong in a way that loses a slot. Both go in the row.

4. **"Ask a person" is a real answer, not a missing one.** It gets its own styling, because a
   table where every cell looks equally settled is a table that hides its own uncertainty.

5. **Every cell carries the rules behind it.** A time with no rule_id beside it cannot be
   checked by the person who has to defend it.

usage:
  python out_of_scope/pipeline/render_answer.py decision.json             markdown to stdout
  python out_of_scope/pipeline/render_answer.py decision.json --html out.html
"""
from __future__ import annotations

import csv
import html
import json
import pathlib
import sys

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C



def load_rules() -> dict[str, dict]:
    with C.RULES_CSV.open(newline="", encoding="utf-8") as fh:
        return {r["rule_id"]: r for r in csv.DictReader(fh)}


def basis_ids(block: dict) -> list[str]:
    return [b["rule_id"] for b in (block or {}).get("basis", []) or [] if b.get("rule_id")]


def row_for(d: dict, rules: dict) -> dict:
    cls = d.get("classification") or {}
    hrs = d.get("hours") or {}
    others = d.get("other_restrictions") or []

    rating = cls.get("value") or "not stated"
    if rating == "no_per_programme_rating":
        rating = "none issued for broadcast"

    conditions = []
    for o in others:
        req = o.get("requirement") or o.get("kind") or "?"
        if o.get("is_condition_of_the_hours"):
            req += "  (this is what the hours depend on)"
        conditions.append(req)

    cited = sorted(set(basis_ids(cls) + basis_ids(hrs)
                       + [i for o in others for i in basis_ids(o)]))
    judgment = [r for r in cited
                if rules.get(r, {}).get("determinacy") == C.JUDGMENT_DETERMINACY]

    # The verdict is about whether the RULES gave a determinate answer, not about whether
    # the slot someone asked for is approved. "CLEARED" next to "not before 21:00" on a 14:30
    # request reads as approval and is not, so the wording stays neutral and the hours column
    # carries the actual answer.
    if d.get("human_review_required"):
        verdict = "A PERSON MUST DECIDE"
    elif str(hrs.get("permitted", "")).lower().startswith("prohibit"):
        verdict = "CANNOT BE SHOWN AT ALL"
    else:
        verdict = "ANSWERED BY THE RULES"

    return {
        "country": d.get("country", "?"),
        "service": d.get("transmission", "not stated"),
        "verdict": verdict,
        "rating": rating,
        "hours": hrs.get("permitted") or "not determined",
        "hours_plain": hrs.get("without_technical_measure") or "",
        "hours_gated": hrs.get("with_technical_measure") or "",
        "conditions": conditions,
        "cited": cited,
        "judgment": judgment,
        "missing": [m.get("field", "?") for m in d.get("missing_information") or []],
        "gaps": d.get("coverage_gaps") or [],
        "reasons": d.get("review_reasons") or [],
    }


def to_markdown(rows: list[dict], payload: dict) -> str:
    out = ["# When can this be shown", ""]
    out += ["| Country | Service | Verdict | Age rating | Permitted hours | Conditions | Rules |",
            "|---|---|---|---|---|---|---|"]
    for r in rows:
        cond = "<br>".join(r["conditions"]) or "none"
        out.append(f"| {r['country']} | {r['service']} | **{r['verdict']}** | {r['rating']} | "
                   f"{r['hours']} | {cond} | {', '.join(r['cited']) or 'NONE CITED'} |")
    out.append("")

    flagged = [r for r in rows if r["verdict"] == "A PERSON MUST DECIDE"]
    if flagged:
        out += ["## Why a person is needed", ""]
        for r in flagged:
            out.append(f"**{r['country']}, {r['service']}**")
            for reason in r["reasons"]:
                out.append(f"- {reason}")
            if r["judgment"]:
                out.append(f"- Rests on a rule that calls for judgement: "
                           f"{', '.join(r['judgment'])}")
            if r["missing"]:
                out.append(f"- Not told: {', '.join(r['missing'])}")
            if r["gaps"]:
                n = len(r['gaps'])
                out.append(f"- {n} thing{'' if n == 1 else 's'} in the content matched no "
                           f"rule. That is a gap in the table, not permission")
            out.append("")

    if payload.get("cross_country_note"):
        out += ["## Where the countries differ", "", payload["cross_country_note"], ""]

    out += ["---", "",
            "Every time in this table is only as good as the rule beside it. Follow a "
            "`rule_id` into `rules/RULES_TABLE_v1.xlsx` to see the clause and the quote from "
            "the law it came from.", "",
            "This table says what the rules permit. It does not say the content was described "
            "correctly, and nothing downstream of the description can tell."]
    return "\n".join(out)


COLOURS = {"ANSWERED BY THE RULES": ("#e9f5ec", "#2f7d55"),
           "A PERSON MUST DECIDE": ("#fdf0e3", "#b4690e"),
           "CANNOT BE SHOWN AT ALL": ("#fbeaea", "#a8323b")}


def to_html(rows: list[dict], payload: dict) -> str:
    cells = []
    for r in rows:
        bg, fg = COLOURS.get(r["verdict"], ("#f1efea", "#555"))
        cond = "<br>".join(html.escape(c) for c in r["conditions"]) or "<i>none</i>"
        extra = ""
        if r["missing"]:
            extra += (f"<div class='note'>Not told: "
                      f"{html.escape(', '.join(r['missing']))}</div>")
        if r["judgment"]:
            extra += (f"<div class='note'>Judgement rule: "
                      f"{html.escape(', '.join(r['judgment']))}</div>")
        cells.append(f"""
      <tr>
        <td><b>{html.escape(r['country'])}</b><div class='note'>{html.escape(r['service'])}</div></td>
        <td style="background:{bg};color:{fg};font-weight:600">{html.escape(r['verdict'])}</td>
        <td>{html.escape(r['rating'])}</td>
        <td><b>{html.escape(r['hours'])}</b>{extra}</td>
        <td>{cond}</td>
        <td class='ids'>{html.escape(', '.join(r['cited'])) or 'NONE'}</td>
      </tr>""")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>When can this be shown</title>
<style>
  body {{ font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         margin: 2rem auto; max-width: 70rem; color: #222; padding: 0 1rem; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1.5rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: .6rem .7rem; vertical-align: top;
            text-align: left; }}
  th {{ background: #f6f6f4; font-size: 13px; text-transform: uppercase;
        letter-spacing: .04em; }}
  .note {{ font-size: 12px; color: #666; margin-top: .25rem; }}
  .ids {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12px; }}
  .legend span {{ display: inline-block; padding: .2rem .5rem; margin-right: .5rem;
                  border-radius: 3px; font-size: 13px; font-weight: 600; }}
  footer {{ margin-top: 2rem; font-size: 13px; color: #555; border-top: 1px solid #ddd;
            padding-top: 1rem; }}
</style></head><body>
<h1>When can this be shown</h1>
<p class="note" style="font-size:13px">A verdict of ANSWERED BY THE RULES means the rules
produced a determinate answer. It is not approval of any particular slot: read the permitted
hours column for that.</p>
<p class="legend">
  <span style="background:#e9f5ec;color:#2f7d55">ANSWERED BY THE RULES</span>
  <span style="background:#fdf0e3;color:#b4690e">A PERSON MUST DECIDE</span>
  <span style="background:#fbeaea;color:#a8323b">CANNOT BE SHOWN AT ALL</span>
</p>
<table>
  <tr><th>Country</th><th>Verdict</th><th>Age rating</th><th>Permitted hours</th>
      <th>Conditions</th><th>Rules relied on</th></tr>{''.join(cells)}
</table>
<footer>
Every time here is only as good as the rule beside it. Follow a rule id into the rules table
to see the clause and the quote from the law it came from.<br><br>
This table says what the rules permit. It does not say the content was described correctly,
and nothing downstream of the description can tell.
</footer>
</body></html>"""


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) > 1 else 2
    path = pathlib.Path(sys.argv[1])
    if not path.is_file():
        print(f"no such file: {path}")
        return 2
    payload = json.loads(path.read_text(encoding="utf-8"))
    decisions = payload.get("decisions") or []
    if not decisions:
        print("no decisions in that file")
        return 2

    rules = load_rules()
    rows = [row_for(d, rules) for d in decisions]

    if "--html" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--html") + 1])
        dest.write_text(to_html(rows, payload), encoding="utf-8")
        print(f"wrote {dest}")
    else:
        print(to_markdown(rows, payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
