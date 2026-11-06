#!/usr/bin/env python3
"""Download the original regulatory source documents listed in MANIFEST.csv.

    python pipeline/fetch_originals.py                 # fetch required + recommended
    python pipeline/fetch_originals.py --tier required # fetch only the required set
    python pipeline/fetch_originals.py --check         # verify what is already on disk
    python pipeline/fetch_originals.py --only FR-R1 FR-A2b

By default only the CURRENT version of each document is fetched - that is what the
rules are decided against. Superseded originals and amending instruments are fetched
only with --include-historical; they exist so you can diff what an amendment changed,
which is how conflict C-09 was caught.

Every entry resolves to a TEXT or PDF file on disk. Entries with format=pdf are
stored as fetched; entries with format=html2txt are extracted to readable .txt,
because a JavaScript shell is useless as a source copy and cannot be searched by
the quote-integrity check. A short extraction is reported as a failure.

Writes each file to sources/originals/ and records its sha256 in
sources/originals/originals.lock.json. That lockfile is what makes the
quote-integrity check in verify_rules.py possible, and what tells you a source
document has changed under you.

Why this script exists rather than the files being committed already: the
environment that produced the extracts had no outbound network access to
ofcom.org.uk, arcom.fr, legifrance.gouv.fr, bbfc.co.uk or eur-lex.europa.eu
(all six refused at the egress proxy). See sources/99_EXTRACTION_NOTES_AND_LIMITS.md,
conflict C-04. Run this from any machine with ordinary internet access.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "sources" / "originals"
MANIFEST = ORIGINALS / "MANIFEST.csv"
LOCKFILE = ORIGINALS / "originals.lock.json"

# A plain, honest client string. Do not put a personal email address here.
UA = "paramount-assignment-source-fetcher/1.0 (regulatory research; contact via repo)"

TIER_ORDER = {"required": 0, "recommended": 1, "optional": 2}


def load_manifest() -> list[dict]:
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


TAG = re.compile(rb"<(script|style|noscript)\b[^>]*>.*?</\1>",
                 re.IGNORECASE | re.DOTALL)


def html_to_text(raw: bytes) -> str:
    """Crude but dependency-free: drop scripts/styles, strip tags, unescape."""
    import html as _html
    body = TAG.sub(b" ", raw)
    txt = body.decode("utf-8", "replace")
    txt = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", "\n", txt,
                 flags=re.IGNORECASE)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    txt = re.sub(r"\n\s*\n\s*\n+", "\n\n", txt)
    return txt.strip()


# Below this many characters of extracted text, the page is almost certainly a
# JavaScript shell rather than the document. Legifrance and Arcom both do this.
MIN_TEXT_CHARS = 2000


def _fold(t: str) -> str:
    """Fold accents, ligatures, dashes and quotes so ASCII `expect` strings match
    accented French source text. NFKD alone does not decompose oe/ae ligatures."""
    import unicodedata
    for a, b in (("\u0153", "oe"), ("\u0152", "OE"), ("\u00e6", "ae"),
                 ("\u00c6", "AE"), ("\u2014", "-"), ("\u2013", "-"),
                 ("\u2019", "'"), ("\u2018", "'"), ("\u00a0", " ")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t).casefold()


def fetch(url: str, dest: Path, fmt: str = "pdf", expect: str = "",
          timeout: int = 60) -> tuple[bool, str]:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
        "Accept-Language": "fr,en;q=0.8",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            ctype = resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"unreachable: {e.reason}"
    except Exception as e:                                    # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"

    if not body:
        return False, "empty response"

    if fmt == "pdf":
        if not body.startswith(b"%PDF"):
            return False, f"not a PDF (content-type {ctype!r}, {len(body)} bytes)"
        dest.write_bytes(body)
        if expect:
            try:
                import io as _io
                import pypdf
                txt = "\n".join((p.extract_text() or "")
                                for p in pypdf.PdfReader(_io.BytesIO(body)).pages)
                if _fold(expect) not in _fold(txt):
                    return False, (f"PDF stored but expected text {expect!r} is absent "
                                   f"({len(txt)} chars extracted) - wrong document?")
            except ImportError:
                return True, f"PDF, {len(body)} bytes (expect not checked: pip install pypdf)"
        return True, f"PDF, {len(body)} bytes"

    # html2txt: store readable TEXT, not markup. Everything in this folder is
    # text or PDF, so the quote-integrity check can always search it.
    text = html_to_text(body)
    dest.write_text(text, encoding="utf-8")
    if len(text) < MIN_TEXT_CHARS:
        return False, (f"only {len(text)} chars of text extracted - almost certainly a "
                       f"JavaScript shell. Saved for inspection; use the page's "
                       f"Telecharger/PDF link instead and set format=pdf")
    # Length alone is not enough: a large navigation menu clears the threshold
    # while carrying no rule text at all. Require the document's own content.
    if expect and _fold(expect) not in _fold(text):
        return False, (f"{len(text)} chars extracted but expected text {expect!r} is "
                       f"ABSENT - this is site navigation, not the document. Saved for "
                       f"inspection; use the page's Telecharger/PDF link and set format=pdf")
    return True, f"text, {len(text)} chars (from {len(body)} bytes of HTML)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tier", default="recommended",
                    choices=["required", "recommended", "optional"],
                    help="fetch this tier and everything above it (default: recommended)")
    ap.add_argument("--only", nargs="+", metavar="DOC_ID",
                    help="fetch just these doc_ids")
    ap.add_argument("--check", action="store_true",
                    help="do not download; report what is present and whether hashes match")
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file is already present")
    ap.add_argument("--include-historical", action="store_true",
                    help="also fetch superseded originals and amending instruments. "
                         "By default only the CURRENT version of each document is fetched, "
                         "since that is what the rules are decided against. The historical "
                         "copies exist only to diff what an amendment changed - which is how "
                         "C-09 was caught.")
    args = ap.parse_args()

    ORIGINALS.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()
    lock = json.loads(LOCKFILE.read_text()) if LOCKFILE.exists() else {}

    if args.only:
        wanted = {d.upper() for d in args.only}
        rows = [r for r in rows if r["doc_id"].upper() in wanted]
        missing = wanted - {r["doc_id"].upper() for r in rows}
        if missing:
            print(f"unknown doc_id(s): {sorted(missing)}", file=sys.stderr)
            return 2
    else:
        cutoff = TIER_ORDER[args.tier]
        rows = [r for r in rows if TIER_ORDER.get(r["tier"], 9) <= cutoff]
        if not args.include_historical:
            before = len(rows)
            rows = [r for r in rows
                    if r.get("version_status", "current") == "current"]
            skipped = before - len(rows)
            if skipped:
                print(f"  ({skipped} historical doc(s) skipped - "
                      f"pass --include-historical to fetch superseded originals "
                      f"and amending instruments)")

    if args.check:
        drift = absent = ok = 0
        for r in rows:
            dest = ORIGINALS / r["target_filename"]
            if not dest.exists():
                print(f"  ABSENT   {r['doc_id']:8s} {r['target_filename']}")
                absent += 1
            elif (r.get("expect") and dest.suffix == ".txt"
                  and _fold(r["expect"]) not in _fold(
                      dest.read_text(encoding="utf-8", errors="replace"))):
                print(f"  SHELL    {r['doc_id']:8s} {r['target_filename']}"
                      "  <- on disk but expected text absent: navigation, not the document")
                drift += 1
            elif r["doc_id"] in lock and lock[r["doc_id"]]["sha256"] != sha256(dest):
                print(f"  CHANGED  {r['doc_id']:8s} {r['target_filename']}"
                      "  <- source document changed since it was locked")
                drift += 1
            else:
                ok += 1
        print(f"\n{ok} ok, {absent} absent, {drift} changed  "
              f"({len(rows)} in scope, tier<={args.tier})")
        if drift:
            print("\nA CHANGED file means the regulator has altered the document. "
                  "Re-extract the affected rules and version the old ones "
                  "(see pipeline/COLAB_rule_pipeline_starter.ipynb, cell 4).")
        return 1 if (absent or drift) else 0

    failures: list[tuple[str, str, str]] = []
    for r in rows:
        doc_id, dest = r["doc_id"], ORIGINALS / r["target_filename"]
        if dest.exists() and not args.force:
            print(f"  skip     {doc_id:8s} already present")
            continue

        print(f"  fetch    {doc_id:8s} {r['url'][:78]}")
        ok, detail = fetch(r["url"], dest, r.get("format", "pdf"),
                           r.get("expect", ""))
        if ok:
            digest = sha256(dest)
            prior = lock.get(doc_id, {}).get("sha256")
            lock[doc_id] = {
                "sha256": digest,
                "url": r["url"],
                "filename": r["target_filename"],
                "bytes": dest.stat().st_size,
                "fetched_at": dt.datetime.now(dt.timezone.utc)
                                .replace(microsecond=0).isoformat(),
            }
            note = ""
            if prior and prior != digest:
                note = "  <- CHANGED since last lock"
            print(f"           ok  {detail}{note}")
        else:
            print(f"           FAILED  {detail}")
            failures.append((doc_id, r["url"], detail))

    LOCKFILE.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    print(f"\nlockfile: {LOCKFILE.relative_to(ROOT)}  ({len(lock)} entries)")

    if failures:
        print(f"\n{len(failures)} failure(s):")
        for doc_id, url, detail in failures:
            print(f"  {doc_id:8s} {detail}\n           {url}")
        print("\nIf these failed with 403/unreachable from a sandboxed environment, the host "
              "is almost certainly not on the egress allowlist. Run this from an unrestricted "
              "machine, or add the domain under claude.ai Settings > Capabilities.")
        print("If a Legifrance page came back as a JS shell rather than the text, use its "
              "'Telecharger' PDF link instead and update MANIFEST.csv.")
        return 1

    print("\nAll fetched. Next: python pipeline/verify_rules.py --with-quotes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
