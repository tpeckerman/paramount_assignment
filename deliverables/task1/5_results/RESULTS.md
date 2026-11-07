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

## Fix: only send a case to a person when it matters

Added to the decision prompt (`RUN_2_decide.md`):

In plain words: the bar for human review went up. Before, any judgment rule in view sent the
case to a person. Now only a rule that actually changed the answer can. Two definitions in
the rules table also stopped asking for a person.

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
