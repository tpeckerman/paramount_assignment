# Scope, design choices, and tools

**Current state:** 105 rules, all approved, each with a word-for-word quote from its source. All 105 quotes verify against the stored documents. 20 of 20 sources collected. An approved rule with no quote fails the build.

## What goes in

A written description of what happens in a program, with timecodes. Not the video. Broadcasters already write compliance viewing notes, and Task 2 covers generating them.

## Scope

The brief asks for an age rating and the hours a program may be shown, plus "other relevant broadcast restrictions." I read that as: **include a rule if it changes, conditions, or replaces the age-and-hours answer.**

Reporting only age and hours would be wrong. One rule lets a film air at any hour if the channel has a PIN lock. Without the lock, the same film is barred before 9pm. A system that models only the clock either drops the condition (a dangerous answer) or misses that a lock lifts the ban (a lost slot). European law is built this way on purpose: it lets a broadcaster protect children by scheduling or by technical measures.

**Included:**
- PIN locks and similar access controls
- The earlier watershed on unprotected premium film channels
- The French on-screen age symbol
- Warnings shown to viewers
- Rules about what a program may sit next to in the schedule
- Trailers, which are judged in their own slot
- Yearly caps on late-night exceptions
- Which channels may show the most restricted category at all
- Exemptions, stored as real rules. A system that models only bans over-restricts, which costs airtime for no compliance gain.

**Excluded:** impartiality, accuracy, elections, fairness, privacy, and advertising. None produces a rating or an hour. Two are flagged because they are not fully clean:
- The news rules do bind this broadcaster. They are left out because they give no rating or hour. The system still has to ask "is this news?" or it will apply rules that do not bind.
- Advertising rules matter for a preschool brand, but they are a different workflow.

Of the UK rulebook, four sections are used: protecting under-eighteens, harm and offence, crime and hatred, and religion.

## The biggest limit: whose rules apply

The table says what the rules are for a channel regulated by the UK regulator or the French one. It does not say which a given channel is.

The two countries decide this in opposite ways. France, inside the EU, goes by where the **company** is based. The UK, outside it, mostly goes by where the service is **watched**. So "where is it watched" and "whose rules apply" are different questions. Answering needs facts about the company (where it is based, who licensed it), not the program.

**This table assumes you already know which regulator covers the channel.** Feed it a country because that is where the audience is, and it can answer confidently from the wrong rulebook. Designed in Task 2, not built (open question C-16).

## Design choices

**1. Two steps, not one.** Step one describes what happens. Step two applies the rules. Step one never sees the rules. A single step that knows both shades its description toward the answer it expects. Split, the description can be checked alone, and the decision can be re-run for another country without re-reading the program.

**2. Rules live in a table, not the prompt.** Adding a country means adding rows. A lawyer can check a rule without reading a prompt.

**3. Three answers, not one.** A country can restrict by rating, by hours, or by another requirement such as a PIN lock or on-screen symbol. These can replace each other and can stack.

**4. "How a rule applies" and "does a person sign it off" are separate columns.** They do not line up. Treating them as one was the worst bug here (see below).

**5. Every rule carries a quote, and a check compares it to the source.** If a quote stops matching, the build fails. It caught four bad rules the day real sources arrived, including two paraphrased from a government summary page instead of the law.

**6. "Not stated" is an answer.** The worst thing this system can do is decide confidently on a fact it was never given. Missing information is reported as missing and goes to a person.

## What testing changed

**The first full run sent 17 of 17 decisions to a human.** That included a cookery program where a presenter nicks a finger and puts on a plaster. No decision said when a program could air. The system saved nobody any work.

**The cause took several runs to find.** The prompt escalated whenever a rule it used was a judgement call. But rules that explain how to weigh things appear in every decision while deciding nothing themselves. Two were plain definitions, and neither can set an hour, a rating, or a condition. One appeared in 9 of the 17 escalations.

**Three changes followed.** The prompt now separates a rule it relied on from one it read and set aside. Those two definitions no longer demand a person. And the prompt escalates on the dedicated sign-off column.

**Result.** Six cases re-run blind, by agents with no knowledge of the project and no access to the expected answers. All six correct. The cookery program is clear in both countries with nobody needed, and the real enforcement case is still barred before 9pm. `tests/RESULTS.md` has both rounds.

## Known weaknesses

- **45 of 105 rules turn on a judgement, and only one decided enforcement case exists to calibrate them.** The table says a person must decide, not where the line sits. More decided cases are the highest-value work left.
- **I wrote the rules, prompts, and tests.** Blind runs remove the problem of knowing the expected answer. They do not remove it if my table misreads a rule, because a blind agent would repeat the misreading.
- **The French rules are quoted from an official English translation** that says only the French text is authentic. A French-qualified reviewer must re-check every one.
- **The category list has no middle ground.** A nicked finger and fatal-accident footage both fit badly.

## What a local expert should check

- Whether any French linear channel in the group still operates after the 2025 closure, and what kind of service it counts as.
- License conditions on the UK public-service channel that may go beyond the rulebook.

## Models and tools

- **Claude Opus 5** for research, reading sources, drafting rule rows, writing the code, and running test cases. Separate agents with no memory of the work ran the blind tests.
- **Python 3** with `openpyxl` (the table), `pypdf` (reading PDFs), and `unicodedata` (accent folding for French quote checks).
- **Scripts I wrote**, not a deliverable: a table builder, a quote checker, gates before and after the decision, a rule selector, source fetchers (one drives a browser for JavaScript pages), and diagram renderers.
- **GitHub Actions** runs every check on each push, so a broken quote fails before a reviewer sees it.
