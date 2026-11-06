# Scope decision: what "other relevant broadcast restrictions" includes

The task is titled *Determine Age Rating and Broadcast Time Restrictions*, but one requirement
bullet asks for "other relevant broadcast restrictions". Those two framings admit three
different scopes, and the choice materially changes the answer, so it is recorded here rather
than left implicit.

## The three candidate scopes

| | Scope | Verdict |
|---|---|---|
| A | Age rating and clock hours only | **Too narrow.** Produces answers that are wrong, not merely incomplete — see below. |
| B | Everything in the Broadcasting Code | **Too broad.** Ten sections, mostly judgment-based, with one enforcement precedent for calibration. Yields confident mush and a tool that claims authority it cannot support. |
| C | The age/time decision **and everything that conditions or substitutes for it** | **Chosen.** |

## The inclusion test

> Does this restriction or allowance **change, condition, or substitute for** the age/time
> answer?

The word doing the work in the requirement is "**relevant**" — relevant to the thing the title
names. That gives a sharp test rather than a vibe, and it cuts in a non-obvious place: it
admits several restrictions that are not about time or age on their face.

### Why scope A is wrong rather than just incomplete

The table contains this row:

```
UK-FLM-003   Rule 1.24   any_time; requires=mandatory_daytime_protection
```

Permitted at **any hour**, including a weekday afternoon — *provided* a PIN gate is in place.
Remove the PIN and the same film is barred before 21:00.

A scope-A tool reports "any time" and is catastrophically wrong, because it dropped the
condition that earned the hours. The same tool reports "barred before 21:00" in the other
direction and is wrong again, having missed that an available technical measure lifts the
restriction entirely.

This is not an edge case. It is the mechanism the EU framework is built on: Article 6a
requires an *outcome* and permits scheduling **or** technical measures as alternatives. So the
axes are not merely independent — **they are substitutes**, and a system that models only two
of them cannot represent the trade.

## In scope, with the reason

| Restriction / allowance | Why it passes |
|---|---|
| Mandatory restricted access, mandatory daytime protection (PIN) | Substitutes directly for an hour. |
| The 20:00 watershed on unprotected premium subscription film services | The watershed is **not a single time**; it moves with service type and protection state. |
| French *signalétique* (on-screen pictogram) | The pictogram **is** the classification's operative form. A French category reported without it is half an instrument. |
| Audience information / advance warning | A context factor: bringing content to the audience's attention changes what is permissible in a slot. |
| Adjacency (`not_near=children_programmes`) | A time restriction expressed against the schedule rather than the clock. |
| Trailers and promos judged by their own slot | An age/time rule on a derived asset. A trailer does not inherit its film's permission. |
| Quota caps (16/year, max 4 cinema titles) | A limit on how often a time derogation may be used. |
| Service eligibility (category V on eligible services only) | Gates whether any answer exists at all. |
| Derogations, exemptions, the fiction exemption, editorial justification | **Allowances**, which move the answer in the permissive direction. |

### On allowances

Modelling only prohibitions systematically over-restricts. In a licensing context that is not
a safe default — it is lost revenue and lost distribution, with no compliance benefit. The
table therefore carries exemptions and derogations as first-class rows, not as notes.

## Out of scope, with the reason

Due impartiality and accuracy, elections, fairness, privacy, and commercial references. None
conditions the age/time answer; each is a separate workflow with a different reviewer and a
different remedy.

Two qualifications, so the exclusions are not silent:

- **The news section binds this broadcaster** — a commercial PSB licence carries news
  obligations. It is excluded because it yields no rating and no hour, not because it does not
  apply. It is still retained as a **router**: the note to Rule 2.2 regulates news elsewhere,
  so "is this news?" must be answered or a harm-and-offence rule gets applied where it does
  not bind.
- **The commercial-references section is live for a preschool brand**, which restricts
  commercial references in children's programming. Excluded as a sponsorship and advertising
  workflow, flagged rather than dropped.

## The honest cost

This tool will stay silent on a genuine fairness or privacy problem, and on commercial
compliance. The write-up must say so plainly rather than implying full-Code coverage. A tool
whose boundaries are stated is auditable; a tool that implies completeness it lacks is a
liability.
