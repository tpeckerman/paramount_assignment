# Stage 0 — Build the rules table from source documents

This is the prompt that produces `rules/csv/Rules.csv` from the documents in
`sources/originals/`. It runs **once per document**, not once per decision. That separation
is the whole architecture: reading regulation and applying regulation are different jobs, and
doing them in one step is how a misreading becomes invisible — nothing separates "what the
rule says" from "what I decided", so there is nothing to check.

Everything below was learned by getting it wrong. Each warning marks a real defect that
reached a committed table.

---

## Input

One regulatory source document, plus its manifest row (`doc_id`, `title`, `url`, `expect`).

## Output

Rows for the rules table. One row per **operative rule**, not per paragraph, not per heading.

---

## Before you extract anything: three checks on the document

**1. Is this the current version?**
The test is the publisher, not the date. A guidance note from 2015 can be current; a PDF from
last year can be superseded. Look for: an issue number, a "last updated" line, and — most
importantly — whether any *amending instrument* exists.

> **This caused two separate failures.** A French category definition was broadened by an
> amending instrument in 2014; the table carried the 2005 wording and would have **under-rated**
> content. It survived review because the English translation and the pre-2014 French text
> agreed *with each other* — both were simply out of date. Cross-checking sources cannot catch
> this. **Only reading the amending instrument can.** The same error then recurred: guidance
> from 2015 was cited for a rule restructured by a statement in 2018.
>
> So: **no row may be approved while citing guidance older than the most recent amendment to
> the rule it interprets.** Record an `amended_by` note on every source.

**2. Is this the whole document, or site furniture?**
A saved web page can be 80% navigation. Worse, it can be *100%* navigation and still look
plausible by length — one saved file was 12,493 characters of pure menus and passed a naive
length check. Confirm a phrase that only the real document contains.

**3. Is this a primary or a secondary source?**
A regulator's own summary page, a government explainer, a news article: all useful for
orientation, none citable as the rule. Mark it. A rule whose only proof quote comes from a
secondary source is an *inference*, and must say so in the row.

---

## Extracting a rule

For each operative rule, capture:

| field | what goes in it |
|---|---|
| `rule_id` | `<COUNTRY>-<CAT>-<NNN>` |
| `authority_rank` | 1 statute, 2 regulator binding, 3 guidance, 4 precedent, 5 regulator summary, 6 classification body, 7 secondary. Conflicts resolve by lowest number. |
| `service_type` | Which services it binds. **Never leave this blank or guess it.** |
| `content_category` | From the controlled vocabulary. A value outside it silently drops the rule out of every decision. |
| `classification` | The label the rule assigns, or `n/a`, or `context_dependent` |
| `time_restriction_text` | The hours in words |
| `time_rule_machine` | The hours as a parseable token |
| `exceptions_conditions` | Derogations, quotas, carve-outs, conditions precedent |
| `determinacy` | `bright_line` / `conditional` / `judgment_based` |
| `ambiguity_flag` | `clear` / `conflicting_sources` / `translation_uncertain` / `unverified` |
| `verbatim_quote` | Proof. See below. |
| `clause_ref` | The rule number as printed in the instrument |

### The quote rule, which is the one that catches everything

`verbatim_quote` must be **character-for-character present in the stored source file.** Not a
paraphrase. Not a tidied version. Not a fragment with punctuation added to make it look like a
sentence.

> **Four quotes failed this check the moment real sources arrived.** Two were paraphrases I
> had written as quotes — "Children are people under fifteen" where the Code says "under the
> age of fifteen years". One cited the wrong document. The fourth is the instructive one: it
> ended `"...post-0530."` with a full stop **I had added**, cutting the sentence before the
> words "which cannot be removed by the user" — the exact words that make the rule
> enforceable. A truncated clause dressed as a complete sentence.
>
> None of these is findable by re-reading your own work. All four were found in seconds by an
> automated check. **Build the checker before you trust the table.**

Keep quotes under 15 words. If it will not fit, the row needs splitting.

### Three distinctions that are easy to collapse and expensive to get wrong

**Determinacy is not ambiguity.** `determinacy` describes the *rule* — is the line bright or
is it a judgment? `ambiguity_flag` describes *your extraction* — are you sure you read it
right? A crisp rule you are unsure you transcribed is `bright_line` + `unverified`. Merging
them loses the ability to say "this rule is clear and I am not confident I captured it".

**An age rating is not a broadcast hour.** They are separate outputs of separate rules and
they come apart in both directions. One jurisdiction here issues **no per-programme rating for
linear TV at all** — a scheduling answer only. In the other, the same category yields
different hours on different service types and different weekdays.

**A restriction is not always a time.** A PIN gate, on-screen signage, an audience warning, an
adjacency limit, a quota cap: these can *substitute* for hours. One rule reads
`any_time; requires=mandatory_daytime_protection` — permitted at any hour, including a weekday
afternoon, provided a gate is in place. Another disapplies the watershed entirely while that
gate is on. **If you extract only ratings and hours, you will produce answers that are wrong,
not merely incomplete.**

### Capture allowances too

Derogations, exemptions, editorial-justification routes, fiction exemptions. A table of
prohibitions only will systematically over-restrict, which costs distribution for no
compliance benefit. These are rows, not footnotes.

### Mine the guidance for worked examples

Guidance notes contain the regulator's own examples and enforcement reasoning. These are the
only thing that calibrates a `judgment_based` rule. Capture them as examples attached to the
rule — a rule that says "judgment required" with no example is barely more useful than silence.

---

## What to do with conflicts

Do not resolve a conflict by picking the tidier answer. Record both, cite both, set
`human_review_required`, and log it with: what conflicts, which rows are affected, what you
believe and why, and what evidence would settle it.

If two sources agree, that is **not** corroboration when they could share an origin — a
translation and its original, or two documents of the same vintage both predating an
amendment.

---

## Self-check before emitting

1. Does every `verbatim_quote` appear in the stored source? Run the checker; do not eyeball it.
2. Does every row's `source_url` point at the **consolidated current** text? Original-publication URLs belong only on superseded rows.
3. Is any row approved while citing guidance older than the latest amendment to its rule?
4. Does any row state a time without its conditions?
5. Is any `service_type` blank or assumed?
6. Does the `content_category` come from the controlled list?
7. Have you recorded what you could **not** determine?

> The last one matters most. A table that is silent about its gaps will be trusted
> exactly as far as a table that has none.
