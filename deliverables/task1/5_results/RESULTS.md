# Results

Every run is saved in `runs/` as raw model output, so any claim here can be checked
against the file.

## Problem: it sent every decision to a human

The first run covered eight cases, run by agents that had never seen the project or the
expected answers. **17 of 17 decisions said "a human must check this."** None said when the
program could be shown, including a cookery show where someone puts a plaster on a cut
finger.

The cause: the prompt escalated whenever a rule it used was a judgment call. But rules that
explain how to weigh things appear in every decision while deciding nothing themselves, so
every decision escalated.

## Fix: escalate on what changed the answer, and on the sign-off column

Added to the decision prompt (`RUN_2_decide.md`):

> **Decide who signs off, using `human_review_required`, not `determinacy`.**

> **`rules_checked_not_triggered`** is for a rule you read and set aside, with one line
> saying what was missing.
> **Escalate on what is in `basis`**, not on what you were handed.

Two plain definitions in the rules table also stopped demanding a person, since neither can
set an hour, a rating or a condition.

## Result: six cases re-run blind, all correct

Three agents with no memory of the project, barred from the expected answers.

| Case | Result |
|---|---|
| Cookery show, plaster on a finger | Clear in both countries, no human needed |
| Music video at 22:15 | Permitted, no human needed |
| Its trailer at 15:00 | Barred, escalates |
| Film, free-to-air | Barred before 9pm; France branched by channel type |
| Documentary contradicting itself | Escalates, low confidence |
| Sitcom, after-sex scene at 2:30pm | Fine at 2:30pm, no human needed |

## Limits

The cases touch 7 of 11 content areas, so a pass rate is a pass rate on those seven. I wrote
the rules the agents applied, so a misreading in my table is one they would repeat.
