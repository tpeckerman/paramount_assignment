#!/usr/bin/env python3
"""Deterministic gates that run BEFORE the model is asked anything.

The rule this file exists to enforce: **if a step can be done by comparing strings, it must
not be done by a language model.** A model asked a question that code can answer is slower,
costs more, and can be argued out of the right answer. Code cannot.

Two gates:

1. ABSOLUTE PROHIBITIONS WITH A STATED TRIGGER. Two of the eight absolute prohibitions fire on
   a fact the description either states or does not: the certificate is BBFC R18, or the film
   was refused classification. No judgement is involved, so no model should be involved. The
   other six ("seriously impair", "extreme or gratuitous violence") genuinely require reading
   the content and stay with the model.

   The README has said for some time that absolute prohibitions "belong in code". Until now
   nothing enforced one; they were described to the model in a prompt and could therefore be
   reasoned around. This closes that gap for the two that can be closed.

2. CONTROLLED-VOCABULARY VALIDATION of the extraction output. A category outside the list
   silently drops the observation out of every rule lookup. Checking it is a set membership
   test, so it runs here rather than being trusted to the model that produced it.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Prohibitions whose trigger is a STATED FACT rather than a reading of the content.
CERT_PROHIBITIONS = {
    "r18": ("UK-FLM-006", "BBFC R18-rated films must not be broadcast."),
    "refused": ("UK-FLM-001", "No film refused classification by the BBFC may be broadcast."),
    "refused classification": ("UK-FLM-001",
                              "No film refused classification by the BBFC may be broadcast."),
}

# The six that genuinely need the content read, kept here so the split is visible rather than
# implied. Every one turns on a threshold a person or a model has to weigh.
JUDGEMENT_PROHIBITIONS = {
    "UK-GEN-001": "'seriously impair' is a threshold, not a fact",
    "UK-SEX-001": "'R18-equivalent' requires judging the material, not reading a certificate",
    "FR-LAW-001": "'nuire gravement' is a threshold",
    "FR-PRO-001": "'offends human dignity' is a judgement",
    "FR-PRO-002": "requires determining that performers are minors",
    "FR-PRO-003": "'extreme or gratuitous' is a judgement",
}


def controlled_categories() -> set[str]:
    rows = csv.DictReader((ROOT / "rules/csv/Rules.csv").open(newline="", encoding="utf-8"))
    return {r["content_category"] for r in rows}


def check_certificate(observations: dict) -> list[dict]:
    """Fire any prohibition whose trigger is a stated certificate. No model involved."""
    hits = []
    for cert in observations.get("asset", {}).get("existing_certificates", []) or []:
        rating = str(cert.get("rating", "")).strip().lower()
        for key, (rule_id, text) in CERT_PROHIBITIONS.items():
            if rating == key:
                hits.append({"rule_id": rule_id, "trigger": f"certificate = {cert.get('rating')}",
                             "decision": "PROHIBITED", "rule": text,
                             "note": "Decided in code. No context, hour or access control "
                                     "lifts this, so no model is asked."})
    return hits


def check_categories(observations: dict) -> list[str]:
    """A category outside the controlled list drops the observation out of every lookup."""
    allowed = controlled_categories()
    bad = []
    for o in observations.get("observations", []) or []:
        c = o.get("category", "")
        if c and c not in allowed:
            bad.append(f"{o.get('id', '?')}: category {c!r} is not in the controlled "
                       f"vocabulary, so this observation would match no rule")
    return bad


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("usage: precheck.py <run1_output.json>")
        return 0 if len(sys.argv) > 1 else 2

    path = pathlib.Path(sys.argv[1])
    if not path.is_file():
        print(f"no such file: {path}")
        return 2
    try:
        obs = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path} is not valid JSON: {e}")
        print("RUN 1 must emit JSON only. Prose around the object is itself a defect.")
        return 2

    bad = check_categories(obs)
    if bad:
        print("CONTROLLED VOCABULARY, this output cannot be decided on:")
        for b in bad:
            print(f"  - {b}")
        print("\nFix the extraction and re-run. An out-of-vocabulary category does not "
              "produce a wrong answer, it produces a complete-looking answer with the "
              "observation missing, which is the failure mode this whole pipeline is "
              "built against.")
        return 2

    hits = check_certificate(obs)
    if hits:
        print("\nPROHIBITED, decided in code before any model ran:")
        for h in hits:
            print(f"  {h['rule_id']}  {h['trigger']}")
            print(f"     {h['rule']}")
        print("\nNo decision prompt is needed for the UK. Nothing lifts an absolute "
              "prohibition, so asking a model would only create a chance of it being "
              "argued away.")
        return 1

    print("No certificate-triggered prohibition. "
          f"{len(JUDGEMENT_PROHIBITIONS)} other prohibitions need the content read and stay "
          f"with the model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
