# sources/originals/

The original regulatory documents, as published. **This folder is empty on purpose.**

## Why it is empty

The environment that produced the extracts in `sources/` had no outbound network access to any
of the publishing domains. Verified directly — all six refused at the egress proxy:

| Domain | Result |
|---|---|
| `ofcom.org.uk` | `CONNECT tunnel failed, response 403` |
| `arcom.fr` | blocked |
| `legifrance.gouv.fr` | blocked |
| `legislation.gov.uk` | blocked |
| `bbfc.co.uk` | blocked |
| `eur-lex.europa.eu` | blocked |

The one available fetch path renders a page and then answers a question about it with a separate
model, which declines to reproduce documents in full. So the files in `sources/` are structured
**extracts with canonical URLs**, not official text. This is conflict **C-04** in
`../99_EXTRACTION_NOTES_AND_LIMITS.md`.

## Filling it

From any machine with ordinary internet access:

```bash
pip install openpyxl pypdf
python pipeline/fetch_originals.py            # required + recommended
python pipeline/fetch_originals.py --tier required
python pipeline/fetch_originals.py --only FR-R1 FR-A2b   # the two that resolve C-02
```

Then the check that actually matters:

```bash
python pipeline/verify_rules.py --with-quotes
```

If you are running inside a sandboxed session, the alternative is to add those domains under
**claude.ai → Settings → Capabilities → allowed domains**, after which the fetch works from
there too.

## Everything here is a text or PDF file

No HTML, no JavaScript app pages. `MANIFEST.csv` carries a `format` column:

| format | behaviour |
|---|---|
| `pdf` | fetched and stored as-is. Rejected if the bytes are not actually a PDF. |
| `html2txt` | the page is fetched and **extracted to readable `.txt`** — scripts and styles dropped, tags stripped, entities unescaped. |

The `url` column still holds the canonical page, because that is what a reviewer should
cite. Only what lands on disk is converted.

Three entries use the publisher's direct PDF endpoint: `UK-L1` and `EU-D1` via
legislation.gov.uk `/data.pdf`, and `EU-D1b` via EUR-Lex's CELEX PDF URL. Ofcom's
documents were already PDFs. Current split: **12 PDF, 17 text.**

### The JavaScript-shell trap

Légifrance and Arcom serve their legal texts through a JS front end, so a naive fetch can
return a 2 KB shell with no rule text in it — and store it as though it were the source.
That would quietly defeat the whole point of having local copies.

So the fetcher treats an extraction under **2,000 characters** as a *failure*, prints what
it got, and tells you to use the page's *Télécharger / Imprimer* PDF instead. The entries
most likely to hit this are flagged in `notes`: `FR-R1`, `FR-L1`, `FR-R1c`, `FR-R1d`,
`FR-A1`, `FR-A2b`, `FR-S1c`. If one does, save the PDF by hand into this folder under the
row's `target_filename` with a `.pdf` extension and change `format` to `pdf`.

## What the full Code PDF does and does not cover

`UK-S0` is `broadcast-code-full.pdf` — the whole Ofcom Broadcasting Code in one file. It is
worth having, but it is **not a shortcut to the whole corpus**. It covers **3 of the 29**
documents here:

| Covered by UK-S0 | Not covered |
|---|---|
| `UK-S1` Section One | **Guidance** (`UK-G1`, `UK-G2`, `UK-G3`) — published separately; the Code PDF contains rules, not guidance |
| `UK-S2` Section Two | `UK-M1` the mandatory-daytime-protection statement — the Code has the rules, the statement has the platform eligibility |
| `UK-S4` Section Four | `UK-P1` enforcement bulletin · `UK-L1`/`UK-L2` legislation · `UK-C1` BBFC |
| | **all 13 French and 2 EU documents** — it is the UK Code only |

So fetching `UK-S0` takes the required list from 19 to 16, not to 1.

### The trap worth naming

"I have the Code, so I have the rules" is wrong in a specific way. The Code gives the rules;
it does not give the **thresholds**. Everything that tells you *how much* violence is
"appropriately limited", what counts as "the most offensive language", or how fast content may
get stronger after 21:00 lives in the **guidance** and the **enforcement bulletins** — neither
of which is in the Code PDF.

`UK-G1` matters most of all: it is the only source with operational detail on **music videos**
and on the post-watershed ramp, and music videos are one of the content types the assignment
suggests for test cases. Of the 29 rule rows marked `judgment_based`, none of their thresholds
can be calibrated from `UK-S0` alone.

## What lands here

`MANIFEST.csv` lists 28 documents in three tiers:

- **required** — needed to verify the rules currently in the table
- **recommended** — identified but not yet extracted; would sharpen the `judgment_based` rows
  (the Ofcom guidance notes and enforcement bulletins in particular, since precedent is the
  only source of *applied* thresholds)
- **optional** — out of core scope, kept for contrast (overseas France; the on-demand regime)

`fetch_originals.py` writes `originals.lock.json` with the sha256 of each file. That lockfile
does two jobs: it makes the quote-integrity check possible, and
`fetch_originals.py --check` uses it to tell you when a regulator has **changed a document
under you** — at which point the affected rules get re-extracted and the old ones versioned
rather than overwritten (`COLAB_rule_pipeline_starter.ipynb`, cell 4).

## Two caveats on the manifest

- **`FR-A2b` was corrected.** The Légifrance JORF id originally guessed for délibération 2014-17
  (`JORFTEXT000028728754`) returns a **search page** — it was wrong, and no Légifrance id for this
  deliberation was located. `FR-A2b` now points at the **Arcom French** text instead, and `FR-R1c` /
  `FR-R1d` were added as the French consolidated texts on arcom.fr and csa.fr. Those, together with
  Légifrance `JORFTEXT000000446802` (the 2005 original, which *is* valid), are what closed **C-02**.
- **`FR-R1d`'s URL is very long** and exceeds some fetch-proxy URL-length limits. Plain `curl` and
  `fetch_originals.py` handle it; a browser-based fetcher may not.
- **Légifrance and Arcom pages may return a JavaScript shell** rather than the text. The
  fetcher rejects a non-PDF served as a PDF, but it cannot tell prose from an empty
  single-page app. If a fetched HTML file has no rule text in it, use the page's
  *Télécharger / PDF* link instead and update `MANIFEST.csv`.

## These files are committed

Once fetched, the documents are **committed to the repo** (`.gitignore` does not exclude them).
A reviewer cloning this repo gets the actual regulatory texts, and
`verify_rules.py --with-quotes` becomes runnable in CI rather than permanently skipped.
`originals.lock.json` records the sha256 and retrieval date of each, so a committed copy is
still provably the published one.

## Licensing

These are official regulatory and legislative texts, retrieved for compliance analysis.
UK legislation and Ofcom codes are Crown copyright, available under the Open Government
Licence; French official texts (Légifrance, JORF) are freely reusable; EU legislation is
reusable under the Commission's reuse policy. They are fetched rather than committed so that
each copy is provably the published one, with a recorded hash and retrieval date.
