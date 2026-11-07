# Review brief

Paste this, plus the assignment text, into a fresh session with the repo attached.

---

You are reviewing a take-home submission for a **Prompt Engineer** role. You have the
assignment and the repository. You do not have the conversation that produced it, which is
deliberate: if something only makes sense with that context, it is not finished.

## Before you read anything, run it

Most review effort gets spent reading prose and agreeing with it. The prose was written by the
same person as the code, so agreeing with it proves nothing. Run these first and report what
actually happened:

```bash
pip install openpyxl pypdf
python pipeline/verify_rules.py --with-quotes   # every rule quote vs its stored source
python pipeline/verify_cases.py                 # test-case claims, and stale numbers in prose
python pipeline/build_inventory.py --check      # is the source list current?
python pipeline/build_diagrams.py --check       # does the diagram render?
```

Then try to make them fail. Change a digit in a quote, point a rule at the wrong source,
edit a count in the README. **A check that cannot fail is decoration.** Report any that
passed when it should not have.

## The single most valuable thing you can do

The repo admits a problem it cannot fix itself, filed as **C-08**: the same person wrote the
rules, the tests and the checker, and ran them. Every passing test may be confirming a shared
misreading.

You are the only one who can break that. **Pick three to five `bright_line` rules. Derive them
yourself from the documents in `sources/originals/`, without reading the table first. Then
compare.** Where you disagree, treat it as a finding about both your reading and theirs.

This is worth more than every other question below.

## Does it answer what was asked

1. Is every Task 1 deliverable present: sources and a rules table, the prompt, test cases,
   results, design choices, models and tools? `README.md` claims a mapping. Follow each link
   and confirm the file contains what the map says.
2. Same for Task 2: five questions as sections, plus a process diagram, a single-rule example,
   a validation plan and success metrics.
3. Is anything claimed as a deliverable that is really something else?
4. Is the **scope decision** defensible? `SCOPE.md` argues for a boundary around "other
   relevant broadcast restrictions". Say if you would have drawn it elsewhere.

## Is it true

5. Spot-check rules against the stored documents. Does the quote support the rule as written,
   or only sit near it?
6. Is any obviously relevant official source missing?
7. Is the **three-axis model** right? The design claims classification, permitted hours and
   other restrictions are separate and substitute for each other. Much follows from this. If
   it is wrong, say so.
8. Are the test cases well chosen? Do they attack real failure modes or restate the rules?
   Two claim known real-world outcomes: check both.
9. The results. Are the conclusions supported by what was actually run? Note that three cases
   are marked **not run** rather than passed.

## The prompts

10. Read all three in `prompts/`. Would you change anything, and why?
11. **Try to break them.** They take a content description from an untrusted source and claim
    its contents are data, never instructions. Write a hostile description that tries to get a
    permissive answer: embedded commands, a fake pre-approval, a claim the rules changed,
    contradictory metadata. The guard has never been tested. Report what works.
12. Are they as concise as they can be without losing accuracy? Examples are long on purpose,
    since they encode real defects. Say if that trade is wrong.

## Is it sound engineering

13. Does every script run? Any broken links anywhere?
14. Anything hardcoded that belongs in `pipeline/constants.py`?
15. Is the code written sensibly: real errors instead of bare asserts, exit codes that
    propagate, no silent failures?
16. **Scope creep.** Sixteen Python files is a lot for a prompt-engineering exercise. The
    README argues each earns its place. Do you agree? Name what you would delete.
17. Is every file necessary? What would you cut?

## Is it readable

18. Could someone who knows a little about technology and can use GitHub follow this? Where
    did you get lost?
19. Are the diagram's steps comprehensive, and does it match the written walkthrough?
20. Are the documents concise, or padded?
21. Any contradictions between files? Numbers, claims, or a diagram that disagrees with the
    prose describing it.

## Is it honest

This one matters most after the re-derivation.

22. **Is anything stated as done that is only designed?** Look for a plan written in the
    present tense. The repo marks some things as not built; check those marks are accurate and
    complete.
23. Known limitations are filed as conflicts `C-05` to `C-08` and `C-16`, in the
    `Open_Questions` tab of the rules table, with more in the limitations sections of
    `TASK1_WRITEUP.md` and `sources/99_EXTRACTION_NOTES_AND_LIMITS.md`. Two questions:
    are they honestly stated, and **what is wrong that is not on that list?** The second is
    the one worth your time.
24. Does any number in prose disagree with the data? There is a check for this; find what it
    misses.

## How to report

Lead with the **three most serious problems**, worst first, each with the file, what is wrong,
and what it would cost if nobody noticed. Then the rest.

Separately: **what is the weakest part of this submission**, and would you advance this
candidate? Answer both plainly. A review that only lists small fixes has not been useful.
