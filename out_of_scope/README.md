# Out of scope

Everything in this folder is **not** part of what the assignment asked for.

The assignment asked for two things: a working prompt that reads a content description and
returns age ratings and broadcast restrictions for the UK and France, and a written plan for
scaling that to dozens of countries. Those live in `deliverables/task1` and
`deliverables/task2`.

This folder holds the scaffolding I built around that work. It is here because a reviewer
may want to see how the table was built and checked, but none of it is a deliverable, and
nothing in `deliverables/` depends on reading any of it.

## What is in here

| Item | What it is | Why it is out of scope |
|---|---|---|
| `prompts/`, `rules/`, `sources/`, `tests/` | The originals that `deliverables/` is generated from: the two prompts, the rules table, the 20 source documents, and the test cases with their saved runs | These ARE the deliverables, but the copies in `deliverables/` are the handover. These are the working originals, kept so the build can regenerate the copies and so the checks have something to check. |
| `TASK1_WRITEUP.md`, `TASK2_SCALING.md` | The originals of the two write-ups | Same reason. The copies that get read live in `deliverables/`. |
| `pipeline/` | 17 Python scripts that build the rules table, check it, and run a decision end to end | The assignment asked for a prompt, not a program. These scripts build and test the thing that was asked for. They are not the thing that was asked for. |
| `BUILD_rules_from_sources.md` | A prompt that turns a legal document into draft table rows | This is how I made the rules table. The table is a deliverable; the tool that produced it is not. Task 2 describes this step as part of a design, which is all the brief asked for. |
| `docs/` | Generated pictures: the Task 2 process diagram, a rules timeline, a diagram index | These are generated from files that are deliverables. The copies that reviewers need are already inside `deliverables/`. |
| `HOW_IT_WORKS.md` | A step by step walkthrough of all 14 stages of the pipeline | Describes the scaffolding above, in detail nobody needs in order to judge the prompt. |
| `SCOPE.md` | My notes on what I decided to include and leave out, and why | Useful background on my reasoning. Not one of the listed deliverables. |

## One thing that could not be moved here

`.github/workflows/verify.yml` is still at the top of the repository. It is the automated
check that runs every time I save work, and GitHub only looks for it in that exact location,
so moving it into this folder would quietly switch it off. It is scaffolding like everything
else in this folder, and it runs the scripts in `pipeline/`.

## If you want to run any of it

The scripts expect to be run from the top of the repository, like this:

```
python3 out_of_scope/pipeline/verify_rules.py --with-quotes
```

They need Python 3.12 with `openpyxl` and `pypdf` installed. They do not need an API key,
because none of them call a model. Sending the prompt to a model is a manual step, and
`prompts/HOW_TO_RUN.md` explains it.
