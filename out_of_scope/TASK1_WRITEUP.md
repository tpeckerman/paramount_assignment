# Design choices, and the tools used

**Current state:** 105 rules, all approved, each carrying a word-for-word quote from its
source. All 105 quotes verify against the stored documents, 0 failing. 20 of 20 sources
collected. An approved rule with no quote fails the build.

## What goes in

A written description of what happens in a program, with timecodes. Not the video.

Watching the video is a real problem and a different one, so pretending to solve it here
would be dishonest. In practice a broadcaster already has this description: compliance
viewing notes exist for exactly this purpose. Task 2 covers what it would take to generate
them.

---

## The design choices

**1. Two steps, not one.** Step one reads the program and writes down what happens. Step two
applies the rules and decides. Step one never sees the rules.

This is the most important choice here. A single step that knows both will unconsciously
shade its description toward the answer it expects, calling something "mild" because mild is
the rating it has in mind. Splitting them means the description can be checked on its own,
and the decision can be re-run against different countries without re-reading the program.

**2. Compile the rules once, look them up many times.** The rules live in a table, not in the
prompt. Adding a country means adding rows, not rewriting instructions. It also means a
lawyer can check a rule without reading any prompt.

**3. Three answers, not one.** A country can restrict a program by rating it, by limiting the
hours, or by requiring something else such as a PIN lock or an on-screen symbol. These are
independent, they can replace each other, and they can stack.

One rule permits a film **at any hour** provided a PIN lock is in place. Report "any time"
without the condition and you have given a dangerous answer. Report "barred until 9pm" without
the available lock and you have cost the broadcaster a slot it was entitled to use. A system
that models only rating and hours cannot express either.

**4. "How a rule applies" and "does a person sign it off" are separate columns.** They do not
line up: some rules need a person because confirming a condition is an operational fact
nobody in the pipeline can check, and some judgement rules need nobody because the judgement
they describe feeds another rule rather than deciding anything.

Treating them as one column was the worst bug in this project. See below.

**5. Every rule carries a word-for-word quote, and a check compares it to the source.** If a
quote stops matching, the build fails. This is the cheapest control here and it caught four
bad rules the day real sources arrived, including two that turned out to be paraphrased from
a government summary page rather than the law.

**6. Scope by what a rule does, not by what it is about.** A rule belongs in this system if it
changes, conditions, or replaces the age-and-hours answer. That test lets in things that are
not about time on their face, such as a PIN lock or an on-screen symbol, and keeps out whole
sections of the rulebook that produce no rating and no hour. `SCOPE.md` sets out the boundary.

**7. "Not stated" is an answer, not a failure.** The most consequential thing this system can
do is decide confidently on a fact it was never given. Missing information is reported as
missing and routes to a person.

---

## What testing changed

The brief asks for an improvement made as a result of testing. There were several; this is
the one that mattered.

**The first full run escalated 17 decisions out of 17.** Every answer went to a human,
including a cookery program where a presenter nicks a finger and puts on a plaster. Not one
decision stated when the program could be shown. Every individual answer was defensible and
the system as a whole was useless, because it saved nobody any work.

**The cause took three rounds to find.** The decision prompt escalated whenever a rule it
relied on was marked as a judgement. But rules that describe *how to weigh things* are
present in every single decision while deciding nothing themselves, so this escalated
everything by construction. Two of them were plain definitions: one about how audience size
affects context, one about deciding two questions separately. Neither can set an hour, fix a
rating or impose a condition. One of them appeared in 9 of the 17 escalations while being
incapable of changing any of them.

**Three changes followed.** The prompt now distinguishes a rule it *relied on* from a rule it
*read and set aside*. Those two definitions no longer demand a person. And the prompt now
escalates on the dedicated sign-off column rather than on how a rule applies.

**The result.** Six cases re-run blind, by agents with no knowledge of this project and no
access to the expected answers. All six correct. The cookery program comes back clear in both
countries with nobody needed, and the real enforcement case still catches, still barred before
9pm.

`tests/RESULTS.md` has all four rounds and what each one changed.

---

## Known weaknesses

- **45 of 105 rules turn on a judgement, and one decided enforcement case exists to
  calibrate them.** The table can say "a person must decide" but not where the line sits.
  Collecting more decided cases is the highest-value work left.
- **I wrote the rules, the prompts and the tests.** The blind runs remove the half of that
  problem that comes from knowing the intended answer. They do not remove the other half: a
  misreading in my table is one a blind agent would faithfully reproduce.
- **The French rules are quoted from an official English translation** which itself says only
  the French is authentic. A French-qualified reviewer must re-check every one.
- **The system assumes you already know which regulator covers the channel.** The two
  countries decide that in opposite ways. Hand it a country because that is where the
  audience is and it will answer confidently from the wrong rulebook. Designed in Task 2, not
  built.
- **The category list has no middle ground.** A nicked finger and real fatal-accident footage
  both land in labels that fit badly, and labels are how rules get retrieved.

---

## Models and tools

**Claude Opus 5** for research, reading sources, drafting rule rows, writing the pipeline
code, and running the test cases. Separate agents with no memory of the work for the blind
test rounds and for independently verifying downloaded files.

**Python 3**, with `openpyxl` for the table, `pypdf` for reading PDFs, and `unicodedata` for
the accent folding the French quote checks need.

**Scripts I wrote**, which are not a deliverable and live outside the deliverable folders: a
table builder, so rules are generated from one source rather than hand-edited where a change
leaves no diff; a quote checker; gates either side of the decision; a rule selector; fetchers
for the source documents including one that drives a browser for pages built by JavaScript;
and renderers for the diagrams and the 24-hour chart.

**GitHub Actions** runs every check on each push, so a broken quote or a stale number fails
before it reaches a reviewer.
