#!/usr/bin/env python3
"""Deterministic checks on a decision, AFTER the model has produced one.

These are steps 13 and 14 of the flow in out_of_scope/HOW_IT_WORKS.md. Both used to be drawn as code and
were not code: step 13 was a property asserted in a docstring, and step 14 was left to the
model's own sense of whether it was sure. Neither is a judgement call, so neither should have
been.

WHAT THIS CATCHES THAT NOTHING ELSE DOES

1. A CITED RULE THAT DOES NOT EXIST. The single most dangerous failure in a compliance tool
   is not a wrong answer, it is a wrong answer wearing a citation. A decision reading
   "prohibited before 22:30 (UK-SCH-012)" is indistinguishable from a correct one unless
   somebody looks UK-SCH-012 up. Looking it up is a dictionary lookup, so it runs here and
   nobody has to remember to do it.

2. A CITED RULE THAT EXISTS BUT IS NOT USABLE. A row that is `draft`, `unverified` or
   `superseded` is in the table deliberately and must never reach a decision. Citing one is
   worse than citing nothing, because the rule_id resolves and the citation looks sound.

3. AN ESCALATION THAT DID NOT HAPPEN. If a decision rests on a rule whose `determinacy` is
   `judgment_based`, a person has to see it. That is not the model's call: it is a property
   of the rule, recorded in the table, and therefore checkable. Same for a decision that
   claims high confidence while listing missing information that would change the answer.

WHAT IT DELIBERATELY DOES NOT CHECK

Whether the answer is RIGHT. Nothing here reads the content or weighs a threshold. A decision
can pass every check in this file and be wrong, and the only thing that catches that is a
person, or a test case with a known answer. These checks establish that the answer is
well-formed, honestly sourced and correctly routed. That is a floor, not a verdict.

usage: postcheck.py <run2_output.json>

exit 0  every check passed
exit 1  the decision must go to a person and did not say so
exit 2  the decision is malformed or cites something that does not hold up
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C



def load_rules() -> dict[str, dict]:
    with C.RULES_CSV.open(newline="", encoding="utf-8") as fh:
        return {r["rule_id"]: r for r in csv.DictReader(fh)}


def cited_ids(decision: dict) -> list[tuple[str, str]]:
    """Every rule_id the decision leans on, with where it was cited from."""
    out = []
    for axis in ("classification", "hours"):
        for b in (decision.get(axis) or {}).get("basis", []) or []:
            if b.get("rule_id"):
                out.append((b["rule_id"], axis))
    for r in decision.get("other_restrictions", []) or []:
        for b in r.get("basis", []) or []:
            if b.get("rule_id"):
                out.append((b["rule_id"], f"other_restrictions/{r.get('kind', '?')}"))
    return out


def check_decision(d: dict, rules: dict[str, dict]) -> tuple[list[str], list[str]]:
    """Returns (defects, escalations). Defects are exit 2; escalations are exit 1."""
    defects: list[str] = []
    escalations: list[str] = []
    where = f"{d.get('country', '?')}/{d.get('transmission', '?')}"

    cites = cited_ids(d)
    if not cites:
        defects.append(f"{where}: the decision cites no rule at all. Every claim has to "
                       f"carry a rule_id; an uncited decision is an opinion.")

    for rule_id, axis in cites:
        rule = rules.get(rule_id)
        if rule is None:
            defects.append(f"{where}: cites {rule_id} on '{axis}', which is not in the "
                           f"rules table. The citation is invented.")
            continue
        if rule["status"] != C.USABLE_STATUS:
            defects.append(f"{where}: cites {rule_id} on '{axis}', which is in the table "
                           f"with status '{rule['status']}'. Only '{C.USABLE_STATUS}' rows "
                           f"may reach a decision.")
            continue
        if rule["country"] != d.get("country"):
            defects.append(f"{where}: cites {rule_id}, which is a {rule['country']} rule, "
                           f"for a {d.get('country')} decision.")

    # Step 14, the part of "clear-cut?" that is a property of the rules rather than a feeling.
    # Only rules in `basis` count. A rule the model read and set aside lives in
    # `rules_checked_not_triggered` and is NOT a judgement it made about this content.
    #
    # Before this distinction existed, every judgement rule in the slice counted as relied
    # on, so every decision escalated: 17 of 17 on the first full run, including a benign
    # control about a plaster on a cut finger. Each escalation was defensible and the system
    # was useless. The fix is not to loosen the rule but to stop miscounting what it applies
    # to.
    checked_only = {r.get("rule_id") for r in d.get("rules_checked_not_triggered") or []}
    judgment = sorted({rid for rid, _ in cites
                       if rid not in checked_only
                       and rules.get(rid, {}).get("determinacy") == C.JUDGMENT_DETERMINACY})
    if judgment and not d.get("human_review_required"):
        escalations.append(
            f"{where}: rests on {', '.join(judgment)}, which {'is' if len(judgment) == 1 else 'are'} "
            f"judgment_based, but human_review_required is not set. Whether a judgement is "
            f"involved is a property of the rule, not a matter of how confident the answer "
            f"sounds.")

    conf = d.get("confidence")
    high = conf == "high" or (isinstance(conf, (int, float)) and conf >= 0.9)
    if d.get("missing_information") and high:
        fields = ", ".join(m.get("field", "?") for m in d["missing_information"])
        escalations.append(f"{where}: confidence is high ({conf}) while {fields} "
                           f"{'is' if len(d['missing_information']) == 1 else 'are'} listed as "
                           f"missing. If the missing field would not change the answer it "
                           f"does not belong in missing_information; if it would, the "
                           f"confidence is not high.")

    if d.get("coverage_gaps") and not d.get("human_review_required"):
        escalations.append(f"{where}: reports observations that matched no rule "
                           f"({len(d['coverage_gaps'])}) without routing to a person. A gap "
                           f"in the table is not the same as permission.")

    # The three axes are substitutes for one another, so a missing one is not a blank, it is
    # an unasked question. See the three-axis note in RUN_2_decide.md.
    for axis in ("classification", "hours"):
        if not d.get(axis):
            defects.append(f"{where}: no '{axis}' in the output. The three axes are "
                           f"reported separately even when one of them is 'none'.")
    if "other_restrictions" not in d:
        defects.append(f"{where}: no 'other_restrictions' key. An empty list says 'none "
                       f"found'; an absent key says nobody looked.")

    return defects, escalations


def slice_ids(context_path: pathlib.Path) -> set[str] | None:
    """The rule_ids that were actually handed to the model, read back from its own prompt.

    WHY THIS EXISTS. Checking a citation against the whole table is not enough. The model is
    given a SLICE, and a rule outside that slice is a rule it never saw, so citing one means
    it reached for regulation from memory. That passes a whole-table check cleanly, because
    the rule is perfectly real.

    This is not hypothetical. On TC-04 a run built both French decisions on a rule that is in
    the table and was not in that case's slice. The run caught it; this checker did not, and
    would not have. The hole was in the one place claiming to make citations trustworthy.
    """
    if not context_path.is_file():
        return None
    body = context_path.read_text(encoding="utf-8", errors="replace")
    # The LAST pair, not the first. The prompt documents its own input format near the top,
    # so an early <rules> is the schema description rather than the data. Reading that one
    # yields an empty slice and then flags every citation, which is a checker that fails
    # loudly instead of silently and is still a broken checker.
    start = body.rfind("<rules>")
    end = body.rfind("</rules>")
    if start < 0 or end < 0 or end < start:
        return None
    found = set(re.findall(r"\b(?:UK|FR|EU)-[A-Z]{2,4}-\d{3}\b", body[start:end]))
    # An empty slice means the parse missed, not that the model was given nothing.
    return found or None


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) > 1 else 2

    path = pathlib.Path(sys.argv[1])
    if not path.is_file():
        print(f"no such file: {path}")
        return 2
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path} is not valid JSON: {e}")
        return 2

    decisions = payload.get("decisions")
    if not decisions:
        print("no 'decisions' in the output. A run that decided nothing should still say so "
              "per country rather than returning an empty object.")
        return 2

    rules = load_rules()

    # If the assembled context sits beside the output, check against the slice too.
    guess = path.with_name(path.name.replace("_run2.json", "_run2_context.txt"))
    in_slice = slice_ids(pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else guess)

    all_defects: list[str] = []
    all_escalations: list[str] = []
    for d in decisions:
        defects, escalations = check_decision(d, rules)
        if in_slice is not None:
            where = f"{d.get('country', '?')}/{d.get('transmission', '?')}"
            for rule_id, axis in cited_ids(d):
                if rule_id in rules and rule_id not in in_slice:
                    defects.append(
                        f"{where}: cites {rule_id} on '{axis}', which is a real rule that "
                        f"was NOT in this decision's slice. The model was never shown it, so "
                        f"it came from memory rather than from the rules supplied.")
        all_defects += defects
        all_escalations += escalations

    if all_defects:
        print("DEFECTS, this decision cannot be served:")
        for x in all_defects:
            print(f"  - {x}")
    if all_escalations:
        print("\nMUST GO TO A PERSON, and the decision did not say so:")
        for x in all_escalations:
            print(f"  - {x}")

    if all_defects:
        return 2
    if all_escalations:
        return 1

    n = len(decisions)
    print(f"{n} decision{'s' if n != 1 else ''} checked. Every cited rule resolves to an "
          f"approved row of the right country, the three axes are all present, and the "
          f"escalation flag agrees with the determinacy of the rules relied on.")
    print("This says the decision is well-formed and honestly sourced. It does NOT say it "
          "is right; nothing here reads the content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
