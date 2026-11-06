# Extraction Notes, Limits and Verification Status

Compiled: 2026-11-06

Read this before using `RULES_TABLE_v1` as ground truth.

---

## 1. What these files are, and what they are not

**They are structured extracts with canonical source URLs. They are not the official full text.**

This matters and should be stated in the assignment submission, because it changes what the ground-truth
table can legitimately be used for.

### Why full verbatim text could not be captured

Two independent blocks:

1. **No direct network access from the execution environment.** Outbound requests to `ofcom.org.uk`,
   `arcom.fr` and `legifrance.gouv.fr` are refused by the egress proxy
   (`connect_rejected` — host not on the session allowlist). Verified by direct test:
   `curl https://www.ofcom.org.uk/.../Broadcast-code-Section-1.pdf` → `CONNECT tunnel failed, response 403`.
2. **The available web-fetch path returns summaries, not source text.** It renders the page and then answers
   a prompt against it with a separate model, which declines to reproduce documents in full
   ("I can't reproduce the full verbatim text"). Several fetches returned exactly that.

Additional specific failures encountered:
- `ofcom.org.uk/.../section-one-protecting-under-eighteens` → site-level `client_error`.
- `ofcom.org.uk/.../section-two-harm-offence` → not on fetch allowlist.
- The `csa.fr` canonical URL for délibération 2014-17 → rejected, *"url exceeds the maximum fetchable length"*.
  Worked around via the `arcom.fr` English equivalent.

### Consequence for the `verbatim_quote` column

The column holds **short quoted fragments that came through the fetch intact** (e.g. the MDP definition,
the AVMSD "most harmful content" sentence). It is **not** a complete quotation of each rule, and it
**cannot currently support an automated quote-integrity check**, because there is no local copy of the
source to check against.

### What would fix it (and why this is a Task 2 finding, not just a Task 1 caveat)

An automated rule-ingestion pipeline **must not** depend on model-mediated fetching for legal text.
It needs either:
- an allowlisted direct fetch of the source documents (PDF/HTML bytes), or
- manual deposit of the official PDFs into the Drive source folder.

Either gives a local canonical copy, which then makes the central integrity control possible:
**every extracted row must carry a verbatim quote that is programmatically confirmed to appear in the
stored source file.** Without that control, extraction errors are silent. This is the single most important
structural recommendation for Task 2.

---

## 2. Two different kinds of "ambiguous" — do not merge them

The table carries **two separate columns** because these are different problems with different remedies.

### `determinacy` — a property of the rule itself
| Value | Meaning | Example |
|---|---|---|
| `bright_line` | One correct answer, mechanically checkable. | Ofcom 1.4 watershed = 21:00. FR cat. IV on non-cinema channels = after 22:30. |
| `conditional` | Bright line, but gated on a condition that must be supplied as input. | Ofcom 1.23 — 18-rated film before 21:00 **unless** MDP in place. FR cat. III derogation after 20:30 except Tue/Fri/Sat/holiday-eve/school holidays. |
| `judgment_based` | Requires evaluative assessment; a *range* of defensible answers. | Ofcom 1.11 "appropriately limited… justified by the context". FR art. 1 violence "perceived as continuous". |

**This column governs how the test set is scored.** Scoring a `judgment_based` row with exact-match is
a measurement error, not a model failure. Suggested scoring:
- `bright_line` → exact match required; any deviation is a defect.
- `conditional` → correct answer **or** a correct missing-information request if the condition was absent.
- `judgment_based` → score the **reasoning and the cited rule**, accept a band of outcomes, and require
  escalation when near a threshold.

### `ambiguity_flag` — a property of *our extraction*
| Value | Meaning |
|---|---|
| `clear` | Extraction is unambiguous and corroborated. |
| `conflicting_sources` | Two sources disagree; resolved by authority rank, resolution recorded. |
| `translation_uncertain` | Derived from a machine translation whose wording is unreliable. |
| `unverified` | Not confirmed against current official text; currency in doubt. |
| `out_of_scope_for_asset_decision` | A real obligation, but not answerable per-asset (quotas, contracts, bundles). |

**Rows with `ambiguity_flag != clear` must not be used as ground truth until resolved.**
They are currently `status = draft` or `unverified`, never `approved`.

---

## 3. Open conflicts and their current resolution

