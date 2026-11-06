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

## What lands here

`MANIFEST.csv` lists 26 documents in three tiers:

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

- **`FR-A2b`** — the Légifrance JORF id for délibération 2014-17 is **unconfirmed**. Verify it
  before trusting that row. It matters: FR-A2b and FR-R1 are the two documents that resolve
  **C-02**, the garbled translation of the French category III scheduling rule, which is what
  currently keeps four rows at `draft`.
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
