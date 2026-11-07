# What this covers, and what it does not

The brief asks for an age rating and the hours a programme may be shown. One line also asks
for "other relevant broadcast restrictions", which is vague enough to mean three different
things. The choice changes the answers, so it is written down here.

## The question

Should the system report:

**A.** Only the age rating and the hours?
**B.** Everything in the whole rulebook?
**C.** The age and hours, plus anything that changes them?

**C was chosen.** The test for including something is: *does this change, condition, or
replace the answer about age and hours?*

## Why A is not just incomplete, it is wrong

There is a rule that says a film can be shown **at any hour of the day**, including a weekday
afternoon, **provided** the channel has a PIN lock in place. Take the lock away and the same
film is barred before 9pm.

A system reporting only age and hours gets this wrong in both directions. It says "any time"
and drops the condition that earned it, which is a dangerous answer. Or it says "barred before
9pm" and misses that a lock would lift the restriction entirely, which costs the broadcaster a
slot it was entitled to use.

This is not an edge case. European law is built this way on purpose: it requires an outcome
(children are protected) and lets a broadcaster get there by scheduling **or** by technical
measures. The two are alternatives. A system that models only the clock cannot represent the
trade.

## What is included, and why

| Included | Why |
|---|---|
| PIN locks and similar access controls | Directly replaces an hour |
| The earlier watershed on unprotected premium film channels | The watershed is not one fixed time; it moves with the channel and whether a lock is present |
| The French on-screen age symbol | In France the symbol *is* the rating in its working form. Reporting the category without it is half an answer |
| Warnings given to viewers | Telling the audience what is coming changes what may be shown in a slot |
| Rules about what a programme may sit next to in the schedule | A time restriction written against the schedule instead of the clock |
| Trailers judged in their own slot | A trailer does not inherit the film's permission, so it is its own age and hours question |
| Annual caps on how often a late-night exception may be used | A limit on a time allowance |
| Which channels may show the most restricted category at all | Decides whether any answer exists |
| Exemptions and justifications | See below |

**On exemptions.** A system that models only bans systematically over-restricts. For a
broadcaster that is not a safe default: it is lost airtime and lost revenue for no gain in
compliance. So permissions and exceptions are stored as proper rules, not as footnotes.

## What is excluded, and why

Rules about impartiality, accuracy, elections, fairness to contributors, privacy, and
advertising or sponsorship. None of them produces an age rating or an hour. Each is a separate
job, for a different reviewer, with a different remedy.

Two of those exclusions are not as clean as they look, so they are flagged rather than
silently dropped:

- **The news rules do bind this broadcaster.** They are excluded because they yield no rating
  and no hour, not because they do not apply. One trace of them remains: news is regulated
  under a different section, so the system must still ask "is this news?" or it will apply a
  rule that does not bind.
- **The advertising rules matter for a preschool brand**, which restricts commercial
  references in children's programmes. Excluded as a different workflow, but real.

## The biggest gap: whose rules apply at all

**This is assumed, not established, and it is the most important limitation here.**

The table answers "what are the rules?" for a channel regulated by the UK regulator, and for a
channel regulated by the French one. It does **not** tell you which of those a given channel
is, and that is a real question with a surprising answer.

The two countries decide it in opposite ways. France, inside the EU, goes by where the
**company** is based: a channel follows the rules of its home country, and other countries
receiving it have to accept that. The UK, having left the EU, mostly goes by where the service
is **watched**: a channel available in the UK generally needs a UK licence wherever the company
sits.

So "where is this being watched" and "whose rules apply" are different questions, and in these
two countries they come apart in opposite directions.

Answering it needs facts about the company, not about the programme: where it is based, who
licensed it, which treaties cover the route between the two countries. None of that can be
read from a description of a programme, which is the only thing this system is given.

**So the boundary is: this table assumes you already know which regulator covers the channel.**
Feed it a country because that is where the audience is, and it will give you a confident
answer out of the wrong rulebook. Recorded as open question C-16.

## The honest cost

This system will stay silent on a real fairness problem, a real privacy problem, or an
advertising breach. The write-up says so plainly rather than implying it covers the whole
rulebook. A tool with stated boundaries can be audited. A tool that implies completeness it
does not have is a liability.

## For reference: which parts of the UK rulebook are used

| Section | Used | Why |
|---|---|---|
| Protecting under-eighteens | Yes | The watershed and the child-audience tests. The core of the task |
| Harm and offence | Yes | Supplies the binding definition of "context", and one of its factors is the time of broadcast |
| Crime, disorder, hatred and abuse | Yes | Its rules bend to the same context test, so the hour is an input. This was wrongly excluded at first |
| Religion | Yes | Restricts claims of special powers when many children may be watching |
| Impartiality and accuracy | No | Produces no rating and no hour. Checked against the live text: no rule mentions children, the watershed, or any time of day |
| Elections | No | Points back to impartiality |
| Fairness, Privacy | No | About how contributors are treated. No rating, no hour |
| Commercial references on TV | No, with the caveat above | Governs adverts and sponsorship, not the programme's rating or slot |
| Commercial references on radio | No | Radio |

One lesson came out of this that is worth stating: **a section can be out of scope for what it
restricts and still in scope for what it switches off.** The impartiality section gives no
hours, but it is the reason the system has to ask whether a programme is news. Scoping only by
"does this give me an hour?" would have missed that.

## What a local expert should check

- Whether any French linear channel in the group still operates after the 2025 closure, and
  if so what kind of service it counts as. This changes which French rules can apply at all.
- The licence conditions attached to the UK public-service channel, which may go beyond the
  rulebook itself.
- Whether the children's block is a separately licensed channel or a slot within the main one,
  which changes how the children's rules attach.
