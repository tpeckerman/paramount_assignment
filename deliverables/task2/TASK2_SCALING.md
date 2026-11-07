# Scaling to dozens of countries

**The question the system answers:** given a description of a TV program, when may it be shown
in country X, and under what conditions?

It works in two steps. Step one reads the description and writes down what happens, with
timecodes. Step two looks up each country's rules and decides: a rating if the country issues
one, the permitted hours, any other conditions, and the rule behind each step. Step one never
sees the rules, so it cannot shade its description toward the answer it expects. A working
version covers two countries and 105 rules.

**The claim this rests on:** most of the work is per country, not per program. Collecting a
country's rules and checking them against the source happens once, and again when the law changes.
Deciding on a program is cheap after that. Thirty countries means thirty times the setup, not
thirty times the running cost.

## How it flows

The diagram is in `process_diagram.html`. Blue boxes are model steps, white boxes are code,
and black-bordered boxes are people. There are two flows.

**When a law changes or a regulator publishes a decision**
1. A script notices that a source file changed, by comparing a fingerprint of the file. No
   model is needed.
2. A small, cheap model answers one question: does this change a rule or add a precedent? If
   not, it ends here.
3. If so, a model drafts the updated rule, or logs the decision. Code checks that every quote
   matches the source and every field is valid. No person signs off. The change goes live when
   the checks pass.
4. The rules table, the decisions table and the timeline update. Every cache row that used a
   changed rule or decision is deleted. A new country goes through this same flow.

**When a new program comes in**
1. Code splits it into segments at scene changes, about 10 minutes at most. Rules attach to
   moments (violence at 20:45), so one description of a two-hour program is too coarse. Short
   segments that repeat across episodes can also come straight from the cache. The program's
   answer is the most restrictive segment answer for each country.
2. A model watches each segment and writes a description with timecodes.
3. The description is embedded and compared with the cache using cosine similarity and
   ROUGE-L. Both must clear a high bar. On a match, the stored answer comes back.
4. With no match, code checks whether the description holds anything that needs checking, such
   as sex or violence. If not, the answer is "no restrictions found" and it ends.
5. If so, code gathers the relevant rules and similar past regulator decisions. A model says
   when the program can be shown, with its reasoning and a confidence score from 0 to 1.
6. If confidence is below X, a compliance reviewer decides. Set X by testing: start at 0.8 and
   move it until reviewers overturn few of the answers above the line.
7. The answer is stored in the cache with the rules and decisions it used. A row is deleted
   when any of them changes or is replaced.

## 1. Collecting and validating sources

- **Primary sources only:** the law, the regulator's binding rules, and its decisions. A
  regulator's summary page is not the law. One French summary page stated a stricter rule than
  the binding text, and the rule built from it was wrong.
- **Regulator decisions are a source too.** Each goes into a decisions table: what the content
  was, what the regulator ruled, and which rule it applied. A decision does not override a
  rule. 
- **Every rule carries a word-for-word quote, and a check compares it to the stored source.**
  If a quote stops matching, the build fails. This caught four bad rules the day real sources
  arrived.
- **Amendments are the main risk at scale.** A 2014 amendment quietly broadened a French
  category, and a rule built from the original text under-rated content. So: store the current
  consolidated text and note which instrument last amended it. Re-check each source on a
  schedule. A changed file means every rule from that document is re-checked. Then
  re-decide a sample of past decisions against the new text and see whether answers moved.
- **Contradictions are stored, not resolved.** Record both sources, rank them by authority,
  and send them to a person.
- **Translation is labeled.** Each rule records its quote's language. Reviewers can then see
  which quotes are translations.
- **A gap is reported as a gap.** France has no rule about alcohol in programs and the UK
  does. Silence for France must not read as approval.

## 2. Organizing the rules

One rules table, one row per sentence of law, fixed columns, plus the decisions table above.
The choices that matter:

- **Rating, hours and conditions are stored separately.** A rule can change the hours without
  changing the rating. Example: a film may air at any time if the channel has a PIN lock, and
  not before 9pm if it does not. The answer has to carry both.
- **Each rule is stored two ways.** The law's own sentence, for a person to check, and a
  short code such as `not_before=22:00` (do not show before 10pm), which the program can act on.
- **A timeline app for lookup.** A 24-hour chart, built from the table, with a country and
  channel-type selector. It shows which rules apply at which hour, and each rule shows its
  quote. See sample:
  https://github.com/tpeckerman/paramount_assignment/blob/main/deliverables/task1/2_rules/timeline.html
- **Dates on every rule.** Rules are closed with an end date, never deleted, so last year's
  decision can still be explained.
- **"How the rule applies" and "does a person review decisions that use it" are separate
  columns.** Merging them was the worst bug in Task 1: every decision went to a person.

## Worked example: one rule

**Collect.** The French regulator's recommendation, consolidated text, with a note that a 2014
instrument amended it.

**Extract.**

```
rule_id           FR-SCH-002
country           FR
service_type      free_to_air; other_than_cinema_channels
content_category  scheduling_general
classification    III_-12
time_rule_machine not_before=22:00
determinacy       bright_line
human_review      no
verbatim_quote    "Pour les autres services de television, ces programmes ne
                   doivent pas etre diffuses avant 22 heures."
source_doc        FR-R1c, art. 3
valid_from        2014-04-09
```

A rule goes live when it passes the automatic checks. Old rules are closed with an end
date, never deleted.

**Check.** The quote must appear character for character in the stored file.

**Use.** A program with sustained violence on a general channel at 20:45 is barred, because
this rule sets 22:00 and the channel matches. The decision cites the rule id.

**Monitor.** If reviewers keep overturning decisions that rest on this rule, the threshold is
wrong and the rule goes back for re-reading.

