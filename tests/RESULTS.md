# Results and failure analysis

## Discount these appropriately

I wrote the rules, the prompts and the test cases, and I executed them. Four roles that should
belong to at least two parties. A system graded by its own author passes.

So the trustworthy parts below are the **failures** and **TC-01**, because the failures
survived my bias rather than being produced by it, and TC-01 has an answer set by a regulator
rather than by me.

What limits the bias a little: every decision cites a `rule_id` resolving to a row with a
clause reference and a quote mechanically checked against the stored document. A reviewer can
audit any single claim without trusting me.

## Summary

| Case | Result | What it showed |
|---|---|---|
| TC-01 *Toofan* | **Pass, against a real finding** | Reproduced the regulator's outcome including the part that is counter-intuitive |
| TC-02 *Fury Road* free-to-air | Pass | Correct "no UK rating"; refused a single French answer |
| TC-03 same film, PIN | **Failed, then fixed** | Two real pipeline bugs. The valuable result |
| TC-04 *Thriller* + trailer | Pass | Separated the trailer from the parent asset |
| TC-05 contradictory doc | Pass | Surfaced the contradiction instead of resolving it |
| TC-06 *Step Brothers* | **Not run** | Rule selection verified; the decision has not been made |
| TC-07 *40-Year-Old Virgin* | **Not run** | As above. The TC-06 and TC-07 pair is the real measurement |
| TC-08 *Friends* at 14:30 | **Not run** | As above, and predicted to fail. See the end of this file |

The last three were added after the first five, because all five fail in the same direction:
each catches the system being too permissive. None of them can catch **over-rating**, where
the system is stricter than the law and nobody complains. TC-08 exists for that, and it is
the one I expect to fail.

---

## TC-01: Back-test against a decided case

The one case where the right answer is not my opinion. Ofcom's published finding on *Toofan*
(NTV, 29 May 2026, 11:30) is the benchmark.

**What the system produced:** breach of Rule 1.3, inappropriate scheduling. It cited
`UK-SCH-001` and `UK-SCH-002`, flagged the absence of any warning via `UK-WRN-003`, raised the
likely child audience on the festival date via `UK-SCH-011`, and treated the BBFC 15
certificate as evidence rather than as the answer via `UK-FLM-010`.

**It also got the part that is easy to miss.** Ofcom opened under the offence rule as well,
then dropped it: the violence was sufficiently contextualised within the film. The content was
defensible *as content*; only the slot was not. The system reported the same split, citing
`UK-CTX-011`.

That distinction is the whole argument for separating the axes. A pipeline that resolves
"justified by the context?" once and reuses the answer for both questions returns "no breach"
here, which is wrong, and wrong in the direction that gets a broadcaster fined.

**Caveat, stated plainly:** `UK-PRE-010` and `UK-CTX-011` were *extracted from this very
decision*. So this is not a clean hold-out test. It confirms the extraction is faithful and
the rules reach the engine; it does **not** prove the system would have reached that answer
without them. A genuine back-test needs decisions the table has never seen, which is C-07 and
the main outstanding work.

---

## TC-02: *Mad Max: Fury Road*, free-to-air

**UK:** `no_per_programme_rating`, with a scheduling verdict of not before 21:00
(`UK-SCH-002`). The BBFC 15 feeds the judgment but is not reported as the answer. Emitting
"15" here would invent an instrument that does not exist for UK linear TV.

**France:** the system refused to give one answer and branched by service type, which is
correct.

It also handled the theme-versus-depiction distinction: captivity and references to sexual
slavery are themes carrying weight under the harm rules, while **nothing sexual is depicted**.
A keyword-driven read tags this as sexual content and over-rates it.

---

## TC-03: Same film, premium service with PIN. **FAILED**

TC-02 and TC-03 contain **identical content**. Any system deriving hours from the rating must
answer them alike and must therefore be wrong about one.

The headline came out right: in the UK the watershed is *disapplied* while mandatory daytime
protection is in place (`UK-SCH-007`), so 14:30 is permissible. Two bugs underneath it.

### Bug 1: the rule defining the condition never arrived

`UK-ACC-001` defines mandatory restricted access as a gate that **cannot be removed by the
user**. It never reached the decision engine.

The engine selects rules by the content categories found in the description. `access_control`
is not a content category, because **a PIN is not content**. No content description ever
mentions one, so it was filtered out every time.

The engine could therefore read `any_time; requires=mandatory_daytime_protection` with no row
saying what that requirement meant. It would have accepted any claimed PIN, including a
parental control the viewer can switch off, which does not satisfy the rule and puts the
broadcast in breach from the first frame.

**Fix:** `access_control`, `audience_information` and `trailers` are force-included regardless
of content. The general lesson is bigger than the fix: **filtering rules by the categories
present in the content silently removes every rule about delivery.**

### Bug 2: two spellings of one service

After fixing Bug 1 the rule still did not arrive. The table used `premium_subscription` in one
row and `premium_subscription_film` in another for the same service, with no controlled
vocabulary, so the mismatch dropped it silently.

**Fix:** vocabulary normalised, and `verify_rules.py` now **fails** on any `service_type`
outside a controlled list.

### Why this is the result worth reading

Neither bug errored. Neither produced a visibly wrong answer. Both produced
**complete-looking output with a rule missing**, which is indistinguishable from correct
output until someone is in front of a regulator.

Both were found by one case built to have **no content difference** from another.

