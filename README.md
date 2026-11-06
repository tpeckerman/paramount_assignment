# Age ratings and broadcast restrictions for linear television — UK & France

Take-home assignment, prompt engineer. This repo holds the work for **Task 1**:
the regulatory sources, the rule table that the prompt will read, and the pipeline
that keeps both honest.

**Scope: linear (broadcast) television only.** On-demand and streaming are a different
regime in both countries — see `sources/FR_03_legal_basis_and_cnc.md` for why a film on a
streaming app is governed by a different French text entirely.

---

## Layout

```
sources/                        the regulatory corpus
  00_SOURCE_INVENTORY.md        START HERE - every body and document, with authority ranks
  UK_01..04_*.md                Ofcom Code s.1, s.2 (context), watershed guidance, MDP regime
  FR_01..03_*.md                Arcom reco. 2005-5, reco. 2004-7 (-18), legal basis + CNC
  EU_01_avmsd_article_6a.md     the framework both countries implement
  99_EXTRACTION_NOTES_*.md      READ BEFORE USING AS GROUND TRUTH - limits and open conflicts
  originals/
    MANIFEST.csv                26 source documents: URLs, filenames, tier
    originals.lock.json         sha256 of each, written by fetch_originals.py

rules/
  RULES_TABLE_v1.xlsx           the rule table - 82 rules, 6 tabs
  csv/                          per-tab CSV mirrors, so rule changes are diffable in a PR

pipeline/
  fetch_originals.py            download the original documents + record hashes
  verify_rules.py               integrity checks; run in CI
  build_rules_table.py          regenerates the workbook and the CSV mirrors
  COLAB_rule_pipeline_starter.ipynb   convert to a Google Sheet; change detection; versioning
```

---

## Quick start

```bash
pip install openpyxl pypdf

python pipeline/fetch_originals.py          # download the source documents
python pipeline/verify_rules.py --with-quotes
```

`--with-quotes` is the check that matters: every extracted rule must carry a verbatim quote
that provably occurs in its stored source document. Without it, extraction errors are silent
and a wrong row quietly becomes ground truth.

To change a rule, edit `pipeline/build_rules_table.py`, re-run it, and commit the workbook
together with the regenerated CSVs so the diff is reviewable.

---

## Two caveats that change how this may be used

### 1. The source files are extracts, not official text

The environment that produced them had **no outbound network access** to `ofcom.org.uk`,
`arcom.fr`, `legifrance.gouv.fr`, `bbfc.co.uk`, `legislation.gov.uk` or `eur-lex.europa.eu` —
all six were refused at the egress proxy — and the available fetch path returns model-written
summaries rather than source text, explicitly declining full reproduction.

So every file in `sources/` is a **structured extract with a canonical URL**, and is labelled
as such. `pipeline/fetch_originals.py` exists to close that gap from any machine with ordinary
internet access. Until it has been run, the quote-integrity check cannot run either.
Logged as conflict **C-04**.

### 2. `determinacy` and `ambiguity_flag` are different things

| Column | Describes | Governs |
|---|---|---|
| `determinacy` | **the rule** — `bright_line` / `conditional` / `judgment_based` | how you **score** it |
| `ambiguity_flag` | **our extraction** — `clear` / `translation_uncertain` / `unverified` / … | whether the row is **usable yet** |

They are independent: a bright-line rule can be translation-uncertain, and a judgment-based
rule can be perfectly clear. Merging them makes the test set unscoreable.

Scoring, by determinacy:
- `bright_line` → exact match; any deviation is a defect.
- `conditional` → the right answer **or** a correct missing-information request when the gating
  input was absent. Both pass.
- `judgment_based` → score the **cited rule and the reasoning**, accept a band of outcomes,
  require escalation near a threshold. Grading these by exact match measures your test set,
  not the model.

Current spread: **38** bright-line, **17** conditional, **27** judgment-based.
**24** rows flagged `human_review_required`.

---

## Using the table as ground truth

Filter `status == 'approved'` — **71 of 82**.

| status | n | why |
|---|---|---|
| `approved` | 71 | usable |
| `draft` | 4 | French category III (-12) scheduling + channel conventions. Conflict **C-02**: Arcom's English text is a machine translation and is garbled at art. 3. Resolved via a French government page, but needs confirming against the Légifrance original. |
| `unverified` | 7 | All French category V (-18) rows. Conflict **C-03**: the sole source dates from 2004 with compliance deadlines of 2005/2006/2008, all elapsed, and predates both the CSA→Arcom transition and the 2021 AVMSD transposition. |

