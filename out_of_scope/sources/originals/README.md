# sources/originals/

The regulatory documents themselves, as published. **All 20 are here and all 20 are
verified.**

This README previously opened by explaining that the folder was empty on purpose. That was
true for most of the project and is now the opposite of the truth, which is a good example of
why anything stateful in this repo is generated rather than written by hand.

## What is in here

| file | what it is |
|---|---|
| `MANIFEST.csv` | The source of truth. 11 columns: what each document is, where it lives, whether it is on disk. |
| `expect.json` | A phrase that must appear in each stored file for it to count as genuinely retrieved. |
| `NOTES.md` | What is known about individual documents: which are translations, which are landing pages rather than the document, which concern a channel that no longer broadcasts. |
| `originals.lock.json` | A sha256 per document, so a later change at source is detectable. |
| `*.txt`, `*.pdf` | The documents. |
| `unused/` | Collected in good faith, then set aside. Has its own README saying why. |
| `incoming/` | Drop-box for manually saved files, emptied by `out_of_scope/pipeline/import_saved.py`. |

## How these were collected, and why it took three routes

Plain HTTP got 5 of 20. The rest sat behind browser challenges, or in one case behind a page
whose body is drawn by JavaScript and so is invisible to any fetcher.

1. **Direct fetch** (`fetch_originals.py`) for publishers that permit it.
2. **A real browser on a GitHub runner** (`fetch_with_browser.py`, Playwright). Added two
   more, then datacenter IP addresses were refused where a home connection would not have
   been.
3. **A human with a browser**, which got the remaining thirteen. A console snippet saved each
   page as text and checked it before downloading.

No challenge was defeated. Where a publisher refused automated access, the document was
listed for manual retrieval instead.

## The check that matters

Every document has an `expect` phrase. It is verified on fetch, on import, and on every
`--check`.

This is not ceremony. The French category V page returned 12,493 characters on its first
apparently successful save, which passed a length test, and was **entirely site navigation**.
A length heuristic cannot tell a document from a menu. A phrase that only the real document
contains can.

The phrase must also identify **that** document. Several earlier ones did not: one matched
five of twenty-two files, and one matched only the *wrong* document, because two unrelated
guidance notes both happened to say "Issue Six".

## Three things worth knowing before citing anything here

**`UK-M1` is a landing page, not the statement.** It carries the fact that the protection
rules were extended on 1 January 2019, but not the reasoning behind it. The statement PDF is
linked from the page and was never retrieved.

**`FR-R2` is a machine translation.** It is Arcom's own English rendering, and the page says
plainly that only the French original is authentic. Every quote drawn from it is English and
needs re-checking by someone who reads French.

**`FR-V1` concerns a channel that no longer exists.** C8 stopped broadcasting on 1 March 2025.
The decision is still a valid reading of the rule it interprets, since a regulator's
interpretation does not expire because the broadcaster did, but say so when citing it.

## HTML is preferred to PDF

Where a publisher offers both, the manifest points at the HTML. An HTML page keeps its address
across revisions and shows the current text; a PDF URL is often minted per revision and rots
silently, which is exactly what happened to four Ofcom links in this project.

Where a document is genuinely PDF-only, the manifest records a `landing_page`: the stable page
the current PDF is always reachable from, so a dead link is recoverable rather than a dead
end. Rows showing `n/a - url is itself a stable page` are HTML already and need no second
address.

## Re-checking later

```bash
python3 out_of_scope/pipeline/fetch_originals.py --check
```

Compares every file against its recorded hash and its expect phrase. A `CHANGED` result means
only that the bytes differ from the lock. It does **not** establish that a regulator altered
anything: replacing a file with a better copy produces the identical signal, and that has been
the common case here. Diff before concluding the law moved.