| ID | Issue | Resolution | Still to do |
|---|---|---|---|
| **C-01** ✅ | Arcom's public summary page describes **-12** as daytime-permitted "under certain conditions", identical to its **-10** wording. Binding text says not before 22:00 on non-cinema channels. | **CLOSED.** Binding text wins (rank 2 over rank 5), and is now confirmed in French (C-02). FR-S1 must not be used as a rule source. | None. Retained as the worked example of authority-rank conflict resolution. |
| **C-02** ✅ | Arcom's **English machine translation** of art. 3 duplicates the cinema-channel sentence for cat. III, then says "before 10 pm", leaving the service mapping ambiguous. | **CLOSED 2026-11-06.** Confirmed against the **French** text from two independent sources: Légifrance `JORFTEXT000000446802` and the csa.fr consolidated page carrying the *"Modifiée par la délibération n° 2014-17"* banner. Non-cinema → not before **22:00**; cinema/PPV → not **Wednesdays before 20:30**; cat. IV → **22:30** / **20:30**. All affected rows promoted to `approved`. | Confirm the derogation's "16/year, max 4" quota numbers in French — still attested only in the English rendering. Does not block the hours. |
| **C-09** ✅ | Closing C-02 exposed an extraction error of our own: délibération 2014-17 replaced art. 2's fifth alinéa and **broadened** the cat. III definition, but the table carried the 2005 wording. `leur scénario recourt de façon répétée **et systématique**` → `le programme recourt de façon répétée`. | **CLOSED 2026-11-06.** `FR-CLS-003` corrected; the pre-2014 wording retained as `FR-CLS-903`, `status=superseded`, `valid_to=2014-04-08`. | None for the rule. The lesson: the error survived because the EN translation and the pre-2014 French text **agreed with each other**, so cross-source corroboration did not catch it — only reading the amending instrument did. Never trust a page labelled "consolidated"; diff the amending deliberation. |
| **C-03** | **Recommandation 2004-7** (the sole source of the French **-18** hours, 00:00–05:00) dates from 2004 with deadlines of 2005/2006/2008, all elapsed. CSA→Arcom transition (2022) and the 2021 AVMSD transposition decree both postdate it. | None — flagged. | Check the current Arcom legal register for amendment/replacement. All cat. V rows are `unverified`. |
| **C-04** | No verbatim source text available locally (section 1 above). | Documented; URLs recorded on every row. | Obtain official PDFs to enable quote-integrity checking. |
| **C-05** | Ofcom Section One uses **"children" = under 15** while the section's principle covers **under 18**. Easy to conflate. | Both recorded explicitly in `UK_01`. | Nothing — but note it in the prompt, since it affects rules 1.3, 1.10, 1.13, 1.27. |
| **C-06** | French **channel conventions** can be stricter than the general recommendation and are not consolidated anywhere. | Out of scope for v1; `channel_specific_override` concept noted. | For Task 2: per-licensee data source, requires local expert. |

---

## 4. Known gaps in v1 (deliberate, documented)

- **Ofcom Guidance Notes for Sections One and Two** were identified but not extracted in detail.
  They would sharpen the `judgment_based` thresholds.
- **Ofcom enforcement precedent** is represented by a single example (*Toofan*, NTV, 29 May 2026 — Rule 1.3
  breach, violent film at 11:30). A real system should ingest the bulletins systematically: they are the
  only source of *applied* thresholds, which is exactly what `judgment_based` rows lack.
- **BBFC classification guidelines** are referenced but not extracted. Needed only for the film path.
- **French channel conventions** — not collected (see C-06).
- **Overseas France** (recommandation du 26 juillet 2005) — noted, not extracted.
- **Trailers** are covered for France (FR-R1 art. 5) and partially for the UK (UK-G1 guidance), but the UK
  Code's trailer treatment sits across Sections One and Two and is not fully mapped.

---

## 5. Recommended immediate next steps

1. ~~Resolve C-02 against Légifrance~~ — **done 2026-11-06.** The French scheduling rows are `approved`.
   Residue: confirm the derogation's "16/year, max 4" quota numbers in French.
2. **Resolve C-03** so the -18 window can be trusted. This is now the main blocker.
3. **Deposit official PDFs** of UK-S1, UK-S2, FR-R1 and FR-R2 into the Drive source folder,
   then add the quote-integrity check.
4. Only then freeze v1 as ground truth and begin prompt testing.

> **A note on using this as ground truth.** Because the extraction and the prompt would otherwise share the
> same author and the same reasoning, there is a real risk of correlated error — the exact failure mode the
> assignment's Task 2 asks about ("how will you prevent the same error appearing in both the solution and the
> test answer?"). Two mitigations are already available here:
> (a) the `verbatim_quote` + `source_url` columns let a reviewer check a row **without** reading the prompt;
> (b) the bright-line rows (times, absolute prohibitions) are checkable against primary sources by someone
> with no knowledge of the solution. Recommend that the **bright-line rows be independently re-derived from
> the primary sources by a second pass that does not see this table**, and the two compared.