Open conflicts **C-01 … C-08** are in `rules/csv/Open_Questions.csv` and
`sources/99_EXTRACTION_NOTES_AND_LIMITS.md`.

### Correlated error

The extraction and the prompt share an author, so they would share mistakes — the exact failure
Task 2 asks about. The bright-line rows (times, absolute prohibitions) should be
**independently re-derived from the primary sources by someone who has not seen this table**,
then compared. The `verbatim_quote` and `source_url` columns exist so a reviewer can check a
row without reading the prompt at all. Logged as **C-08**.

---

## Findings that shape the prompt design

1. **The UK has no per-programme age rating for linear TV.** The correct UK output is a
   scheduling verdict, the earliest permissible time, and the Code rules relied on — not an
   age label. France *does* have a graded rating (I–V), with its own hours. The two countries
   cannot share one decision path.

2. **Hours follow service type, not just the rating.** French **-16** is after 22:30 on
   ordinary channels but after **20:30** on cinema and pay-per-view channels — identical
   content, different hour. A UK **BBFC 18** film is barred before 21:00 on one service and
   permitted **at any hour** on another, purely because of a PIN measure. Any rating→hours
   mapping fails here.

3. **The French -18 window lives in a different document** (reco. 2004-7, 00:00–05:00) from
   the rest of the scheduling rules, and **service eligibility gates it**: on an ineligible
   channel it is a total prohibition and the hours are irrelevant. Answering by analogy with
   -16 is wrong.

4. **Some rules ignore the category entirely.** French art. 1 restricts violence, including
   psychological violence, between 06:00 and 22:00 regardless of the category assigned. A
   solution that reasons only over I–V misses it.

5. **Music videos are treated oppositely.** France exempts them from systematic signage with a
   soft *"preferably after 22:00"*; the UK applies the full watershed with detailed content
   thresholds and says explicitly that a niche music channel does not reduce the duty. The same
   video yields a hard UK verdict and a soft French one. Rendering the French preference as a
   prohibition is an over-rating defect.

6. **Three UK access concepts must not be conflated** — *mandatory daytime protection* (films,
   any hour), *mandatory restricted access* (adult sex material, 22:00–05:30 only), and no
   protection. Treating "PIN protected" as one concept wrongly allows adult sex material in
   daytime.

7. **Required inputs a bare content description will not contain:** service type; access
   measures in place; the intended broadcast **date** (France has day-of-week and
   school-holiday rules); whether the asset is a theatrical film and its existing BBFC/CNC
   classification; and whether it is a trailer or a music video. When one is missing and a
   candidate rule depends on it, the correct output is a **missing-information flag**, not an
   assumption. Several of these make good dedicated test cases.

8. **Absolute prohibitions should be enforced in code, not prompt reasoning** —
   `UK-GEN-001`, `UK-SEX-001`, `UK-FLM-001`, `UK-FLM-006`, `FR-LAW-001`,
   `FR-PRO-001/002/003`. No contextual argument or access measure should be able to override
   them.

---

## Regulatory bodies in scope

Ofcom and Arcom are the regulators, but they are not the only sources.

**UK** — Ofcom Broadcasting Code s.1 and s.2, Ofcom guidance, Ofcom's separate
**mandatory daytime protection** statement, Ofcom enforcement bulletins (the only source of
*applied* thresholds), Communications Act 2003 s.319, SI 2020/1062, and **BBFC** as an input
for films.

**France** — Arcom recommendation 2005-5 as amended by délibérations 2012-57 and **2014-17**
(the current operative scheduling text), **recommendation 2004-7** for category V,
Loi 86-1067 art. 15 (the two-tier *nuire gravement* / *nuire* standard), per-channel
**conventions** (which can be stricter and are not consolidated anywhere — **C-06**), and
**CNC** as an input for theatrical films only.

**EU** — AVMSD art. 6a, the common ancestor. It mandates an *outcome* and permits broadcast
time **or** technical measures as alternatives, which is precisely why the two national
frameworks look so different.

**Ruled out:** ASA/BCAP advertising codes, radio, and on-demand/VSP regimes.

Full detail with authority ranks: `sources/00_SOURCE_INVENTORY.md`.
