# Defects found by running the prompts

These came out of running the prompts against the test cases, by agents that had never seen
the expected answers. Reading a prompt does not find them.

Only the ones that changed an answer, or would have, are listed. Small schema annoyances were
cut from this list; they are not what a reviewer needs.

Background: the work happens in two steps. **Step one** reads the programme and writes down
what happens in it. **Step two** takes that list, applies the rules, and decides. Step one
never sees the rules, so it cannot shade its description toward an answer it expects.

---

# Fixed

## 1. A PIN lock had nowhere to go

One test case says the channel has a PIN that is on by default and that the viewer cannot
switch off. Step one had no box for it, so the fact survived only as a sentence in a notes
field.

This is the most dangerous kind of miss. A lock like that is what turns "not before 9pm" into
"any time of day", so losing it produces an answer **more permissive than the law allows**,
with nothing flagged.

**Fixed.** Step one now records whether a lock exists, what kind, whether it is on by default,
whether the viewer can turn it off, and the exact words used. The last two are separate
questions on purpose: a lock the viewer can switch off is not the same protection as one they
cannot, and only the second counts.

## 2. No way to tell a time of day from a running time

`00:11:33` can mean eleven hours into a film or half past eleven in the morning. Nothing said
which.

**Which one matters: the time of day.** Every hour rule is written about the clock on the
wall. The watershed is 9pm, not "ninety minutes in".

**Why both get recorded anyway.** Step one is handed whichever the source used, and
descriptions usually count from the start of the programme. You cannot reach a time of day
without knowing which kind of number you were given, plus when the programme starts.

**Fixed, in two halves.** Step one marks each event as a time of day or a running time, and
copies the number exactly. It does no arithmetic, deliberately. Step two then converts and
applies the rules to the time of day.

The first attempt only did the first half: step one recorded it and step two never looked.
That went unnoticed because the one real enforcement case already had times of day in it. On a
programme counted from zero it would have applied an hour rule to the wrong number. A scene 90
minutes into a programme starting at 8pm goes out at 9:30pm, past the watershed. Read as a
running time it looks like 1:30am.

## 3. Two different signals for "a human must check this", and no rule saying which wins

The rules table has two columns. One says **how** a rule applies: mechanically, or only once
you confirm a condition, or by weighing a judgement. The other says **whether a person must
sign it off**. They do not line up, and the prompt only ever mentioned the first.

Escalating on the first sends everything to a human, because rules that describe how to weigh
things are present in every single decision while deciding nothing themselves. That is exactly
what happened: 17 decisions out of 17 went to a person, including a cookery programme with a
plaster on a cut finger.

**Fixed.** The prompt now says the sign-off column governs, and explains why the two differ.
Found independently by a blind run, which followed the second column and flagged that the
prompt never said which to use.

## 4. One box asked two questions at once

A field called `treatment` was used both for *was this shown on screen* and for *how was it
played*. One case has characters joking explicitly about sex with nothing shown. It is both
comic and not shown, and only one value fit, so information was thrown away and the prompt
left the choice to chance.

**Fixed.** A separate yes/no field for "was it shown" already existed, so the conflicting value
was removed. `treatment` records framing only.

## 5. A rule that could never be retrieved

Rules are fetched by matching what is in the programme **and** what kind of channel it is. One
French rule had "per channel" written in the channel column. That is not a kind of channel, it
is a note meaning "applies to each one individually", so it failed every channel test and
dropped out of every selection ever made.

The rule matters: it is the one saying each French channel signs its own contract with the
regulator, which **can be stricter than the general law**.

**Fixed.** Corrected to all linear television, which is what it binds.

---

# Not fixed, and why

## 6. The category list has no middle ground

Every event must be filed under one of fifteen labels, and the prompt says never to invent a
new one. Two real events have nowhere sensible to go.

A presenter nicking a finger, with a plaster and no blood, is not violence and not serious
harm. A blind run filed it under **violence**, which is the nearest word and badly wrong: it
pushes a trivial event into the category most likely to restrict a programme.

Worse in the other direction, real footage of a fatal accident gets filed under **serious
harm** — which is correct, and which then retrieves only the absolute bans, because those are
the rules that carry that label. The graduated violence rules, the ones that would actually
decide the hour, never arrive. Real death footage ends up measured against a ban it cannot
meet and against nothing in between.

**Why not fixed.** This needs new labels, and labels are how rules are retrieved. Adding one
changes which rules reach every future decision, so it is a change to the table's retrieval
design rather than a word added to a list. Doing it properly means working out the missing
tiers across both countries, not patching the two cases that exposed it.

## 7. Nothing defines what "COUNTRIES: UK, FR" means

Every description ends with a line naming countries, and nothing anywhere says what the line
refers to. It could be where the programme will be shown, where it was made, or where the
rights were sold.

The system reads it as "apply these countries' rules". That is the *country of destination*
answer, and it is exactly the answer France does not use. France goes by where the **company**
is based: a French-regulated channel showing a program in the UK follows French rules. So a
system that reads `UK` off that line and reaches for the UK rulebook has **chosen** a
jurisdiction rather than been told one, and it will do so confidently and silently.

**Why not fixed, and where it is handled.** Fixing it properly is not a label change. It needs
two things the system does not have: a record of which regulator covers each channel, and a
grid of whether each country accepts another country's regulator. Neither can be read off a
description of a programme, which is the only input this system takes.

This is written up as the jurisdiction section of the Task 2 proposal, including the two
tables, the free European database that supplies most of the first one, and the warning that
applying the stricter of two countries' rules is usually the wrong instinct because usually
only one country's rules were ever going to apply. Tracked as open question C-16.

## 8. Step one is banned from using obvious evidence

Step one must never work out whether a programme is news, or made for children, from its genre.
So a cookery show records "unknown" for both, and step two then has to branch or flag a
question nobody would seriously ask.

**Why not fixed, on purpose.** The whole value of step one is that it describes without
judging. Let it reason from genre and it will start shading descriptions toward the answer it
expects, which is the failure the two-step design exists to prevent, and it would be invisible
when it happened.

The right fix is narrow: allow it only where the answer is genuinely not in doubt. That line
needs drawing carefully, and drawing it hastily to make one test case pass would trade a
visible nuisance for an invisible bias.

---

## What this says about the prompts

The prompts were careful about the **reasoning** and loose about the **containers**. Almost
every defect here is a box that cannot hold what the programme contains, or two boxes
disagreeing about which question they answer. None was visible from reading. All of it
surfaced on the first run.
