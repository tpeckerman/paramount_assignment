# Which Code sections are in scope — and why, given what Paramount actually operates

Scoping the Code in the abstract produced one error already (C-11: Section Three was wrongly
excluded). Scoping it against the actual service mix catches a second class of error — rules
that are in scope on paper but can never fire, and rules that looked peripheral but are
central because of what these channels are.

---

## What Paramount operates in the two markets

**UK — five linear channels, one of them a PSB, one brand aimed at preschoolers.**
The linear roster is `5` (formerly Channel 5), `5Action`, `5Star`, `5USA` and `5Drama`, the
last launched 21 October 2026 in place of `5Select`. `5` is the UK's third largest commercial
public service broadcaster, and the portfolio includes `Milkshake!`, a dedicated preschool
brand.

Two consequences:

1. **Child-audience rules are the core case, not the edge case.** A preschool block means
   "programmes made for children" and "when children are particularly likely to be watching"
   are everyday determinations, not exceptional ones.
2. **PSB status brings a news obligation.** So the Code sections that govern news genuinely
   bind this broadcaster. "Paramount doesn't do news" is not available as a scoping reason.

**France — service type is the pivot, and it is not a given.**
The French scheduling rules are *service-type dependent*: the same category III title is
barred before 22:00 on a general channel and before 20:30 on a cinema or pay-per-view
service, and the day of the week moves it again.

> **Design consequence.** Stage 2 must never assume a French service type. It must branch
> across the plausible ones and say which answer belongs to which. A single unqualified
> French answer is almost always wrong.

---

## Section-by-section, with the reason stated

| Section | In scope | Reason |
|---|---|---|
| One — Protecting the under-eighteens | **Yes** | The watershed and the child-audience tests. The whole point. |
| Two — Harm and offence | **Yes** | Supplies the binding definition of "context", whose third factor is the time of broadcast. |
| Three — Crime, disorder, hatred and abuse | **Yes** | Rules 3.2/3.3 are permitted "except where it is justified by the context" — the same context test, so the hour is an input. Wrongly excluded at first; see C-11. |
| Four — Religion | **Yes** | Rule 4.7 restricts claims of special powers when significant numbers of children may be watching. |
| Five — Due impartiality and accuracy | **No, but it binds them** | Yields **no age rating and no broadcast hour**. A different compliance decision, not a different company's problem. Verified against the live page: "justified by the context" appears in no rule, "editorially justified" only at Rule 5.3, and no rule mentions children, the watershed or any time of day. |
| Six — Elections and referendums | No | Cross-refers to Section Five. Same reason. |
| Seven — Fairness | No | Governs treatment of contributors. No rating, no hour. |
| Eight — Privacy | No | Same. |
| Nine — Commercial references in TV | No, **with a caveat** | Restricts commercial references in children's programming — which a preschool brand makes live and real. But it governs *commercial* content, not the content rating or its slot: a separate sponsorship and advertising workflow, the same reason the ASA/BCAP codes are out. Flagged rather than silently dropped **because Milkshake! exists**. |
| Ten — Commercial references on radio | No | Radio. Out of scope entirely. |

---

## The routing flag this analysis produced

Section Five is out of scope as a *source of restrictions* but in scope as a *router*. The
note to Rule 2.2 states that news is regulated under Section Five — so for news content,
Rule 2.2 does not apply.

That makes **"is this news or current affairs?"** a question Stage 1 must answer, not because
news gets different hours, but because answering it wrongly applies a Section Two rule that
does not bind. Added to Stage 1's asset block as `is_news_or_current_affairs`.

This is the general shape of the lesson: a section can be out of scope for what it *restricts*
and still in scope for what it *disapplies*. Scoping by "does this section give me an hour?"
alone would have missed it — the same single-test mistake as C-11, in a new costume.

---

## What a local expert should check

- Whether any Paramount French linear service survived the 2025 closure, and if so its
  service type under the Arcom classification. This changes which French rules can fire.
- The licence conditions attaching to `5` as a PSB, which may impose obligations beyond the
  Code itself and are not in the Code text.
- Whether `Milkshake!` is a separately licensed service or a block within `5`, which affects
  how the children's-programming rules attach.
