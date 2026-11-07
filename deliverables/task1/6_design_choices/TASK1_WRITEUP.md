# Task 1, Design choices, and the tools used

Everything the assignment asks for, with the reasoning. Where a choice was wrong and got
changed, the original is stated rather than quietly replaced, the corrections are the most
informative part of this.

| Deliverable | Where |
|---|---|
| Sources and rule table | `sources/00_SOURCE_INVENTORY.md`, `2_rules/RULES_TABLE_v1.xlsx`, `2_rules/RULES_TABLE_v1.xlsx` |
| The prompt | `prompts/RUN_1_describe_content.md`, `prompts/RUN_2_decide.md` |
| *Not a deliverable for either task:* the prompt that builds the table | the rule-building prompt (repository only; not a deliverable). Task 1 asks for a table, not a method of making one; Task 2 asks for a design, not a working prompt. This is apparatus |
| Test cases and results | `tests/CASES.md`, `tests/RESULTS.md` |
| Scope reasoning | the scope note in Task 1's design-choices folder |
| Design choices and tools | this file |

**Current state:** 105 rules, all 105 approved, 20 of 20 sources collected. All 103 carry a verbatim
quote and all 103 verify, 0 failing. Coverage is enforced: an approved rule with no quote
fails the build (C-15).

---

## What the prompt takes in, and why there is no video step

Requirement 2 sets the interface: the prompt "accepts a content description including events
and timecodes". Requirement 3 asks for test cases built from "short videos, music videos, or
any content available to you to run with the prompt".

Read together: a video is where a test case **comes from**; the description is what **runs**.
Writing that description is the tester's job, done once per case, and the test cases here are
built from real identifiable content rather than invented titles so a reviewer can check the
descriptions against the works.

Two reasons beyond the requirement for drawing the boundary there.

**Broadcasters already produce this artifact.** Compliance viewing notes and as-run logs are
standard practice. The description is not a workaround for lacking video understanding; it is
the document that already exists in the workflow this would slot into.

**It would be the least verifiable link in the chain.** Every other step here can be checked
against something external: a rule against its source document, a decision against a cited
rule. A model's reading of a video can only be checked by a human watching it, which is the
cost the system exists to reduce.

### Where the hard part actually is

The natural assumption is that classification is a judgment call and the rules are the easy
part. It is closer to the reverse.

| | Deterministic? | Example |
|---|---|---|
| Deciding **what is in** the content | **No.** This is where the judgment lives. | Is this violence "presented repeatedly"? Is this treatment "derogatory"? Is the method "easily imitable"? |
| Applying rules **once that is settled** | **Largely yes.** 33 of 105 rules are bright lines. | Category V airs 00:00 to 05:00. R18 never airs. The watershed is 21:00, or 20:00 on an unprotected premium film service. |

The rule-application half is close to a lookup, which is why most of the effort here went into
making the table correct and checkable rather than into prompt wording.

The characterisation half is hard in a way that does not look hard. "Two teenagers share a
cigarette, played for laughs" and "a character smokes" are different inputs to the same rule
and yield different answers.

Splitting the stages puts the judgment in one place where it can be tested and escalated, and
leaves the other half nearly mechanical. It is also what makes the extractor's blindness to
the rules possible, which matters because an extractor that knows the thresholds decides the
outcome through word choice before any rule is applied.

## Which steps this task covers

All fourteen steps in the repository walkthrough belong to Task 1. Steps 1 to 4 produce the sources
and the rule table; steps 8 to 12 are the prompt.

The checks are the exception: nothing in Task 1 asks for them. It exists because
Task 2 asks how you know the rules are right, and that question needs a mechanical answer
rather than an assurance. It then paid for itself inside Task 1 by catching four defective
quotes and a rule citing the wrong document.

## Design choice 1, Two stages, not one

**Chosen:** RUN 1 turns the description into timecoded observations. RUN 2 applies rules.
RUN 1 **does not know the rules exist.**

A single prompt doing both is smaller and cheaper. It is also unauditable: there is nothing
separating "what the rule says" from "what I decided", so a misreading cannot be caught. And
an extractor that knows the thresholds will shade its descriptions toward the rating it
expects, write "graphic violence" rather than "a man is struck with a bottle; blood is
visible" and the decision is already made, invisibly, by an adjective.

**Cost:** two calls, and RUN 1 sometimes produces observations no rule uses. That turned
out to be a feature. An observation matching no rule is a **coverage gap**, which is how you
discover a missing rule.

## Design choice 2, Compile the rules once, query them many times

**Chosen:** source documents → rules table → decisions read the table.

The alternative is feeding regulatory text to the model per decision. That re-reads the law
thousands of times, re-derives it slightly differently each time, and leaves no citation that
resolves to anything. Here a rule is read once, checked once, signed off once. Updating a rule
is a row edit with a provenance trail. The decision context is roughly 5× smaller than the
source corpus, and that corpus is still only 12 of 20 documents, so the real ratio is far
higher.

**Cost:** the table can go stale. That is why the currency gate and the amendment tracking
exist, and they exist because this failure happened twice.

## Design choice 3, Three output axes, not two

