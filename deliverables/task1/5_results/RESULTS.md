# Results

Four rounds of running the prompts. Each round: what came back, what was wrong with it, and
what changed as a result.

Every run is committed in `runs/` as the raw model output, so any claim here can be
checked against the file rather than taken on my word.

Background: the work happens in two steps. **Step one** reads the program and writes down
what happens in it. **Step two** applies the rules and decides. Step one never sees the
rules, so it cannot shade its description toward an answer it expects.

---

## Round 1: it escalated everything

Eight cases, run by agents that had never seen this project or the expected answers.

**Result: 17 decisions out of 17 said "a human must check this".** Not one gave an answer.
The field for *when the program may be shown* came back empty every single time, including
for a cookery show where someone nicks a finger and puts a plaster on it.

Every individual answer was defensible. The system as a whole was useless, because it saved
nobody any work.

### What was wrong

**1. A PIN lock had nowhere to go.** One case says the channel has a PIN that is on by
default and that the viewer cannot switch off. Step one had no box for it, so the fact
survived only as a sentence in a notes field.

This is the most dangerous kind of miss. A lock like that turns "not before 9pm" into "any
time of day", so losing it produces an answer **more permissive than the law allows**, with
nothing flagged.

**2. No way to tell a time of day from a running time.** `00:11:33` can mean eleven hours
into a film or half past eleven in the morning. Nothing said which. For the one real
enforcement case in the set, that distinction is the entire question.

**3. One box asked two questions.** A field called `treatment` held both *was this shown* and
*how was it played*. One case has characters joking explicitly about sex with nothing shown.
It is both comic and not shown, only one value fit, so information was thrown away and the
prompt left the choice to chance.

**4. A repeat channel invited arithmetic the prompt elsewhere banned.** One instruction
mentioned that some channels rebroadcast an hour later, inviting step one to turn 14:30 into
15:30. Another said never to adjust a time.

### What changed

- Step one gained a section for access controls: whether a lock exists, what kind, whether it
  is on by default, whether the viewer can remove it, and the exact words used. The last two
  are separate questions, because a lock the viewer can switch off is not the same protection
  as one they cannot.
- Every event now records whether its timecode is a time of day or a running time.
- `treatment` records framing only. A separate yes/no field already answered "was it shown",
  so the conflicting value was removed.
- Step one records the broadcast as given and notes that a repeat channel may exist. The
  arithmetic is step two's job, where there is a rule for it.
- The deciding prompt gained a rule separating *a rule you relied on* from *a rule you read
  and set aside*, so that a judgement rule merely present in the slice no longer escalates.

---

## Round 2: the clock fix was half wrong

Two cases re-run to check round 1's changes.

**Result: the access-control fix worked.** The PIN reached the decision as structured data.

**What was wrong.** The clock field had been put on the broadcast rather than on each event.
Those genuinely differ: a program starting at 14:30 whose scenes are counted from zero has a
clock start time and running-time scene markers. One field said both and therefore said
neither.

**What changed.** The field moved onto the event. A third run confirmed it.

---

## Round 3: it answered, but I knew the answers

Five cases, run by me. **This round does not count as evidence**, because I had read the
expected answers first. It was a check that the rules and prompts *can* reach the right
answer, not that they do so unaided.

**Result: all five correct, and every decision stated hours.** Zero empty answers, against 17
of 17 in round 1.

### What was wrong

**Two definitions were forcing every UK decision to escalate.** One says bigger audiences
need more justification; the other says to decide two questions separately. Neither can set
an hour, fix a rating, or impose a condition. Both were nonetheless marked "a person must
check this".

A definition applies to **every** decision in its country. So a sign-off flag on one escalates
everything, whatever the content. One of them appeared in 9 of the 17 round-1 escalations
while being incapable of changing any of them.

**I hedged twice in my own outputs**, and a checker caught both: claiming high confidence
while listing missing facts that would change the answer.

### What changed

- Both definitions no longer demand a person. A lens on how to read a rule is not itself a
  decision.
- A new check stops any definition from demanding sign-off again.

---

## Round 4: blind, and it held

Six cases, run by three separate agents with no memory of this project, barred from reading
the expected answers or this file.

**Result: all six match.** Including the two that matter most.

