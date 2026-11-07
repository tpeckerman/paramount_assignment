# Scaling to dozens of countries

**The question the system answers:** given a description of a TV program, when may it be shown
in country X, and under what conditions?

It works in two steps. Step one reads the description and writes down what happens, with
timecodes. Step two looks up each country's rules and decides: a rating if the country issues
one, the permitted hours, any other conditions, and the rule behind each step. Step one never
sees the rules, so it cannot shade its description toward the answer it expects. A working
version covers two countries and 105 rules.

**The claim this rests on:** most of the work is per country, not per program. Collecting a
country's rules and having a lawyer confirm them happens once, and again when the law changes.
Deciding on a program is cheap after that. Thirty countries means thirty times the setup, not
thirty times the running cost.

The process diagram is in `process_diagram.html`. Blue boxes are model steps, white boxes are
code, and black-bordered boxes are people.

## 1. Collecting and validating sources

- **Primary sources only:** the law, the regulator's binding rules, and its decided cases. A
  regulator's summary page is not the law. One French summary page stated a stricter rule than
  the binding text, and the rule built from it was wrong.
- **Every rule carries a word-for-word quote, and a check compares it to the stored source.**
  If a quote stops matching, the build fails. This caught four bad rules the day real sources
  arrived.
- **Amendments are the main risk at scale.** A 2014 amendment quietly broadened a French
  category, and a rule built from the original text under-rated content. So: store the current
  consolidated text and note which instrument last amended it. Re-check each source on a
  schedule by comparing a file fingerprint. A changed fingerprint means a person reads the
  difference, and every rule from that document goes back to unconfirmed. Then re-decide a
  sample of past decisions against the new text and see whether the answers moved.
- **Contradictions are stored, not resolved.** Record both sources, rank them by authority,
  and send them to a person.
- **Translation is labeled.** Each rule records the language of its quote. Machine translation
  can sort the work. A lawyer who reads the original language signs off.
- **A gap is reported as a gap.** France has no rule about alcohol in programs and the UK
  does. Silence for France must not read as approval.

## 2. Organizing the rules

One table, one row per sentence of law, fixed columns. Four choices matter:

- **Three separate answers:** rating, hours, and other conditions (such as a PIN lock). They
  can replace each other or stack. One rule lets a film air at any hour if a PIN lock is on.
  Reporting "any time" without the condition is dangerous. Reporting "barred until 9pm" while
  ignoring the lock costs the broadcaster a slot.
- **A machine-readable form beside the quote.** Code acts on `not_before=22:00`. A lawyer
  reads the sentence.
- **Dates on every rule.** Rules are closed with an end date, never deleted, so last year's
  decision can still be explained.
- **"How the rule applies" and "does a person sign it off" are separate columns.** Merging
  them was the worst bug in Task 1: the system sent every decision to a human.

Fixed word lists are enforced by the build. In Task 1 two spellings of one service type
silently dropped eight French rules from every decision.

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
status            approved
```

**Check.** The quote must appear character for character in the stored file.

**Sign off.** A French media lawyer confirms the reading and the 2014 change.

**Use.** A program with sustained violence on a general channel at 20:45 is barred, because
this rule sets 22:00 and the channel matches. The decision cites the rule id.

**Monitor.** If reviewers keep overturning decisions that rest on this rule, the threshold is
wrong and the rule goes back for re-reading.

## 3. Solution structure

Three levels: **country** (the rules), **program** (the description, written once and reused
for every country), and **channel**. The channel level is the one first drafts miss. The same
program can be legal on one channel and not another, because rules attach to the kind of
service, and in France each channel also has its own contract with the regulator, which can be
stricter than the general law. Each country is decided on its own. If France fails because a
source is down, the UK answer still returns, with France marked unavailable.

**Whose rules apply.** The system takes a country and applies that country's rules. That is
only right if the country is the one whose regulator covers the channel. Inside the EU, the
rules of the country where the **company** is based apply, and other EU countries accept them.
The UK mostly goes by whether the service is **available in the UK**. The input line naming
countries does not say which meaning it has, so the system silently picks one.

The fix is two tables. One lists, per channel, which regulator covers it, on what basis, and
who confirmed it. The other lists, per pair of countries, whether B accepts A's regulator.
Then apply exactly **one** country's rules, and refuse to decide if either table has no
confirmed answer. Do not apply "the stricter of the two" as a shortcut. Usually only one
country's rules were ever going to apply, so the stricter rule pushes content later than the
law requires, and nobody complains about that. For Europe, a free public database called
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
with a plaster on a cut finger exposed a system that escalated every case. Run cases blind,
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
| **Signing off a rule before it can decide anything** | **Local expert** |
| **Resolving two sources that disagree** | **Local expert** |
| **Confirming which regulator covers a channel** | **Local expert** |
| Final call on anything the system escalated | Compliance reviewer |

Everything mechanical can be automated. Every threshold needs a person. Of Task 1's 105 rules,
45 turn on a judgment, and one decided case exists to calibrate them. Finding qualified
reviewers in each country is the real constraint, so start hiring before the engineering.

## Rollout

1. **Two countries, deep.** Build the controls: quote checking, amendment detection, blind
   tests, the three error types. They are cheap now and impossible to retrofit later.
2. **Five countries in one legal family.** This tests the rule structure on a country it was
   not designed around, without adding translation and a new legal tradition at once.
3. **Add the jurisdiction tables** before leaving the EU.
4. **Then widen.**

The risk is not the model. It is a rule that is quietly wrong or missing, producing confident
answers nobody questions. Measure the escalation rate from day one: a system that sends
everything to a person is not careful, it is not working.
