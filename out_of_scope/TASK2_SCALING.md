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
  rule. It shows where the regulator draws the line on a judgment rule. It is used twice: the
  model sees similar past decisions when it decides, and the decision becomes a test case.
- **Every rule carries a word-for-word quote, and a check compares it to the stored source.**
  If a quote stops matching, the build fails. This caught four bad rules the day real sources
  arrived.
- **Amendments are the main risk at scale.** A 2014 amendment quietly broadened a French
  category, and a rule built from the original text under-rated content. So: store the current
  consolidated text and note which instrument last amended it. Re-check each source on a
  schedule. A changed file sends every rule from that document back to unconfirmed. Then
  re-decide a sample of past decisions against the new text and see whether answers moved.
- **Contradictions are stored, not resolved.** Record both sources, rank them by authority,
  and send them to a person.
- **Translation is labeled.** Each rule records its quote's language. Reviewers can then see
  which quotes are translations.
- **A gap is reported as a gap.** France has no rule about alcohol in programs and the UK
  does. Silence for France must not read as approval.

## 2. Organizing the rules

One rules table, one row per sentence of law, fixed columns, plus the decisions table above.
Four choices matter:

- **Rating, hours and conditions are stored separately.** A rule can change the hours without
  changing the rating. Example: a film may air at any time if the channel has a PIN lock, and
  not before 9pm if it does not. The answer has to carry both.
- **A machine-readable form beside the quote.** Code acts on `not_before=22:00`. A lawyer
  reads the sentence.
- **A timeline app for lookup.** A 24-hour chart, built from the table, with a country and
  channel-type selector. It shows which rules apply at which hour, and each rule shows its
  quote. Someone can check "what applies at 21:30 on a free-to-air channel" without reading
  the table. It is rebuilt whenever the table changes, so it cannot go stale. Task 1 has a
  working version for two countries.
- **Dates on every rule.** Rules are closed with an end date, never deleted, so last year's
  decision can still be explained.
- **"How the rule applies" and "does a person review decisions that use it" are separate columns.** Merging
  them was the worst bug in Task 1: the system sent every decision to a human.

Fixed word lists are enforced by the build. In Task 1 a misspelled service type silently
dropped eight French rules.

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

Three levels: **country** (the rules), **program** (the description, written once and reused
for every country), and **channel**. The channel level is the one first drafts miss. The same
program can be legal on one channel and not another, because rules attach to the kind of
service, and in France each channel also has its own contract with the regulator, which can be
stricter than the general law. Each country is decided on its own, so one failing does not block the rest.

**Whose rules apply.** The system takes a country and applies that country's rules. That is
only right if the country is the one whose regulator covers the channel. Inside the EU, the
rules of the country where the **company** is based apply, and other EU countries accept them.
The UK mostly goes by whether the service is **available in the UK**. The input line naming
countries does not say which meaning it has, so the system silently picks one.

The fix is two tables. One lists, per channel, which regulator covers it, on what basis, and
who confirmed it. The other lists, per pair of countries, whether B accepts A's regulator.
Then apply exactly **one** country's rules, and refuse to decide if either table has no
confirmed answer. Do not apply "the stricter of the two" as a shortcut: usually only one
country's rules apply, and the stricter one pushes content later than the law requires. For Europe, a free public database called
MAVISE lists which country regulates each channel. There is no worldwide equivalent.

## 4. Validation plan

A test set written by the people who wrote the rules only tests whether the system agrees
with them. Truth sources, strongest first:

1. **Decided enforcement cases.** The regulator already ruled. Task 1 has exactly one, its
   biggest weakness.
2. **A local lawyer's written answer**, obtained before the system runs on the case.
3. **The broadcaster's own undisputed compliance decisions.**

Per country, cover each content area, each channel type, each rule with an exception, and at
least **two benign cases that must come back clear**. A test set of only difficult content
cannot notice a system that restricts everything. Task 1 ran that way until a cookery program
exposed a system that escalated every case. Run cases blind,
with people or agents who have not seen the expected answers.

## 5. Success metrics

The three kinds of error cost different amounts, so track them separately:

| Error | Cost |
|---|---|
| **Under-restricting:** cleared something the rule restricts | A regulatory breach |
| **Over-restricting:** restricted something the rule allows | Lost airtime, and nobody complains |
| **Escalating needlessly:** sent a clear case to a person | No work saved, and the system gets ignored |

Also track:
- **Escalation rate per country.** A country far above its neighbors usually has badly
  extracted rules, not a stricter law.
- **Reviewer overturn rate per rule.** The best signal for which rule to re-read.
- **Coverage:** the share of rule areas the test set exercises. A pass rate on a third of the
  table is not a pass rate.
- **Time since each source was last confirmed.**

To find where an error came from, give step two a hand-written correct description. If the
answer is still wrong, the fault is in the rules or prompt. If it is right, step one described
the program wrongly.

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

Everything mechanical can be automated. Every judgment threshold needs a person. Of Task 1's 105 rules,
45 turn on a judgment, and one decided case exists to calibrate them. Finding qualified
reviewers in each country is the real constraint, so start hiring before the engineering.

## Rollout

Start with **two countries, deep**, to build the controls (quote checking, amendment
detection, blind tests, the three error types), which are impossible to retrofit later. Then
**five countries in one legal family**, to test the rule structure without adding translation
and a new legal tradition at once. Add the jurisdiction tables before leaving the EU. Then
widen.

Measure the escalation rate from day one. A system that sends everything to a person is not
careful, it is not working.