## 3. Solution structure

**What is shared across all countries, and what is specific to each?**

| Shared (built once) | Specific to each country |
|---|---|
| The two steps: describe the program, then decide | The rules, in the rules table |
| The prompts for both steps | The rating scheme (France has five categories, the UK has none per program) |
| The table's columns and fixed word lists | The channel types the rules attach to |
| The program description, written once and reused for every country | The regulator, its decisions, and its source documents |
| The checks, the cache and the review flow | The language of the sources, and the local expert |

Channel type belongs in the country column for a reason. The same program can be legal on
one channel and not another, because rules attach to the kind of service, and in France each
channel also has its own contract with the regulator, which can be stricter than the general
law. Each country is decided on its own, so one failing does not block the rest.

**Which decisions are made in the prompt, and which in code?**

| In the prompt (needs reading and judgment) | In code (same input, same output) |
|---|---|
| Describing what happens in the program | Fetching sources and spotting changes |
| Applying judgment rules to that description | Checking quotes, word lists and dates |
| Writing the reasoning and the confidence score | Choosing which rules to hand to the prompt |
| | Absolute bans, which nothing can override |
| | Checking every claim cites a real rule |
| | The cache lookup, and sending low-confidence cases to a person |
| | Which country's rules apply to a channel |

The last row matters. The system takes a country and applies that country's rules, which is
only right if that country's regulator covers the channel. Inside the EU, the rules of the
country where the **company** is based apply. The UK mostly goes by whether the service is
**available in the UK**. So code needs two lookups: per channel, which regulator covers it
and who confirmed it, and per pair of countries, whether B accepts A's regulator. Then apply
exactly **one** country's rules, and refuse to decide if either lookup has no confirmed
answer. Do not apply "the stricter of the two" as a shortcut, because usually only one
country's rules apply. For Europe, a free public database called MAVISE lists which country
regulates each channel. There is no worldwide equivalent.

## 4. Correctness testing

**How do we build a test set with approved answers?** Per country, cover each content area,
each channel type, each rule with an exception, and at least **two benign cases that must come
back clear**. A set of only difficult content cannot notice a system that restricts
everything. 

**Who approves the answers?** Never the person who wrote the rules. In order of strength:
1. **A decided enforcement case.** The regulator already ruled, so the answer is on record.
   Task 1 has exactly one, which is its biggest weakness.
2. **A local lawyer's written answer**, written before the system runs on the case.
3. **The broadcaster's own undisputed compliance decisions.**

**How do we stop the same error landing in both the solution and the answer?** Four rules:
- The lawyer writes the answer from the law itself, without seeing the rules table or the
  system's output.
- Run the cases blind: people or agents who have not seen the expected answers.
- When the system and the answer disagree, check the source law. Do not assume either is right.
- Have a second person re-derive the fixed rules (times, absolute bans) from the primary
  source and compare. Any difference is a finding about both.

## 5. Measurement and diagnosis

**How do we measure under-rating, over-rating and wrong hours?** Run the test set and count,
per country:

| Error | Count |
|---|---|
| **Under-rating** | Cases where the system gave a lower rating than the right answer. A breach |
| **Over-rating** | Cases where it gave a higher rating. Lost airtime |
| **Hours too early** | Cases where the earliest time is before the right time. A breach |
| **Hours too late** | Cases where the earliest time is after the right time, and by how many minutes. Lost airtime |

The UK has no rating per program, so UK answers are measured on hours and conditions only.

**How do we tell a content error from a rule error?** The two steps are tested separately.
- *Step two alone:* give it a hand-written correct description. If the answer is still wrong,
  the fault is in the rules or the prompt.
- *Step one alone:* give it a program with a known list of events. If events are missed or
  mislabeled, the fault is in the description.

Log every error as one of the two. A single error rate cannot tell them apart.

### Success metrics

Each is a number someone can compute from the test set or the logs. The targets are starting
points, to be reset after the first month of real use.

| Metric | How it is measured | Starting target |
|---|---|---|
| **Missed restrictions** | Of test cases where the right answer is "restricted," how many the system cleared | 0. Any miss blocks release |
| **Needless restrictions** | Of test cases where the right answer is "clear," how many the system restricted | Under 5% |
| **Cases sent to a person** | Share of all decisions that go to a reviewer, per country. Task 1's first run sent 100% | Under 15% |
| **Reviewer overturn rate** | Of the cases reviewers see, how many they change. Also re-check a random 2% of cases that skipped review | Under 5% |
| **Wrong cache answers** | Re-decide 2% of cache hits from scratch each month and count how many differ | Under 1% |
| **Rule update time** | Days from a regulator publishing a change to the table and cache updating | Under 1 business day |
| **Stale sources** | Sources not checked in the last 7 days | 0 |
| **Test coverage** | Share of content categories with at least 2 test cases. Task 1 covers 7 of 11 | 100% |

## What can be automated, and what needs a local expert

| Step | Who |
|---|---|
| Fetching sources, detecting changes | Automated |
| Quote check, word lists, dates, consistency | Automated |
| Selecting which rules could apply | Automated |
| Applying mechanical rules | Automated |
| Drafting rule rows from a legal document | Model, then a person |
| Describing a program | Model, then a person if borderline |
| **Deciding what a threshold means** | **Local expert** |
| **Confirming a translation is faithful** | **Local expert** |
| **Resolving two sources that disagree** | **Local expert** |
| **Confirming which regulator covers a channel** | **Local expert** |
| Final call on anything the system escalated | Compliance reviewer |

Everything mechanical can be automated. Every judgment threshold needs a person. Of Task 1's 105
rules, 45 turn on a judgment, and one decided case exists to calibrate them. Finding qualified
reviewers in each country is the real constraint, so start hiring before the engineering.
