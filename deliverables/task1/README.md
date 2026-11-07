# Task 1 deliverables

| Asked for | Where |
|---|---|
| Sources and a table of rules | `1_sources/` (with links and scope), `2_rules/RULES_TABLE_v1.xlsx` |
| The full prompt | `3_prompt/`: `RUN_1` describes the content, `RUN_2` decides |
| The test cases | `4_test_cases/CASES.md`, with each input alone in `inputs/` |
| The results of the runs | `5_results/RESULTS.md`, with the raw model outputs in `runs/`. `FIRST_RUN_ALL_ESCALATED.md` summarizes the first run, where every decision went to a person |
| Design choices, and models and tools used | `6_design_choices/TASK1_WRITEUP.md` |

Extra, not asked for: `2_rules/timeline.html`, a 24-hour view of which rules apply when, built from the table.

**Start with** `5_results/RESULTS.md`. It records what the runs got wrong, not only what they got right.

## Glossary (for readers outside broadcasting)

| Term | Meaning |
|---|---|
| Linear TV | Scheduled channels watched live. On-demand and streaming are out of scope. |
| Free-to-air | A channel anyone can receive without paying. |
| Pay / premium channel | A subscription channel. Different rules can apply, for example if it has a PIN lock. |
| `+1` channel | A channel that repeats another channel's output an hour later. Each showing is its own decision. |
| Watershed | The UK 9pm line. Before it, content must suit children. After it, stronger material is allowed. |
| Ofcom | The UK broadcast regulator. Its Broadcasting Code is the main UK rulebook. |
| Arcom | The French broadcast regulator. It sorts programs into five categories (I to V) with hours for each. |
| BBFC | The UK film classifier (ratings such as 15). It does not rate TV programs. |
| PIN lock | A parental-control code. It can replace a time restriction. |
| Escalate | Send the case to a human compliance reviewer. |
| Blind run | A test run by an agent that has not seen the expected answer. |
