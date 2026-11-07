# Age ratings and broadcast restrictions for linear television, UK and France

Take-home assignment, prompt engineer.

**103 rules, all 103 approved. 20 of 20 official sources collected.**

**All 103 approved rules carry a verbatim quote, and all 103 verify against their stored
source with 0 failing.** Coverage is enforced: an approved rule with no quote fails the build.

That was not always true. For most of this project the check reported "50 verified, 0 failed,
0 skipped", which read as full coverage and was not: 52 rules carried no quote and were never
shown to the check at all.

---

## The deliverables

### Task 1

| Asked for | Where | What is in it |
|---|---|---|
| **Sources and a table of rules** | [`sources/00_SOURCE_INVENTORY.md`](sources/00_SOURCE_INVENTORY.md) | All 20 sources with links, scope and link health |
| | [`sources/originals/`](sources/originals/) | The documents themselves, so every quote can be checked |
| | [`rules/RULES_TABLE_v1.xlsx`](rules/RULES_TABLE_v1.xlsx) | 103 rules across 6 tabs, with a readable legend and the open questions |
| | [`rules/csv/Rules.csv`](rules/csv/Rules.csv) | The same rules as plain text, for diffing and for code |
| **The full prompt** | [`prompts/BUILD_rules_from_sources.md`](prompts/BUILD_rules_from_sources.md) | Turns a law into rules. Run once per document |
| | [`prompts/RUN_1_describe_content.md`](prompts/RUN_1_describe_content.md) | Reads the content. Deliberately does not know the rules |
| | [`prompts/RUN_2_decide.md`](prompts/RUN_2_decide.md) | Applies the rules and decides. This is the one the brief asks for |
| **The test cases** | [`tests/CASES.md`](tests/CASES.md) | Five cases on real media, including a back-test against a decided regulator case |
| **The results of the runs** | [`tests/RESULTS.md`](tests/RESULTS.md) | What happened, the one failure, and the two bugs it exposed |
| **Design choices** | [`TASK1_WRITEUP.md`](TASK1_WRITEUP.md) | Seven choices and why, plus the limits |
| **Models and tools used** | [`TASK1_WRITEUP.md`](TASK1_WRITEUP.md) | Last section |

There are three prompts because reading the law and applying the law are kept apart on
purpose. That separation is what makes the quote check possible and what lets a wrong answer
be traced to either the content or the rules. [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md) explains
it with diagrams.

### Task 2

| Asked for | Where |
|---|---|
| The five questions, each as a numbered section | [`TASK2_SCALING.md`](TASK2_SCALING.md) |
| A process diagram | [`TASK2_SCALING.md`](TASK2_SCALING.md), "Process" |
| An example of how a single rule is represented | [`TASK2_SCALING.md`](TASK2_SCALING.md), "Deliverable: how a single rule is represented" |
| A validation plan | [`TASK2_SCALING.md`](TASK2_SCALING.md), section 4 |
| Success metrics | [`TASK2_SCALING.md`](TASK2_SCALING.md), section 5 |

**New to the repo?** [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md) has the diagrams and explains how a
content description becomes a decision.

**Supporting:** [`SCOPE.md`](SCOPE.md) why the boundary sits where it does ·
[`sources/99_EXTRACTION_NOTES_AND_LIMITS.md`](sources/99_EXTRACTION_NOTES_AND_LIMITS.md) the
limits in plain language · [`docs/timeline.html`](docs/timeline.html) a 24-hour view of which
rules bite when · `pipeline/` the tooling that produced and checks all of it.

---

## How it works, in one paragraph

Official documents are read **once** by a build prompt that turns each operative rule into a
table row carrying a verbatim quote. A separate run prompt reads a content description and
produces timecoded observations **without knowing the rules exist**, so it cannot shade its
descriptions toward an expected rating. Code then selects the rules that could apply, and a
second run prompt decides, citing a `rule_id` for every claim. Reading law and applying law
are kept apart, which is what makes the quote check possible, and that check caught four
defective quotes the moment real sources arrived.

Diagrams and a worked trace: [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md).

## Quick start

```bash
pip install openpyxl pypdf

python pipeline/verify_rules.py --with-quotes     # does the table hold up?
python pipeline/run_decision.py --countries UK FR --service free_to_air --categories violence
python pipeline/build_timeline.py                 # regenerate the 24-hour view
python pipeline/verify_cases.py                   # do the test cases' outcomes hold up?
python pipeline/render_answer.py decision.json    # the country-by-country answer table
```

## Scope

**Linear broadcast television only.** On-demand and streaming are a different regime in both
countries.

