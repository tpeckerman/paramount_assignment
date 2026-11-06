# Test results and failure analysis

## How these were run, and why you should discount them

I wrote the prompts, the rules table, the test cases **and** I am the model that executed
them. That is four roles that should belong to at least two parties. A system graded by its
own author will pass.

So the honest reading of what follows: the parts worth trusting are the ones where something
**failed**, because those survived my bias rather than being produced by it. The parts where
the system succeeded should be re-run by someone else before anyone believes them.

What limits that bias a little: every decision cites a `rule_id` that resolves to a row with a
clause reference and a verbatim quote that has been mechanically checked against the stored
source document. So a reviewer can audit any single claim without trusting me. That is the
point of the architecture, not a nice extra.

---

## Summary

| Case | Result | What it exposed |
|---|---|---|
| TC-01 | Pass | Correct UK "no rating" answer; correctly refused one French answer |
| TC-02 | **Failed, then fixed** | Two real pipeline bugs. Detail below — this is the valuable one |
| TC-03 | Pass | Caught the rule with no depicted content, escalated rather than banned |
| TC-04 | Pass | Separated the trailer from its parent asset |
| TC-05 | Pass | Surfaced the contradiction instead of resolving it |

One case out of five failed. It failed in two different ways, both of which were invisible
defects that produced **complete-looking output with a rule silently missing**.

---

## TC-01 — Cinema film on free-to-air

**UK.** Classification: `no_per_programme_rating`. This is the correct and slightly
counter-intuitive answer — UK linear television has no per-programme age rating. Scheduling:
not before 21:00 (`UK-SCH-002`). The BBFC 15 certificate is *evidence* feeding the
film-carryover rules, not an answer; reporting "15" as the UK rating would invent a
regulatory instrument that does not exist.

**France.** The system refused to give one answer and branched by service type, which is
correct. On a general channel the drug and violence content points to category III with its
own hours; on a cinema or pay-per-view service the hours differ.

**Both.** The heroin scene produced **two** observations — the drug rule and an
imitable-behaviour rule, because the technique is shown in close-up. Merging them into one
"drugs" observation loses a rule hit. The suicide scene was correctly *not* over-read: no
method is depicted, which matters because the relevant rule turns on method depiction.

---

## TC-02 — Identical film, premium service with a PIN — **FAILED**

This case exists because TC-01 and TC-02 have **identical content**. Any system that derives
hours from the rating must give them the same answer and must therefore be wrong about one.

The system got the headline right: in the UK the watershed is *disapplied* while mandatory
daytime protection is in place (`UK-SCH-007`), so a 14:30 transmission is permissible. But
two bugs underneath it:

### Bug 1 — the rule that defines the condition never arrived

`UK-ACC-001` defines what "mandatory restricted access" actually means: a gate that
**cannot be removed by the user**. It never reached the decision engine.

The cause: the engine selects rules by the content categories found in the description.
`access_control` is not a content category. **No content description ever mentions a PIN,
because a PIN is not content.** So it was filtered out every single time.

The engine could therefore read `any_time; requires=mandatory_daytime_protection` with no row
telling it what that requirement means or how to tell whether it is met. It would have
accepted *any* claimed PIN — including a parental control the viewer can switch off, which
does not satisfy the rule and would put the broadcast in breach from the first frame.

**Fix:** `access_control`, `audience_information` and `trailers` are now force-included
regardless of content. The general lesson is bigger than the fix: **filtering rules by the
categories present in the content silently removes every rule about delivery.**

### Bug 2 — two spellings of the same service

After fixing Bug 1 the rule *still* did not arrive. The rules use `premium_subscription` in
one place and `premium_subscription_film` in another for the same service. There was no
controlled vocabulary, so the mismatch dropped the rule silently.

**Fix:** vocabulary normalised, and the verifier now **fails** on any `service_type` token
outside a controlled list, so this cannot recur quietly.

### Why this is the most important result here

Neither bug produced an error. Neither produced a visibly wrong answer. Both produced
**complete-looking output with a rule missing**, which is the worst failure mode a compliance
system has: it is indistinguishable from correct output until someone is in front of a
regulator.

Both were found by one test case that was deliberately built to have *no content difference*
from another.

---

## TC-03 — Comedy sketch mocking a religion

No violence, no sex, no drugs, no strong language. A category-driven pipeline scores this
clean and returns "no restrictions".

The system instead fired `UK-HAT-002` (abusive or derogatory treatment of a religion or
community) and flagged it for human review. That is the right answer twice over:

- The trigger is **treatment**, not depicted subject matter. Nothing in the event list is
  "content" in the usual sense.
- It **escalated rather than refused**. Comedy and satire have real protection, and the rule
  is context-justified. A system that cleared this is wrong; a system that banned it is also
  wrong.

This rule was added only after the scoping test was corrected. Before that correction the
system returned "no restrictions" for this case.

---

## TC-04 — Music video and its trailer

Two decisions, correctly separated. The video at 22:15 is post-watershed. The 30-second
trailer in a 15:00 break is judged **in its own slot** (`UK-TRL-002`) and does not inherit
the video's permission — so the same audio that is fine at 22:15 is a breach at 15:00, with
no change to the material.

A pipeline that reasons about "the asset" rather than each transmission misses this entirely.

---

## TC-05 — Contradiction and missing information

The distributor's summary says "suitable for all audiences, no content of concern". The event
list contains real footage of a fatal accident.

The system reported the contradiction rather than resolving it, which is the required
behaviour: the extraction stage is explicitly forbidden from tidying conflicts, because a
tidied description hides the disagreement from the only parties who can settle it.

It also refused to answer France at all without a service type, listing what each service type
would yield instead. And it distinguished real footage of death from dramatised violence,
which engage different rules.

**A confident answer here would be a failure even if the rating were right.**

---

## What the failures have in common

Every real defect found today — in the rules, in the pipeline, and in the sources — was
**silent**. Nothing crashed. Nothing looked wrong:

- four quotes that were paraphrases or had invented punctuation
- a rule citing guidance superseded in 2018
- a rule that could never reach the engine
- two spellings of one service name
- a manifest column deleted by a script that had never heard of it
- files on disk reported as missing because a lockfile was treated as proof

None was found by reading the work. All were found by a mechanical check that compares the
work against something external. **The checks are the deliverable as much as the table is.**

---

## Honest limits

- **28 of 90 rules are judgment-based and essentially uncalibrated.** The table can say "a
  judgment is required here"; it cannot say where the line sits. Only one enforcement
  precedent has been collected. The regulator's guidance notes contain worked examples that
  would calibrate these, and 8 of 20 sources are still not collected.
- **Author equals grader.** See the top of this page.
- **French sources are translations.** The category V rules are quoted from Arcom's own
  English translation, which states that only the French is authentic.
- **Nothing here has been tested on real Paramount assets**, only on cases I wrote. Written
  test cases share the blind spots of whoever wrote them.
