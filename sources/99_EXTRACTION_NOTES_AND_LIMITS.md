# Limits and verification status

Read this before using the rule table as ground truth.

An earlier version of this file duplicated the conflict log and went stale: it still showed
two conflicts as open after they had been closed, was missing four that had been opened since,
and pointed at a file that had been deleted. **The conflict log lives in
`rules/csv/Open_Questions.csv` and nowhere else.** This file covers the limits that are not
conflicts.

## Where things stand

- 103 rules, 102 approved. The one exception is `FR-CNV-001`, draft because French channel
  conventions have not been collected.
- 20 of 20 source documents collected and on disk.
- **56 of the 102 approved rules carry a verbatim quote.** All 56 verify against their
  stored source, 0 failing. **The other 46 carry none and are never checked** (C-15).
  Treat an unquoted row as unverified whatever its status field says.
- Conflicts: see `rules/csv/Open_Questions.csv`. Four remain open; the substantive one is
  **C-07**, below.

## The limit that matters most: judgment rules are barely calibrated

**35 of 103 rules are `judgment_based`**, and exactly **one** decided case has been collected.

One case is an anchor, not a scale. It tells you that a BBFC 15 film with sustained graphic
violence at 11:30 in the morning breached, which is useful, but it does not tell you where the
line sits. Every `judgment_based` row should be treated as **routing to a human**, not as
deciding anything.

The fix is known and unglamorous: the guidance notes name roughly a dozen further decisions
(*The X Factor Final*, *Candy Bar Girls*, *Emmerdale*, *Coronation Street*, *EastEnders*,
*Ice Road Truckers*, *Taggart*, *Midsomer Murders*, *Hell's Kitchen USA*, *Amores Perros*,
*Stylista*). Collecting those bulletins is the highest-value remaining work on this table.

Tracked as **C-07**.

## Two kinds of ambiguity, which must not be merged

**`determinacy`** is a property of the **rule**.

- `bright_line`: a clock time or an absolute prohibition. Score by exact match; any deviation
  is a defect.
- `conditional`: the answer depends on an input such as service type. Either the right answer
  **or** a correct missing-information request passes, depending on whether the input was
  supplied.
- `judgment_based`: accept a band of outcomes, score the cited rule and the reasoning, and
  require escalation near a threshold. Scoring these by exact match measures the test set, not
  the model.

**`ambiguity_flag`** is a property of **the extraction**: `clear`,
`conflicting_sources`, `translation_uncertain`, `unverified`,
`out_of_scope_for_asset_decision`.

They are independent. A bright-line rule can be translation-uncertain; a judgment-based rule
can be perfectly clear. Merging them loses the most useful state of all: *this rule is crisp
and I am not confident it was transcribed correctly.*

## What the sources cannot tell you

**The French rules are quoted from an English translation.** The category V document is
Arcom's own machine rendering, and the page states that only the French original is authentic.
Every quote drawn from it is English and needs re-checking by someone who reads French.

**One UK document is a landing page, not the document.** `UK-M1` carries the fact that the
protection rules were extended on 1 January 2019 but not the reasoning. The statement itself
was never retrieved.

**One enforcement decision concerns a channel that no longer exists.** C8 stopped broadcasting
on 1 March 2025. The decision remains a valid reading of the rule it interprets, but say so
when citing it.

Per-source detail is in `sources/originals/NOTES.md`.

## Deliberate gaps

- **French channel conventions** (C-06). Each channel's agreement with the regulator can be
  stricter than the general law, and they are not consolidated anywhere. This is channel-level
  data: two channels in the same country, under identical law, can need different answers. The schema for it is set out in TASK2_SCALING.md.
- **BBFC classification guidelines.** The Code refers to BBFC ratings, but the guidelines
  behind those ratings are not collected. A certificate is treated as evidence, never as an
  answer.
- **Overseas France.**
- **Everything outside the age and time decision.** Impartiality, fairness, privacy and
  commercial references are excluded by a deliberate scope choice, set out in
  `SCOPE.md`. Note that the news section genuinely **binds** this broadcaster, since
  a commercial PSB licence carries news obligations. It is out of scope because it yields no
  rating and no hour, not because it does not apply.

## The structural limit

The rules, the prompts, the tests and the checker share an author, so they share their
mistakes. That is the exact failure mode Task 2 asks about, and it cannot be fixed by more
care from the same person.

The mitigation is independent re-derivation: someone who has **not** seen this table should
derive the bright-line rows from primary sources and diff. `verbatim_quote` and `source_url`
exist so a reviewer can check any single row without reading the prompt at all.

Tracked as **C-08**.

## A check that was measuring itself

For most of this project the quote check reported "50 verified, 0 failed, **0 skipped**",
and that read as complete coverage. It was not. "0 skipped" only ever meant no *source
document* was missing from disk. Rules carrying no quote were passed over in silence, because
the check iterated the rules that had one.

Six of the unchecked rules were the **absolute prohibitions**, the rules the design says
belong in code because no contextual argument may override them. Those six are now quoted and
verified.

The verifier now prints the denominator beside the count and names any unquoted absolute
prohibition. **A coverage number that counts only the rows which opted in will always report
success.**

## What the checks already caught

Worth stating, because it is the argument for the checks rather than for the table:

- Four defective quotes, found the moment real sources landed. Two were paraphrases written as
  quotes; one cited the wrong document; one had a full stop added mid-sentence, cutting off
  the words "which cannot be removed by the user" that make the rule enforceable.
- A French category definition broadened by a 2014 amendment, where the table carried the
  older, narrower wording and would have **under-rated** content. It survived review because
  the translation and the pre-amendment original agreed with each other. Cross-checking cannot
  catch that; only reading the amending instrument can.
- The same class of error a second time, in rules written hours after that lesson was recorded.
- A rule that could never reach the decision engine, because it described delivery rather than
  content.
- Two spellings of one service name, silently dropping a rule from every decision slice that
  used the other.

None of these was found by reading the work.