| Case | Result |
|---|---|
| Cookery show, plaster on a finger | **Clear in both countries, no human needed** |
| Music video at 22:15 | **Permitted, no human needed** |
| Its trailer at 15:00 | Barred, escalates |
| Film, free-to-air | Barred before 9pm; France branched by channel type |
| Documentary contradicting itself | Escalates, low confidence |
| Sitcom, after-sex scene at 2:30pm | **Fine at 2:30pm, no human needed** |

The cookery show is the one that settles it. An agent that did not know it was supposed to
come back clear cleared it anyway. The escalate-everything problem is fixed, not
fixed-because-the-author-knew-the-answer.

The music video is the strongest single result: permitted on one bright-line rule, with every
judgement rule in the slice read and explicitly set aside.

### What was wrong

**1. Two different signals for "a human must check this", and no rule saying which wins.**
The table has two columns: one says *how* a rule applies, the other says *whether a person
must sign off*. They do not line up, and the prompt only ever mentioned the first. Escalating
on that one sends everything to a person, because rules describing how to weigh things appear
in every decision while deciding nothing themselves. **This was the root cause of round 1.**

**2. A rule that could never be retrieved.** Rules are fetched by matching what is in the
program *and* what kind of channel it is. One French rule had "per channel" in the channel
column, which is not a kind of channel, so it failed every channel test and dropped out of
every selection ever made. It is the rule saying each French channel signs its own contract
with the regulator, **which can be stricter than the general law**.

**3. Two French age categories had an hour but no definition.** Three rules said when -16
content may air. Nothing said what makes a program -16. Two agents independently reported the
branch as undecidable, correctly, since the prompt forbids citing a rule it was not given.

**4. The UK answer "no rating exists" is true and unquotable.** The prompt requires it, and
separately requires a rule behind every claim. No rule says it, because it is an **absence**:
there is no sentence in the Code asserting it.

### What changed

- The prompt now says the sign-off column governs, and explains why the two differ.
- The French rule's channel field corrected. It now reaches decisions.
- Definitions added for both missing categories, built from the stored French text with
  verified quotes. 105 rules.
- The UK rating value is now exempt from needing a citation, with the reason stated. **No rule
  was invented for it.** A row in this table means a quote from a source, and manufacturing
  one for a structural fact would put an unquotable claim behind the same seal as 102 quoted
  ones. Recorded as open question C-19 instead.

---

## Left open on purpose

**The category list has no middle ground.** Every event must be filed under one of fifteen
labels and the prompt forbids inventing new ones. A nicked finger is not violence and not
serious harm; a blind agent filed it under **violence**, the nearest word, which pushes a
trivial event into the most restrictive bucket. Worse the other way: real fatal-accident
footage files under **serious harm**, which then retrieves only the absolute bans and never
the graduated violence rules that would actually set the hour.

Not fixed because labels are how rules are retrieved. Adding one changes what reaches every
future decision, so it is a change to the table's retrieval design, not a word added to a
list.

**Nothing defines what the countries line in an input means.** Every description ends with a
line naming countries and nothing says what it refers to: where it will be shown, where it
was made, or where the rights sit. The system reads it as "apply these countries' rules",
which is the *country of destination* answer and exactly the one France does not use. France
goes by where the **company** is based. So the system **chooses** a jurisdiction rather than
being told one, confidently and silently.

Not fixable here: it needs a record of which regulator covers each channel, and a grid of
which countries accept which others' regulators. Neither can be read off a description of a
program. Written up in the Task 2 proposal, tracked as C-16.

**Step one is banned from using obvious evidence.** It must never infer from genre whether a
program is news or made for children, so a cookery show records "unknown" for both.

Left deliberately. The value of step one is that it describes without judging. Let it reason
from genre and it will shade descriptions toward the answer it expects, which is the failure
the two-step design prevents, and it would be invisible when it happened. The right fix is a
narrow exception, and drawing that line hastily to pass one test would trade a visible
nuisance for an invisible bias.

---

## What this does not show

Six blind cases prove the system can tell restricted content from benign. They do not measure
how well.

The cases touch 7 of the 11 content areas that have rules, so any pass rate is a pass rate on
two thirds of the table.

And the blind runs remove only half the correlated-error problem. They were separate agents
with no memory of this work, not a separate model, and I wrote the rules they applied. A
misreading in my table is one they would faithfully reproduce. That is C-08, and only an
independent re-derivation closes it.
