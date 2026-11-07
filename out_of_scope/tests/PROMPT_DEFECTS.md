# Defects found by running the prompts

These came out of running the prompts against the test cases, by agents that had never seen
the expected answers. Reading a prompt does not find these. None was visible to the person who
wrote it.

The runs are in `tests/runs/`.

**Five of nine are fixed.** Each entry says what went wrong, and either what the fix was or
why it has been left alone.

Background, for anyone who has not read the prompts: the work happens in two steps. Step one
reads the programme and writes down what happens in it, as a structured list. Step two takes
that list, applies the rules, and decides. Step one never sees the rules, so it cannot shade
its description toward an answer it expects. Most defects below are **container** problems in
step one: a box that cannot hold what the programme actually contains.

---

## 1. Nowhere to record a PIN lock. FIXED.

**What went wrong.** One test case says the channel has a PIN that is on by default and that
the viewer cannot switch off. Step one had no box for it, so the fact survived only as a
sentence in a notes field.

That is the most dangerous kind of miss. A lock like that is what turns "not before 9pm" into
"any time of day", so losing it produces an answer *more* permissive than the law allows, with
nothing flagged.

**The fix.** Step one now has a dedicated section recording whether a lock exists, what kind,
whether it is on by default, whether the viewer can turn it off, and the exact words used. The
last two are separate questions on purpose: a lock the viewer can switch off is not the same
protection as one they cannot, and only the second counts.

## 2. One box asked two questions at once. FIXED.

**What went wrong.** A field called `treatment` was used both for *was this shown on screen*
and for *how was it played*. One test case has characters joking explicitly about sex without
anything being shown. It is both comic and not shown, and only one value fits. Information had
to be thrown away and the prompt left the choice to chance.

The prompt contradicted itself: one instruction said the field marks things only spoken about,
the next said it records framing.

**The fix.** There was already a separate yes/no field for whether something was shown, so the
"not shown" value was duplicated as well as conflicting. Removed it. `treatment` now records
framing only, and the two instructions each own one question.

## 3. No way to tell a time of day from a running time. FIXED.

**What went wrong.** `00:11:33` can mean eleven hours into a film, or half past eleven in the
morning. Nothing recorded which.

For the real enforcement case in the test set, that distinction is the entire question. The
regulator ruled on violence going out at 11:33 on a weekday morning, not eleven hours into a
movie.

**Which one actually matters.** The time of day. Every hour rule is written about the clock
on the wall: the watershed is 9pm, not "ninety minutes in".

**So why record both.** Because the describing step is given whichever the source used, and
descriptions usually count from the start of the programme. You cannot get to the time of day
without knowing which kind of number you were handed, plus what time the programme starts.

**The fix, in two halves.** Step one now marks every event as either a time of day or a
running time, and copies the number exactly as given. It does no arithmetic, deliberately: it
is the step that must not interpret anything.

Step two then converts. It adds a running time to the start time to get the time of day, and
applies the rules to that. A scene 90 minutes into a programme starting at 8pm goes out at
9:30pm, on the far side of the watershed from the programme's own start. If the start time is
unknown the conversion is impossible, and that is reported as missing information rather than
guessed.

**This was caught late.** The first version of the fix only did the first half. Step one
recorded the distinction carefully and step two never looked at it, so the information was
collected and then ignored. It happened to work on the one real enforcement case because that
case's timecodes were already times of day. On a case counted from zero it would have applied
an hour rule to the wrong number.

The prompt also now forbids padding a timecode, because turning `00:08` into `00:08:00`
silently converts eight minutes into eight seconds.

## 4. Two lists disagreed about what a documentary is. FIXED.

**What went wrong.** The list of programme types had no entry for a documentary, so one became
"other". The framing list *did* have "documentary". The two disagreed about whether documentary
is a kind of programme or a way of filming.

**The fix.** It is a kind of programme. Added to the programme-type list, removed from the
framing list.

## 5. A repeat channel invited arithmetic the prompt elsewhere forbids. FIXED.

**What went wrong.** Some channels rebroadcast everything an hour later. One instruction
mentioned this, which invited step one to work out that 14:30 becomes 15:30. Another said
never to adjust a time. Both applied and they pointed opposite ways.

**The fix.** Step one records the broadcast exactly as given and notes that a repeat channel
may exist. Working out what the later slot means is step two's job, where there is a rule for
it. Step one no longer does arithmetic.

---

# Left alone, and why

## 6. An event cannot say which broadcast it belongs to. NOT FIXED.

One test case is a music video at 22:15 plus a 30-second trailer cut from it going out at
15:00. Two slots, two different answers. Events carry no marker saying which they came from,
so the link exists only in prose. Their timecodes collide too, because both start at 00:00.

**Why not.** One extra field would do it. But exactly one case out of nine has two broadcasts,
and reshaping the output to suit a single example is how a system gets tuned to its own test
set instead of to the job. This wants two or three more multi-broadcast cases first, so the
field is designed against a pattern rather than one instance.

## 7. "There is none" and "nobody said" are stored the same way. NOT FIXED.

"Certificate: none" is someone answering the question. "Service: not stated" is nobody
answering it. Both end up recorded as absence, so the system asks a human about a question
that has already been answered.

**Why not.** Low cost and low risk, but it touches several fields at once and every one feeds
the decision step. Worth doing deliberately rather than squeezing it in beside changes that
affect whether answers come out right.

## 8. Step one is forbidden from using obvious evidence. NOT FIXED, ON PURPOSE.

Step one must never work out whether a programme is news, or made for children, from its
genre. So a cookery show records "unknown" for both, and step two then has to branch or flag a
question nobody would seriously ask.

**Why not.** The ban exists for a good reason and removing it is riskier than it looks. The
whole value of step one is that it describes without judging. Let it reason from genre and it
will start shading descriptions toward the answer it expects, which is the failure the two-step
design exists to prevent, and it would be invisible when it happened.

The right fix is narrow: allow it only where the answer is genuinely not in doubt. That line
needs drawing carefully, and drawing it hastily to make one test case pass would trade a
visible nuisance for an invisible bias. Left as is deliberately.

## 9. Small ones that still cost accuracy. NOT FIXED.

- One certificate covering both cinema and home video has to be entered twice, because the
  field holds one scope. Anything counting certificates would double-count it.
- Running time is a whole number of minutes, but one case is 13 minutes 42 seconds. Rounding
  is forced by the shape and forbidden by the instructions.
- "Countries: UK, FR" could mean where it is shown, where it was made, or where the rights
  sit. Nothing says which.
- "No warning was given" is someone positively answering a question. Not an event, not a gap,
  so it has nowhere to go and lands in a notes field.
- The source descriptions use words like "sustained" and "prolonged". Step one is banned from
  adding its own severity words but required to quote exactly. Stripping them would destroy
  the only signal about how long something lasts.
- Two things match no category: a minor injury, and pain played for laughs. Both land in the
  catch-all. Step two handles them correctly, but only because the catch-all rule happens to
  cover them.

---

## What this says about the prompts

The prompts are careful about the **reasoning** and were loose about the **containers**.
Almost every defect here is a box that cannot hold what the programme contains, or two facts
sharing one box. None was visible from reading. All of it surfaced on the first run.

Defect 1 was the one to fix before anything else, because it is the only one that silently
produces an answer more permissive than the law allows. The four still open cost accuracy, and
none unlocks a wrongly permissive answer, which is why they rank below the ones that are done.