The task title says "age rating and broadcast time restrictions" but one requirement asks for
"other relevant broadcast restrictions", and that is a real question with a real answer. The
test used here: *does this restriction change, condition, or substitute for the age/time
answer?* That admits PIN gates, signage, warnings, adjacency limits, trailer handling and
quota caps, and excludes impartiality, fairness, privacy and commercial references. Reasoning
in [`SCOPE.md`](SCOPE.md).

## The findings that shaped the design

1. **The UK issues no per-programme age rating for linear TV.** The correct UK output is a
   scheduling verdict, not a number. France does have a graded rating. The two countries
   cannot share one decision path.

2. **Three axes, not two, and they are substitutes.** A rating, a set of hours, and a set of
   other restrictions. One rule reads `any_time; requires=mandatory_daytime_protection`;
   another disapplies the watershed entirely while that gate is in place. Report "any time"
   without the condition and you are wrong; report a bar without the available measure and you
   are wrong the other way. This is AVMSD art. 6a's mechanism: it mandates an outcome and
   permits scheduling **or** technical measures as alternatives.

3. **Hours follow service type.** French -16 is after 22:30 on ordinary channels and after
   20:30 on cinema and pay-per-view. A UK BBFC 18 film is barred before 21:00 on one service
   and permitted at any hour on another, purely because of a PIN. Ofcom says so itself: the
   Code "dispensed with these rules relating scheduling to ratings".

4. **The watershed is a ramp, not a gate.** Content starting after 21:00 must not open with
   its strongest material. A scheduler treating 21:00 as a threshold passes every clock check
   and still breaches.

5. **A decision is about a transmission, not a programme.** A `+1` service repeats the same
   file an hour later, moving content placed while children are at school into the time they
   are home. Identical file, different answer.

6. **The French -18 window lives in a different document** from the rest of the scheduling
   rules, and service eligibility gates it: on an ineligible channel it is a total
   prohibition and the hours are irrelevant.

7. **Some rules ignore the category entirely.** French art. 1 restricts violence between 06:00
   and 22:00 whatever category is assigned.

8. **Music videos are treated oppositely.** France exempts them from systematic signage with a
   soft preference; the UK applies the full watershed. Rendering the French preference as a
   prohibition is an over-rating defect.

9. **Three UK access concepts must not be conflated:** mandatory daytime protection (films,
   any hour), mandatory restricted access (adult sex material, 22:00 to 05:30 only), and no
   protection.

10. **Inputs a bare content description will not contain:** service type; access measures; the
    broadcast **date**, not just the time, since France has day-of-week and school-holiday
    rules and a regulator has treated a religious festival as raising the likely child
    audience; whether the asset is a theatrical film and its certificate; whether it is a
    trailer or a music video. When one is missing and a rule depends on it, the correct output
    is a missing-information flag, not an assumption.

11. **Absolute prohibitions are force-included in every decision slice**, whatever the
    content categories, and are checked first. They were being filtered by category like
    ordinary rules, so the extreme-violence ban only arrived if the content happened to be
    tagged `violence`. A rule absent from the slice is indistinguishable from one that did
    not apply. `UK-GEN-001`,
    `UK-SEX-001`, `UK-FLM-001`, `UK-FLM-006`, `FR-LAW-001`, `FR-PRO-001/002/003`.

## The honest caveat

I wrote the rules, the prompts, the tests and the checker, and executed them. Four roles that
should belong to at least two parties. The trustworthy results are the **failures**, since
those survived the bias rather than being produced by it. Bright-line rules need independent
re-derivation by someone who has not seen this table, which is conflict C-08.

The weakest part of the table is calibration: 35 of 103 rules are judgment-based and exactly
one decided case has been collected. That is an anchor, not a scale.

## Sources in scope

**UK** Broadcasting Code Sections One, Two, Three and Four; Ofcom guidance notes, which carry
the worked examples; the mandatory daytime protection statement; enforcement bulletins, the
only source of *applied* thresholds; Communications Act 2003 s.319; SI 2020/1062; BBFC as an
input for films.

**France** Arcom recommandation 2005-5 as amended by délibérations 2012-57 and 2014-17;
recommandation 2004-7 for category V; Loi 86-1067 art. 15; per-channel conventions, which can
be stricter and are not consolidated anywhere (C-06); CNC for theatrical films only.

**EU** AVMSD art. 6a, the common ancestor of both national frameworks.

**Ruled out** advertising codes, radio, on-demand regimes, and the Code sections that yield
neither a rating nor an hour. Note that the news section genuinely binds this broadcaster; it
is excluded because it produces neither output, not because it does not apply.
