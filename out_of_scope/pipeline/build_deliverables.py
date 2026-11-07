#!/usr/bin/env python3
"""Assemble deliverables/task1 and deliverables/task2: only what was asked for.

WHY THIS EXISTS

The repository holds the deliverables and the apparatus that produced them, mixed together
because that is how the work happened. A reader marking the submission should not have to
work out which is which, and a list in a README is a weaker answer than two folders with
nothing else in them.

So this copies out the artefacts the brief actually names, and nothing else. No pipeline, no
checkers, no notebooks, no review brief, no rule-building prompt. Those are how the work got
done, not what was asked for.

WHAT GOES IN, AND THE RULE FOR DECIDING

Task 1 names six things: sources and a table of rules, the prompt, the test cases, the
results, the design choices, the models and tools. Task 2 names five questions plus four
items: a process diagram, a worked rule, a validation plan, success metrics.

A file is copied if it IS one of those, or if a reader cannot understand one of those
without it. The raw run outputs qualify because "the results of the runs" is not checkable
without them.

Everything is a copy. The folders are generated and disposable; the repository is the
original. Re-run this after changing anything.

usage: python out_of_scope/pipeline/build_deliverables.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C  # noqa: E402

OUT = C.ROOT / "deliverables"

# (source, destination relative to the task folder, why it is here)
TASK1: list[tuple[pathlib.Path, str, str]] = [
    (C.SOURCE_INVENTORY_MD, "1_sources/00_SOURCE_INVENTORY.md",
     "deliverable 1: the sources, with links and scope"),
    (C.ORIGINALS_DIR, "1_sources/originals",
     "the documents themselves, so every quote can be checked"),
    (C.RULES_XLSX, "2_rules/RULES_TABLE_v1.xlsx",
     "deliverable 1: the table of rules"),
    # NOT the CSV mirror. It is in the repository because an .xlsx is a binary blob that
    # GitHub cannot diff, so a rule change would be unreviewable without it. Neither reason
    # applies to a folder someone opens to read the rules, where it is just one of the six
    # tabs again under a second filename.
    (C.PROMPTS_DIR / "HOW_TO_RUN.md", "3_prompt/HOW_TO_RUN.md",
     "how to run the two prompts, including the rule-selection step between them"),
    (C.PROMPTS_DIR / "RUN_1_describe_content.md", "3_prompt/RUN_1_describe_content.md",
     "deliverable 2: reads the content"),
    (C.DECISION_PROMPT, "3_prompt/RUN_2_decide.md",
     "deliverable 2: applies the rules and decides"),
    (C.CASES_MD, "4_test_cases/CASES.md", "deliverable 3: the test cases"),
    (C.TESTS_DIR / "inputs", "4_test_cases/inputs",
     "each case's input on its own, as fed to the prompt"),
    (C.TESTS_DIR / "RESULTS.md", "5_results/RESULTS.md", "deliverable 4: the results"),
    (C.TESTS_DIR / "runs", "5_results/runs",
     "the raw model outputs, so the results can be checked rather than believed"),
    (C.TASK1_MD, "6_design_choices/TASK1_WRITEUP.md",
     "deliverables 5 and 6: scope, design choices, and the models and tools used"),
    (C.TIMELINE_HTML, "2_rules/timeline.html",
     "not asked for: a 24-hour view of which rules bite when, built from the table"),
]

TASK2: list[tuple[pathlib.Path, str, str]] = [
    (C.TASK2_MD, "TASK2_SCALING.md",
     "the five questions, the process diagram, the worked rule, the validation plan, "
     "the metrics"),
    (C.DIAGRAMS_HTML, "process_diagram.html",
     "the process diagram, large and scrollable"),
]


# A deliverable folder has to stand on its own. The repository copies of these documents
# refer to the apparatus that produced them, which is correct there and dangling here, so
# every such reference is rewritten on the way out.
#
# Two kinds. A file that IS in the folder gets its path corrected. A file that is not gets
# replaced by a description of what it does, with no path at all: a reader should learn what
# checked a claim without being sent to a file that is not in front of them.
REWRITES: list[tuple[str, str]] = [
    # paths that exist in the folder, under a different name
    ("`tests/runs/`", "`runs/`"),
    ("`tests/runs`", "`runs/`"),
    ("out_of_scope/tests/CASES.md", "CASES.md"),
    ("out_of_scope/tests/RESULTS.md", "RESULTS.md"),
    ("out_of_scope/tests/PROMPT_DEFECTS.md", "`RESULTS.md`"),
    ("`rules/RULES_TABLE_v1.xlsx`", "`2_rules/RULES_TABLE_v1.xlsx`"),
    ("`rules/csv/Rules.csv`", "`2_rules/RULES_TABLE_v1.xlsx`"),
    ("`sources/originals/`", "`1_sources/originals/`"),
    ("`sources/originals`", "`1_sources/originals`"),
    # apparatus: describe, do not link
    ("`out_of_scope/pipeline/verify_rules.py --with-quotes`",
     "the quote checker (in the repository, not in this folder)"),
    ("`out_of_scope/pipeline/verify_rules.py`", "the quote and schema checker (repository only)"),
    ("`out_of_scope/pipeline/verify_cases.py`", "the test-claim checker (repository only)"),
    ("`out_of_scope/pipeline/postcheck.py`", "the decision checker (repository only)"),
    ("`out_of_scope/pipeline/precheck.py`", "the pre-decision gates (repository only)"),
    ("`out_of_scope/pipeline/run_decision.py`", "the prompt assembler (repository only)"),
    ("`out_of_scope/pipeline/build_rules_table.py`", "the table builder (repository only)"),
    ("`out_of_scope/pipeline/build_inventory.py`", "the inventory builder (repository only)"),
    ("`out_of_scope/pipeline/build_timeline.py`", "the chart builder (repository only)"),
    ("`out_of_scope/pipeline/build_diagrams.py`", "the diagram renderer (repository only)"),
    ("`out_of_scope/pipeline/fetch_precedents.py`", "the precedent fetcher (repository only)"),
    ("`out_of_scope/pipeline/fetch_originals.py`", "the source fetcher (repository only)"),
    ("`out_of_scope/pipeline/fetch_with_browser.py`", "the browser fetcher (repository only)"),
    ("`out_of_scope/pipeline/import_saved.py`", "the import script (repository only)"),
    ("`out_of_scope/pipeline/supersede.py`", "the rule-closing script (repository only)"),
    ("`out_of_scope/pipeline/render_answer.py`", "the answer-table renderer (repository only)"),
    ("`out_of_scope/pipeline/build_deliverables.py`", "the script that assembles these folders"),
    ("`out_of_scope/pipeline/constants.py`", "the shared constants file (repository only)"),
    ("`out_of_scope/BUILD_rules_from_sources.md`",
     "the rule-building prompt (repository only; not a deliverable)"),
    ("[`out_of_scope/HOW_IT_WORKS.md`](out_of_scope/HOW_IT_WORKS.md)", "the repository walkthrough"),
    ("`out_of_scope/HOW_IT_WORKS.md`", "the repository walkthrough"),
    ("`verify.yml`", "the CI workflow (repository only)"),
    ("`MANIFEST.csv`", "the source manifest (repository only)"),
    ("`expect.json`", "the identity-check file (repository only)"),
    ("`sources/originals/NOTES.md`", "the per-source notes (repository only)"),
    ("`originals.lock.json`", "the source lockfile (repository only)"),
    ("`sources/99_EXTRACTION_NOTES_AND_LIMITS.md`", "the extraction notes (repository only)"),
    ("`rules/csv/Open_Questions.csv`",
     "the Open_Questions tab of the rules table"),
    ("`TASK2_SCALING.md`", "the Task 2 proposal, in `deliverables/task2/`"),
    ("`tests/inputs/`", "`inputs/`"),
    # bare script names, which survive the out_of_scope/pipeline/ rewrites above
    ("`verify_rules.py --with-quotes`", "the quote checker"),
    ("`verify_rules.py`", "the quote checker"),
    ("`verify_cases.py`", "the test-claim checker"),
    ("`postcheck.py`", "the decision checker"),
    ("`precheck.py`", "the pre-decision gates"),
    ("`run_decision.py`", "the prompt assembler"),
    ("`build_rules_table.py`", "the table builder"),
    ("`build_inventory.py`", "the inventory builder"),
    ("`build_timeline.py`", "the chart builder"),
    ("`fetch_originals.py`", "the source fetcher"),
    ("`fetch_with_browser.py`", "the browser fetcher"),
    ("`import_saved.py`", "the import script"),
    ("`tests/`", "this folder"),
    ("`out_of_scope/docs/timeline.html`", "`2_rules/timeline.html`"),
    ("`out_of_scope/docs/diagrams.html`", "`process_diagram.html`"),
]


def rewrite_refs(folder: pathlib.Path) -> int:
    """Point every reference at something that is actually in the folder, or at nothing."""
    changed = 0
    for md in folder.rglob("*.md"):
        text = original = md.read_text(encoding="utf-8")
        for old, new in REWRITES:
            text = text.replace(old, new)
        if text != original:
            md.write_text(text, encoding="utf-8")
            changed += 1
    return changed

def copy(src: pathlib.Path, dest: pathlib.Path) -> int:
    """Copy a file or a directory. Returns how many files landed."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        # The source folder holds the documents AND the machinery that fetched and
        # verified them. Only the documents are a deliverable: the manifest, the lockfile
        # and the expectation file are how they were collected and checked, and the links
        # and scope they carry are already presented in 00_SOURCE_INVENTORY.md, which is
        # generated from them.
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", "incoming", "unused",
            "MANIFEST.csv", "expect.json", "originals.lock.json", "NOTES.md", "README.md"))
        return sum(1 for _ in dest.rglob("*") if _.is_file())
    shutil.copy2(src, dest)
    return 1


