# Results

Every run is saved in `runs/` as raw model output, so any claim here can be checked
against the file.

## Problem: it sent every decision to a person

The first run covered eight cases, run by agents that had never seen the project or the
expected answers. **17 of 17 decisions said "a person must check this."** That included a
cookery show where someone puts a plaster on a cut finger.

The cause: every rule in the table has a flag saying whether a person must sign off on it.
Two rules, plain definitions that apply to every program, had that flag set. So every program
ran into them and went to a person.

## Fix: unflag the two definitions, and tell the prompt which flag to read

The flag was cleared on the two definitions, since a definition cannot set an hour or a
rating. The decision prompt (`RUN_2_decide.md`) now says which flag decides:

> `human_review_required` says **whether a person must sign it off**. Escalate on this one.

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