---

## TC-04: *Thriller* and its trailer

Two decisions, correctly separated. The video at 22:15 is post-watershed. The 30-second
trailer in a 15:00 break is judged **in its own slot** (`UK-TRL-002`, `UK-TRL-003`) and does
not inherit the video's permission, so the same footage is fine at 22:15 and a breach at
15:00.

The system also picked the right categories: this is `fear_distress` and horror imagery, not
`violence`. And it treated France more softly than the UK, which is correct, since France
exempts music videos from systematic signage with a soft preference while the UK applies the
full watershed. Rendering that French preference as a prohibition would be an over-rating
defect.

The on-screen occult disclaimer was recorded as a contextual factor rather than ignored.

---

## TC-05: Contradiction and missing information

The distributor's summary says "suitable for all audiences". The event list contains real
footage of a fatal accident.

The system reported the contradiction rather than resolving it, refused to answer France
without a service type and listed what each type would yield, and distinguished real footage
of death from dramatised violence. The "easy to copy at home" line was caught as an
imitable-behaviour trigger.

A confident answer here would be a failure even if the rating happened to be right.

---

## What the failures have in common

Every real defect in this project, in the rules, the pipeline and the sources, was **silent**:

- four quotes that were paraphrases or had punctuation added that cut a sentence short
- a rule citing guidance superseded in 2018
- a rule that could never reach the engine
- two spellings of one service name
- a manifest column deleted by a script that had never heard of it
- files on disk reported as missing because a lockfile was treated as proof
- three dead source URLs, each dead for a different reason, all labelled the same way

None was found by reading the work. All were found by a check comparing the work against
something external. **The checks are as much the deliverable as the table is.**

## A check that was measuring its own appetite

Worth separating from the list above, because it is not a defect in a rule but in a
**measurement**.

The quote check reported "50 verified, 0 failed, 0 skipped" throughout. That reads as full
coverage. It was not: "0 skipped" only ever meant no source document was missing from disk,
and rules carrying no quote were never looked at, because the check iterated the rules that
had one. 50 of 102. Six of the unchecked were the absolute prohibitions.

Found by a question about how an adult drama can air in the UK, not by any check.

All 46 have since been quoted from the stored sources: **coverage is 102 of 102, all
verifying**. The verifier now prints the denominator and treats coverage as a ratchet, so an
approved rule with no quote fails the build. Backfilling also surfaced a second source
misattribution, which only became visible once the quote existed to be checked.

## Limits

- **35 of 103 rules are judgment-based and barely calibrated.** One decided case is an anchor,
  not a scale. The guidance names about a dozen more; collecting them is the highest-value
  work left.
- **Author equals grader**, except for TC-01, which is itself not a clean hold-out.
- **The French rules are quoted from an official English translation** that states only the
  French is authentic.
- **Nothing has been run against a real Paramount asset**, only against descriptions I wrote.

---

## TC-06 to TC-08: specified, and only partly run

**Status, stated plainly: these three cases are written but the deciding step has not been
run on them.** What has been run is the part that is code. Reporting them as passes would be
exactly the failure the rest of this file is about.

### What was actually run

`pipeline/run_decision.py` was executed for the UK, free-to-air, with the content categories
these cases produce. That is step 11, rule selection, and it is deterministic, so the result
is a real result and not a judgement.

It selected 31 of 103 rules, and all three rules these cases turn on were among them:

| rule | clause | determinacy | what it does here |
|---|---|---|---|
| `UK-SEX-004` | Rule 1.20 | `conditional` | depicted intercourse, escape is a serious educational purpose only |
| `UK-SEX-003` | Rule 1.19 | `judgment_based` | strong or explicit sexual images or language, escape is context |
| `UK-NUD-001` | Rule 1.21 | `judgment_based` | nudity, escape is context |

That matters because the whole point of these cases is the difference between those escape
clauses, and a rule that never reaches the engine cannot be applied. TC-02 failed in exactly
that way: the rule was in the table and the selection step dropped it.

`UK-SEX-002` (Rule 1.18) was correctly **not** selected, being restricted to a service type
these cases do not use.

### What has not been run, and what it would show

The deciding step. Running it is what would answer whether the model treats "comedic" as a
single modifier it applies to all sexual content, which is the actual hypothesis under test:

- **TC-06 passes** if the answer is 21:00 citing Rule 1.20, with the comedy noted and
  discarded as irrelevant to that rule.
- **TC-07 passes** if the answer escalates to a person citing Rule 1.19, with the comedy
  presented as a live argument rather than settled either way.
- **TC-08 passes** if the answer is that 14:30 is fine, **and** it notices the +1 service.

The pair TC-06 and TC-07 is the real measurement. Getting either one alone proves nothing,
because a system that always says 21:00 passes TC-06, and a system that always escalates
passes TC-07. Only answering them **differently**, for the stated reason, shows the
distinction was understood.

### One prediction worth recording before the run

I expect **TC-08 to be the one that fails**, and for the system to push it to 21:00.

Every example in the prompts, and four of the first five test cases, are about content being
less suitable than it looks. Nothing in the material so far rewards clearing something. If
that prediction is right, the fix is not a prompt tweak but a test-set problem, and it is the
one described in section 5 of `TASK2_SCALING.md`: over-rating generates no complaints, so
nothing catches it unless a test is built to.

Recording the prediction first is deliberate. A prediction written after seeing the result is
worth nothing.