The assignment warns against assuming age rating implies broadcast hours. The warning
understates it. There are **three** outputs and they are **substitutes**:

```
UK-FLM-003   Rule 1.24   any_time; requires=mandatory_daytime_protection
UK-SCH-007   Rule 1.4    the watershed does not apply while that gate is in place
```

Permitted at any hour, weekday afternoons included, *provided* a PIN gate is on by default.
Report "any time" and you dropped the condition that earned it. Report "barred before 21:00"
and you missed that a technical measure lifts it. **Wrong in both directions.**

This is not a quirk. The EU framework requires an *outcome* and permits scheduling **or**
technical measures as alternatives, so any country implementing it will show the same shape.

## Design choice 4, Determinacy and ambiguity are separate fields

`determinacy` describes the rule: bright line, conditional, or judgment. `ambiguity_flag`
describes my extraction: clear, conflicting, translation-uncertain, unverified.

Merging them loses the most useful state: *this rule is perfectly crisp and I am not confident
I captured it correctly.* Scoring uses the first; usability uses the second.

## Design choice 5, Every claim carries a verbatim quote

The single highest-value decision. Each rule stores a quote that must appear
character-for-character in the stored source, checked mechanically.

The moment real sources landed, it failed four rules. Two were paraphrases I had written as
quotes. One cited the wrong document. The fourth is the one worth remembering: it ended
`"...post-0530."` with a full stop **I had added**, cutting the sentence before the words
"which cannot be removed by the user", the exact words that make the rule enforceable. A
truncated clause dressed as a complete sentence.

I could not have found any of these by re-reading my own work.

## Design choice 6, Scope by escape clause, not by keyword

I first scoped the Broadcasting Code by searching for one phrase and concluded seven of ten
sections were irrelevant. That was wrong. Section Three enters through a different door: its
rules are permitted "except where it is justified by the context", and *context* is a defined
term whose third factor is **the time of broadcast**.

A single lexical test is not a scoping method. The corrected test enumerates the escape
clauses. Sections Five to Eight use "editorially justified", which does **not** import the
context definition and so never turns on the hour, verified against the live text, not
assumed.

**Scope boundary:** this tool covers the age/time decision and anything that conditions or
substitutes for it. It stays silent on impartiality, fairness, privacy and commercial
compliance. The news section still binds this broadcaster, it is excluded because it yields
no rating and no hour, not because it does not apply, and it is retained as a *router*, since
news is regulated elsewhere and applying a harm rule to it would be wrong.

## Design choice 7, "Not stated" is an output, not a failure

The worst outcome is a confident decision on absent information. `not_stated` is a
first-class value and RUN 2 is forbidden from resolving it by assumption, it branches and
labels instead. Service type is the critical one: French hours depend on it, so a single
unqualified French answer is almost always wrong.

---

## Failure analysis, and the improvements I can demonstrate

Two rounds of this. The first came from the rule-selection code, the second from running the
prompts for real against all eight cases.

### Improvement 2, from running the prompts: a fact with nowhere to live

The eight cases were run by agents that had **never seen the expected answers**. They were
given the prompt and the input and nothing else. That matters, because an author running
their own tests cannot find this class of defect: they already know what the output should
say, so prose that happens to contain the right words looks like success.

**What the first run exposed.** TC-03 describes `mandatory PIN, enabled by default, cannot
be disabled by the subscriber`. The RUN 1 output schema had **nowhere to put it**. Not on
the asset, not on the transmission. So it survived only as prose, folded into
`intended_service` and a notes field.

That is the most outcome-changing fact a description can carry. A gate of that kind is what
turns `not before 21:00` into `any time` under `UK-FLM-003`. Buried in prose, a decision step
that reads fields cannot see it, and the answer comes back **more permissive than the law
allows** with nothing flagged. It is the only defect found in this whole project that fails
in that direction.

The same run found a second one: TC-01's timecodes are times of day, taken from a
regulator's finding about a broadcast, while the schema implies elapsed time from the start
of the program. Nothing recorded which. In TC-01 that distinction is the entire case.

**The change.** `prompts/RUN_1_describe_content.md` gained an `access_control` block on the
transmission with five fields, a `clock` field, and the two rules explaining why each exists.

**The re-run, which found my fix was half wrong.** A second blind agent reported that
`access_control` now worked, and that `clock` did not: it sat on the transmission but
described timecodes, and in TC-03 the two differ. The events are elapsed, the 14:30 start is
a time of day, and one field cannot say both. It also noted that padding `00:08` to
`00:08:00` turns eight minutes into eight seconds.

**The second change.** `timecode_clock` moved onto the observation where it belongs,
`start_time` is now defined as always a time of day, timecodes are copied exactly as
written, and two more field-less facts got fields: `warning_or_signposting` and
`calendar_context`. Both were in the same category as the PIN, both outcome-bearing, and
both had been surviving in a notes field.

**The third run confirmed it.** On TC-01 every observation carries `wall_clock`; on TC-03
they carry `elapsed` beside a 14:30 wall-clock start; the PIN is in fields and nowhere else;
the absent warning and the Eid date are both captured; and `00:08` is stored unpadded. The
agent's words were that the schema expressed both cases "correctly and without strain".

