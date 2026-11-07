# Age ratings and broadcast restrictions for linear television, UK and France

Take-home assignment, prompt engineer.

The repository has two folders. **`deliverables/` is the assignment.** `out_of_scope/` is
everything else I built along the way, kept so you can check my work, and safe to ignore.

---

## `deliverables/`

Two folders, one per task. Each one stands on its own. Nothing in either links to a file
outside it, so you can open just one and nothing will be missing.

### [`deliverables/task1/`](deliverables/task1/)

A prompt that reads a content description and returns, for the UK and France, an age
rating, the hours the content may be shown, any other restrictions, the reasoning with the
rule behind each step, and anything a person needs to settle. The six numbered folders are
the six things the brief asked for, in order.

| Folder | What the brief asked for | What is in it |
|---|---|---|
| `1_sources/` | Sources, with links and scope | All 20 official sources, plus the documents themselves so any quote can be checked |
| `2_rules/` | A table of rules | 105 rules across 6 tabs, with a legend, the open questions, and a 24-hour chart of which rules bite when |
| `3_prompt/` | The full prompt | Two prompts, one that reads the content and one that decides, plus how to run them |
| `4_test_cases/` | At least three diverse test cases | Nine cases on real media, with the exact input text for each |
| `5_results/` | The results of the runs | What each run returned, what failed, and the prompt changes that came out of it |
| `6_design_choices/` | A short explanation of design choices | Seven choices and why, the limits, and the models and tools I used |

**Where it stands:** 105 rules, all 105 approved, every one carrying a quote from its source
that is checked against the stored document automatically. 20 of 20 sources collected. Eight
of nine cases run, with the saved model output for each.

### [`deliverables/task2/`](deliverables/task2/)

A written plan for scaling this to dozens of countries: collecting and validating sources,
organizing the rules, the shape of the solution, testing correctness, and measuring quality.
It includes the process diagram, a worked example of a single rule, the validation plan, the
success metrics, and which steps can be automated against which need a local expert.

---

## `out_of_scope/`

**Not part of the assignment.** [It has its own map](out_of_scope/README.md) explaining each
item.

The brief asked for artefacts and a written design. It did not ask for a working system. So
everything that produced those artefacts is here rather than at the top, including the
original copies that `deliverables/` is generated from.

| Item | What it is |
|---|---|
| `prompts/`, `rules/`, `sources/`, `tests/` | The originals the deliverable copies are made from |
| `TASK1_WRITEUP.md`, `TASK2_SCALING.md` | The originals of the two write-ups (Task 1: scope, design choices, tools) |
| `pipeline/` | 17 scripts that build the rules table, check it, and run a decision end to end |
| `scripts/` | A helper used to pick rules when running a test case by hand |
| `BUILD_rules_from_sources.md` | The prompt that turned each legal document into draft table rows |
| `docs/` | Generated pictures, already copied into the deliverables |
| `HOW_IT_WORKS.md` | A walkthrough of all 14 stages, if you want to see how a decision is actually made |

One thing could not move. `.github/workflows/` has to stay at the top of the repository or
GitHub stops running it. It is scaffolding like the rest, and it runs the scripts in
`out_of_scope/pipeline/`.

---

## The honest version

The rules table is the strong part: every rule is traceable to a quote from an official
document, and the build fails if a quote stops matching its source.

The weak part is judgment. 43 of the 105 rules turn on a threshold a person has to weigh,
such as whether something is justified by context, and only one decided case has been
collected to calibrate against. The prompt is built to send those to a human rather than
guess, which is the right behavior but is not the same as being right.

`out_of_scope/TASK1_WRITEUP.md` says where else the boundary sits, including jurisdiction, which is
a real gap and a deliberate one.