def build(name: str, items: list[tuple[pathlib.Path, str, str]]) -> list[str]:
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    lines, total, missing = [], 0, []
    for src, rel, why in items:
        if not src.exists():
            missing.append(C.relative(src))
            continue
        n = copy(src, folder / rel)
        total += n
        lines.append(f"| `{rel}` | {why} |")
    print(f"  {name}: {total} file(s)")
    if missing:
        print(f"    MISSING, not copied: {missing}")
    return lines


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    OUT.mkdir(exist_ok=True)
    t1 = build("task1", TASK1)
    t2 = build("task2", TASK2)

    (OUT / "task1" / "README.md").write_text(
        "# Task 1 deliverables\n\n"
        "Everything the brief asks for, and nothing else. Generated by "
        "`out_of_scope/pipeline/build_deliverables.py` from the repository root, which holds these files "
        "alongside the apparatus that produced them.\n\n"
        "| Asked for | Where |\n|---|---|\n"
        "| Sources and a table of rules | `1_sources/`, `2_rules/` |\n"
        "| The full prompt | `3_prompt/`. Start with `HOW_TO_RUN.md` |\n"
        "| The test cases | `4_test_cases/` |\n"
        "| The results of the runs | `5_results/` |\n"
        "| A short explanation of design choices | `6_design_choices/TASK1_WRITEUP.md` |\n"
        "| The models and tools used | same file, last section |\n\n"
        "## What each file is for\n\n| File | Why it is here |\n|---|---|\n"
        + "\n".join(t1) +
        "\n\n## What is deliberately not here\n\n"
        "The prompt that built the rules table, and the sixteen scripts that fetch, check "
        "and render. The brief asks for a table of rules, not for a method of producing "
        "one. Those live in the repository and are described in its README.\n\n"
        "## Read this first\n\n"
        "`5_results/RESULTS.md` is the honest one. All eight cases were run blind, by agents "
        "that had not seen the expected answers, and the raw outputs are in `5_results/runs/` "
        "so the claims can be checked rather than believed. It also records what the runs "
        "got wrong, including a prediction of mine that turned out to be false.\n",
        encoding="utf-8")

    (OUT / "task2" / "README.md").write_text(
        "# Task 2 deliverables\n\n"
        "Task 2 asks for a **design**, not a system: how sources would be collected and "
        "validated, how rules would be organised, what is shared and what is "
        "country-specific, how correctness would be tested, and how it would be measured.\n\n"
        "| Asked for | Where |\n|---|---|\n"
        "| 1. Source collection and validation | `TASK2_SCALING.md`, section 1 |\n"
        "| 2. Organizing the rules | section 2 |\n"
        "| 3. Solution structure | section 3 |\n"
        "| 4. Correctness testing | section 4 |\n"
        "| 5. Measurement and diagnosis | section 5 |\n"
        "| A process diagram | `process_diagram.html`, and inline in the document |\n"
        "| An example of how a single rule is represented | the deliverable section after 2 |\n"
        "| A validation plan | section 4 |\n"
        "| Success metrics | section 5 |\n"
        "| What can be automated and where a local expert is required | "
        "`TASK2_SCALING.md`, \"What can be automated\" |\n\n"
        "The brief also says: *you are not required to actually collect rules for dozens of "
        "countries as part of this task.* Nothing here does.\n\n"
        "## What each file is for\n\n| File | Why it is here |\n|---|---|\n"
        + "\n".join(t2) +
        "\n\n## Note on length\n\n"
        "This is longer than a concise proposal should be. An external reviewer put it at "
        "around four times the length it needs, and was right. The five questions and the "
        "four required items are all answered; the excess is in the discussion around "
        "them.\n",
        encoding="utf-8")

    for name in ("task1", "task2"):
        n = rewrite_refs(OUT / name)
        print(f"  {name}: rewrote references in {n} file(s)")

    print(f"\nwrote {C.relative(OUT)}/task1 and {C.relative(OUT)}/task2")
    print("These are COPIES. The repository is the original; re-run this after any change.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