**What the pattern says.** Every defect in this round was a container problem, not a
reasoning problem: a field that could not hold what the content said, or two facts sharing
one slot. The prompts were careful about *how to think* and loose about *where to put the
answer*. Reading them again would never have found it. Running them found it immediately,
and the full list is in `tests/PROMPT_DEFECTS.md`.

### Improvement 1, from rule selection: two bugs from one case

TC-01 and TC-02 are the same film with **identical content** on different services. Any
system deriving hours from the rating must answer both alike, and must therefore be wrong
about one.

**Bug 1. The rule defining the condition never reached the engine.** `UK-ACC-001` defines
"mandatory restricted access" as a gate that *cannot be removed by the user*. The engine
selects rules by the content categories present in the description. `access_control` is not a
content category, because **a PIN is not content**. So it was filtered out every time. The
engine would read `requires=mandatory_daytime_protection` with no row saying what that meant,
and would have accepted a parental control the viewer can switch off, a breach from the
first frame.

*Fix:* `access_control`, `audience_information` and `trailers` are force-included regardless
of content. The lesson is larger than the fix: **filtering rules by content categories
silently removes every rule about delivery.**

**Bug 2, two spellings of one service.** After that fix the rule still did not arrive.
`premium_subscription` in one row, `premium_subscription_film` in another, no controlled
vocabulary, rule silently dropped.

*Fix:* vocabulary normalized, and the verifier now **fails** on any unknown `service_type`.

**Why this matters more than a passing test:** neither bug errored. Neither produced a
visibly wrong answer. Both produced complete-looking output with a rule missing, which is
indistinguishable from correct output until someone is in front of a regulator.

---

## Known weaknesses

- **45 of 105 rules are judgment-based and uncalibrated.** This is the weakest part of the
  table. Exactly one decided enforcement case has been collected, so the table can say "a
  human must decide" but cannot say where the line sits. The guidance names roughly twelve
  more enforcement bulletins; collecting them is the highest-value work left (C-07).
- **Author equals grader.** I wrote the rules, prompts, tests and checker, and executed them.
  The failures are the trustworthy part. Bright-line rules need independent re-derivation by
  someone who has not seen the table (C-08).
- **French rules are quoted from an official English translation** that states only the French
  is authentic. A French-qualified reviewer has to re-check every one.
- **Channel-level agreements not collected.** In France these can be stricter than the law.
  One rule records that the agreements exist and bind; what they say is still unknown (C-06).
- **The table never says which channels it applies to.** Before you can use a country's
  rules you have to know that country's regulator actually covers the channel, and the two
  countries here decide that in opposite ways: France by where the company is based, the UK
  mainly by where the service is available. No rule in the table is wrong because of this,
  but the table assumes a precondition it never states. Recorded as C-16, and the boundary is
  now written down in the scope note in Task 1's design-choices folder.
- **The `superseded` path is untested.** The versioning mechanism is written and no rule has
  yet travelled through it, because no source has been amended during this project.

---

## Models and tools

**Claude Opus 5**, research, source analysis, rule extraction, pipeline code, and executing
the test cases. One sub-agent run for independent verification of 22 downloaded files, used
specifically because my own substring matching had already produced two false positives.

**Python 3**, `openpyxl` (table), `pypdf` (PDF extraction), `csv`/`json`, `unicodedata` for
the accent and ligature folding the French quote checks need.

**Scripts I wrote to do the work.** These are not a deliverable and are not in the
deliverables folders; they live in the repository. Described by what they do rather than by
filename, since the filenames are not the point:

- a **table builder**, so the rules are generated from one source rather than hand-edited in
  a spreadsheet where a change leaves no diff
- a **quote checker**, which compares every rule's quote against the stored document
  character for character, and now also compares the hours in a row against the hours its
  quote contains. It found four defective quotes the day real sources arrived
- **gates either side of the decision**: one that stops the run before a model is asked
  anything it cannot settle, one that rejects a citation to a rule that does not resolve or
  was never supplied
- a **prompt assembler**, which filters the table to the rules that could apply and wraps
  them in the delimiters the decision prompt declares
- **fetchers** for the source documents, including a Playwright one for pages drawn by
  JavaScript, and an importer for pages a person saved from a browser
- **renderers** for the source inventory, the 24-hour chart and the process diagram

**GitHub Actions**, running the schema check, the quote check, the test-claim check, the
diagram render, and a regenerate-and-diff of the CSV so the binary table cannot drift
unnoticed. One workflow; an earlier claim here that a second one fetches sources was wrong,
and there is no such workflow.

**Removed:** a Colab notebook that converted the table to a Google Sheet. Its integrity
checks had become a weaker, drifting copy of the quote checker, it referred to rule statuses
that no longer occur, nothing ran it so nothing caught the drift, and it carried a hardcoded
Drive folder id. Its one idea worth keeping, closing out rules from a replaced document, is
now real code.

**Not used, deliberately:** no attempt to defeat Cloudflare or AWS WAF challenges. Blocked
documents were listed for manual retrieval instead, with a console snippet that verifies each
save contains the phrase identifying the real document.
