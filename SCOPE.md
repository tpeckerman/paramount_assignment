# Scope decision: what "other relevant broadcast restrictions" includes

The task is titled *Determine Age Rating and Broadcast Time Restrictions*, but one requirement
bullet asks for "other relevant broadcast restrictions". Those two framings admit three
different scopes, and the choice materially changes the answer, so it is recorded here rather
than left implicit.

## The three candidate scopes

| | Scope | Verdict |
|---|---|---|
| A | Age rating and clock hours only | **Too narrow.** Produces answers that are wrong, not merely incomplete, see below. |
| B | Everything in the Broadcasting Code | **Too broad.** Ten sections, mostly judgment-based, with one enforcement precedent for calibration. Yields confident mush and a tool that claims authority it cannot support. |
| C | The age/time decision **and everything that conditions or substitutes for it** | **Chosen.** |

## The inclusion test

> Does this restriction or allowance **change, condition, or substitute for** the age/time
> answer?

The word doing the work in the requirement is "**relevant**", relevant to the thing the title
names. That gives a sharp test rather than a vibe, and it cuts in a non-obvious place: it
admits several restrictions that are not about time or age on their face.

### Why scope A is wrong rather than just incomplete

The table contains this row:

```
UK-FLM-003   Rule 1.24   any_time; requires=mandatory_daytime_protection
```

Permitted at **any hour**, including a weekday afternoon, *provided* a PIN gate is in place.
Remove the PIN and the same film is barred before 21:00.

A scope-A tool reports "any time" and is catastrophically wrong, because it dropped the
condition that earned the hours. The same tool reports "barred before 21:00" in the other
direction and is wrong again, having missed that an available technical measure lifts the
restriction entirely.

This is not an edge case. It is the mechanism the EU framework is built on: Article 6a
requires an *outcome* and permits scheduling **or** technical measures as alternatives. So the
axes are not merely independent, **they are substitutes**, and a system that models only two
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
a safe default. It is lost revenue and lost distribution, with no compliance benefit. The
table therefore carries exemptions and derogations as first-class rows, not as notes.

## Out of scope, with the reason

Due impartiality and accuracy, elections, fairness, privacy, and commercial references. None
conditions the age/time answer; each is a separate workflow with a different reviewer and a
different remedy.

Two qualifications, so the exclusions are not silent:

- **The news section binds this broadcaster**, a commercial PSB licence carries news
  obligations. It is excluded because it yields no rating and no hour, not because it does not
  apply. It is still retained as a **router**: the note to Rule 2.2 regulates news elsewhere,
  so "is this news?" must be answered or a harm-and-offence rule gets applied where it does
  not bind.
- **The commercial-references section is live for a preschool brand**, which restricts
  commercial references in children's programming. Excluded as a sponsorship and advertising
  workflow, flagged rather than dropped.

### Which channels these rules apply to at all

**Assumed, not established.** The table answers "what are the rules?" for a channel that
Ofcom regulates, and for a channel that the French regulator regulates. It does **not**
establish whether a given channel is one of those, and that is a real question with a
non-obvious answer.

The two countries decide it in opposite ways. France, in the EU, works on country of origin:
a channel follows the rules of the country where the company is based, and the countries
receiving it have to accept that. The UK, having left the EU, works mainly on country of
destination: a service available in the UK generally needs an Ofcom licence wherever the
company sits. So "where is this being watched" and "whose rules apply" are different
questions, and in these two countries they come apart in opposite directions.

Working that out needs facts about the company, not about the programme: where it is
established, who licensed it, which treaties cover the route between the two countries. None
of that can be read off a content description, which is the only input this system takes.

So it is out of scope, and the boundary is: **this table assumes you already know the channel
is regulated by Ofcom or by Arcom.** Feeding it a country because that is where the audience
is will produce a confident answer out of the wrong rulebook. Recorded as open conflict C-16.

## The honest cost

This tool will stay silent on a genuine fairness or privacy problem, and on commercial
compliance. The write-up must say so plainly rather than implying full-Code coverage. A tool
whose boundaries are stated is auditable; a tool that implies completeness it lacks is a
liability.

---

# Which Code sections are in scope

## Section-by-section, with the reason stated

| Section | In scope | Reason |
|---|---|---|
| One, Protecting the under-eighteens | **Yes** | The watershed and the child-audience tests. The whole point. |
| Two, Harm and offence | **Yes** | Supplies the binding definition of "context", whose third factor is the time of broadcast. |
| Three, Crime, disorder, hatred and abuse | **Yes** | Rules 3.2/3.3 are permitted "except where it is justified by the context", the same context test, so the hour is an input. Wrongly excluded at first; see C-11. |
| Four, Religion | **Yes** | Rule 4.7 restricts claims of special powers when significant numbers of children may be watching. |
| Five, Due impartiality and accuracy | **No, but it binds them** | Yields **no age rating and no broadcast hour**. A different compliance decision, not a different company's problem. Verified against the live page: "justified by the context" appears in no rule, "editorially justified" only at Rule 5.3, and no rule mentions children, the watershed or any time of day. |
| Six, Elections and referendums | No | Cross-refers to Section Five. Same reason. |
| Seven, Fairness | No | Governs treatment of contributors. No rating, no hour. |
| Eight, Privacy | No | Same. |
| Nine, Commercial references in TV | No, **with a caveat** | Restricts commercial references in children's programming, which a preschool brand makes live and real. But it governs *commercial* content, not the content rating or its slot: a separate sponsorship and advertising workflow, the same reason the ASA/BCAP codes are out. Flagged rather than silently dropped **because Milkshake! exists**. |
| Ten, Commercial references on radio | No | Radio. Out of scope entirely. |

---

## The routing flag this analysis produced

Section Five is out of scope as a *source of restrictions* but in scope as a *router*. The
note to Rule 2.2 states that news is regulated under Section Five, so for news content,
Rule 2.2 does not apply.

That makes **"is this news or current affairs?"** a question RUN 1 must answer, not because
news gets different hours, but because answering it wrongly applies a Section Two rule that
does not bind. Added to RUN 1's asset block as `is_news_or_current_affairs`.

This is the general shape of the lesson: a section can be out of scope for what it *restricts*
and still in scope for what it *disapplies*. Scoping by "does this section give me an hour?"
alone would have missed it, the same single-test mistake as C-11, in a new costume.

---

## What a local expert should check

- Whether any Paramount French linear service survived the 2025 closure, and if so its
  service type under the Arcom classification. This changes which French rules can fire.
- The licence conditions attaching to `5` as a PSB, which may impose obligations beyond the
  Code itself and are not in the Code text.
- Whether `Milkshake!` is a separately licensed service or a block within `5`, which affects
  how the children's-programming rules attach.
