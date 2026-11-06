#!/usr/bin/env python3
"""Bulk-fetch the outstanding sources using a real browser, on your own machine.

Why this exists. fetch_originals.py uses plain HTTP and gets 403 from Ofcom, legislation.gov.uk,
Legifrance and EUR-Lex, which all refuse automated clients. This script instead drives a real
Chromium through Playwright, which:

  - renders JavaScript, so FR-R2 (whose body is drawn client-side and is invisible to any
    fetcher) finally yields its text;
  - behaves like a browser, so the usual challenges generally pass;
  - verifies each save against the manifest's `expect` phrase and refuses to write a file that
    does not contain it. That guard is the point: FR-R2's first apparently-successful save was
    12,493 characters of pure site navigation that passed a naive length check.

Run it from the repo root:

    pip install playwright
    playwright install chromium
    python3 pipeline/fetch_with_browser.py

Useful flags:
    --only UK-S1 FR-R2      just these documents
    --headed                watch it work; needed if a challenge wants a click
    --timeout 45            seconds per page (default 30)

Files land in sources/originals/incoming/. Then run:

    python3 pipeline/import_saved.py

which identifies each file by content rather than filename, re-checks `expect`, records a
sha256 and updates the manifest. So the verification happens twice and a wrong filename here
is harmless.

If a page still fails after this, fall back to DOWNLOAD_SNIPPET.md and do that one by hand.
Nothing here tries to defeat a challenge that genuinely blocks it - it reports and moves on.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "sources/originals/MANIFEST.csv"
OUT = ROOT / "sources/originals/incoming"

STRIP = ("nav, aside, footer, header, script, style, noscript, svg, form, "
         "[class*=cookie], [class*=banner], [class*=breadcrumb], [aria-hidden=true]")


def fold(s: str) -> str:
    """Match the verifier's comparison: accents, ligatures and case all folded."""
    import unicodedata
    s = (s.replace("œ", "oe").replace("Œ", "OE")
          .replace("æ", "ae").replace("Æ", "AE")
          .replace("–", "-").replace("—", "-")
          .replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"'))
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--timeout", type=int, default=30)
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed. Run:\n"
              "    pip install playwright\n"
              "    playwright install chromium", file=sys.stderr)
        return 1

    rows = [r for r in csv.DictReader(MANIFEST.open(newline="", encoding="utf-8"))
            if not r["download_status"].startswith("verified")]
    if a.only:
        want = {x.upper() for x in a.only}
        rows = [r for r in rows if r["doc_id"].upper() in want]
    if not rows:
        print("nothing outstanding to fetch")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    ok, bad = [], []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not a.headed)
        ctx = browser.new_context(
            locale="en-GB",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36"),
        )
        page = ctx.new_page()

        for r in rows:
            doc, url, want = r["doc_id"], r["url"], r["expect"]
            dest = OUT / r["target_filename"]
            print(f"\n{doc:<8}{url[:84]}")

            try:
                if r["format"] == "pdf" or url.split("?")[0].lower().endswith(".pdf"):
                    resp = ctx.request.get(url, timeout=a.timeout * 1000)
                    if not resp.ok:
                        bad.append((doc, f"HTTP {resp.status}")); print(f"  FAIL HTTP {resp.status}")
                        continue
                    body = resp.body()
                    if not body.startswith(b"%PDF"):
                        bad.append((doc, "not a PDF")); print("  FAIL not a PDF")
                        continue
                    dest.write_bytes(body)
                    print(f"  saved {dest.name}  {len(body):,} bytes "
                          f"(expect '{want}' is checked on import)")
                    ok.append(doc)
                    continue

                page.goto(url, timeout=a.timeout * 1000, wait_until="domcontentloaded")
                # Let late-rendering bodies arrive, and nudge lazy content into view.
                page.wait_for_timeout(2500)
                page.mouse.wheel(0, 20000)
                page.wait_for_timeout(1500)

                text = page.evaluate(
                    """(strip) => {
                        const r = (document.querySelector('main, article, [role=main]')
                                   || document.body).cloneNode(true);
                        r.querySelectorAll(strip).forEach(n => n.remove());
                        return r.innerText;
                    }""", STRIP)
                text = re.sub(r"\n{3,}", "\n\n", (text or "").strip())

                if want and fold(want) not in fold(text):
                    bad.append((doc, f"missing expect phrase '{want}' ({len(text):,} chars)"))
                    print(f"  FAIL  expect phrase '{want}' not present in {len(text):,} chars")
                    print(f"        probably a challenge page or navigation only. "
                          f"Retry with --headed, or do this one by hand.")
                    continue
                if len(text) < 2000:
                    bad.append((doc, f"only {len(text)} chars"))
                    print(f"  FAIL  only {len(text)} chars")
                    continue

                dest.write_text(text, encoding="utf-8")
                print(f"  saved {dest.name}  {len(text):,} chars, expect phrase present")
                ok.append(doc)

            except Exception as e:
                bad.append((doc, type(e).__name__))
                print(f"  FAIL  {type(e).__name__}: {str(e)[:110]}")

        browser.close()

    print(f"\n{'=' * 64}\nsaved {len(ok)}  |  failed {len(bad)}")
    if ok:
        print("  ok     : " + " ".join(ok))
    if bad:
        print("  failed :")
        for d, why in bad:
            print(f"     {d:<8}{why}")
        print("\n  For these, use DOWNLOAD_SNIPPET.md and save them by hand.")
    if ok:
        print(f"\nNext:  python3 pipeline/import_saved.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
