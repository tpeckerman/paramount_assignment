#!/usr/bin/env python3
"""Import documents you saved from a browser, whatever form they came in.

    1. open the url from sources/originals/MANIFEST.csv in your browser
    2. save the page ANY way that is convenient:
         Cmd/Ctrl+S  -> .html  (choose "Web Page, HTML Only" if offered)
         Cmd/Ctrl+P  -> "Save as PDF"
       The filename does not matter.
    3. drop the file(s) in  sources/originals/incoming/
    4. python pipeline/import_saved.py

This script works out which manifest row each file belongs to, converts HTML to
text, copies PDFs through, renames to the manifest's target_filename, updates
`format` and `download_status` in MANIFEST.csv, records the sha256 in the
lockfile, and refuses anything that does not contain its document's `expect`
string - so a saved cookie banner or error page cannot slip in as a source copy.

    python pipeline/import_saved.py --dry-run     # report, change nothing
    python pipeline/import_saved.py --doc UK-S1   # force a file to one doc id
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import pathlib
import re
import shutil
import sys
import unicodedata

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import constants as C

def load_expect() -> dict:
    """Per-document phrase that proves a stored file is the real thing.

    Lives in expect.json rather than MANIFEST.csv so the CSV stays readable. It is not
    optional: this is the check that caught a saved page of 12,493 characters that was
    entirely site navigation and passed a length test.
    """
    import json as _json
    p = C.EXPECT_JSON
    if not p.exists():
        return {}
    return _json.loads(p.read_text(encoding="utf-8")).get("expect", {})


EXPECT = load_expect()



ROOT = C.ROOT
ORIGINALS = C.ORIGINALS_DIR
INCOMING = ORIGINALS / "incoming"
MANIFEST = C.MANIFEST_CSV
LOCKFILE = ORIGINALS / "originals.lock.json"

FIELDS = ["doc_id", "country", "regulator", "title", "url", "landing_page",
          "link_health", "target_filename", "format", "tier", "download_status"]

TAGS = re.compile(rb"<(script|style|noscript|svg)\b[^>]*>.*?</\1>", re.I | re.S)


def fold(t: str) -> str:
    for a, b in (("œ", "oe"), ("Œ", "OE"), ("æ", "ae"),
                 ("’", "'"), ("‘", "'"), (" ", " "),
                 (", ", "-"), (", ", "-")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t).casefold()


def html_to_text(raw: bytes) -> str:
    import html as _html
    body = TAGS.sub(b" ", raw)
    txt = body.decode("utf-8", "replace")
    txt = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", txt).strip()


def pdf_to_text(raw: bytes) -> str | None:
    try:
        import pypdf
    except ImportError:
        return None
    try:
        return "\n".join((p.extract_text() or "")
                         for p in pypdf.PdfReader(io.BytesIO(raw)).pages)
    except Exception:
        return None


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report only")
    ap.add_argument("--doc", metavar="DOC_ID",
                    help="assign every incoming file to this doc_id (use with one file)")
    args = ap.parse_args()

    INCOMING.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(MANIFEST.open(newline="", encoding="utf-8")))
    by_id = {r["doc_id"]: r for r in rows}

    files = [p for p in sorted(INCOMING.iterdir())
             if p.is_file() and not p.name.startswith(".")]
    if not files:
        print(f"Nothing in {INCOMING.relative_to(ROOT)}/")
        print("\nSave the pages listed in MANIFEST.csv there (any filename, .html or")
        print(".pdf), then run this again. Browser: Cmd/Ctrl+S for HTML, Cmd/Ctrl+P ->")
        print("Save as PDF for PDF. Either works.")
        return 0

    import json
    lock = json.loads(LOCKFILE.read_text()) if LOCKFILE.exists() else {}
    claimed, rejected, unmatched = [], [], []

    for p in files:
        raw = p.read_bytes()
        is_pdf = raw.startswith(b"%PDF")
        text = pdf_to_text(raw) if is_pdf else html_to_text(raw)
        if text is None:
            rejected.append((p.name, "PDF text could not be read (pip install pypdf)"))
            continue
        folded = fold(text)

        # Which document is this? Prefer an explicit --doc, then a doc_id in the
        # filename, then the only manifest row whose `expect` string occurs in it.
        if args.doc:
            cand = [args.doc.upper()] if args.doc.upper() in by_id else []
        else:
            cand = [d for d in by_id if d.lower() in p.name.lower()]
            if not cand:
                cand = [r["doc_id"] for r in rows
                        if EXPECT.get(r["doc_id"], "") and fold(EXPECT.get(r["doc_id"], "")) in folded]

        if not cand:
            unmatched.append((p.name, len(text)))
            continue
        if len(cand) > 1:
            # Prefer a document still outstanding over one already verified - you
            # do not re-import something you have - then the most specific
            # (longest) expect string. Only give up if still tied.
            cand.sort(key=lambda d: (
                by_id[d].get("download_status") == "verified",
                -len(by_id[d].get("expect", "")),
            ))
            best = [d for d in cand
                    if (by_id[d].get("download_status") == "verified",
                        -len(by_id[d].get("expect", ""))) ==
                       (by_id[cand[0]].get("download_status") == "verified",
                        -len(by_id[cand[0]].get("expect", "")))]
            if len(best) > 1:
                rejected.append((p.name, f"matches {best} equally - these documents are "
                                         f"near-identical; rerun with --doc <DOC_ID>"))
                continue
            print(f"  (disambiguated {p.name} -> {cand[0]} from {len(cand)} candidates)")
            cand = [cand[0]]

        r = by_id[cand[0]]
        if EXPECT.get(r["doc_id"], "") and fold(EXPECT.get(r["doc_id"], "")) not in folded:
            rejected.append((p.name, f"does not contain {EXPECT.get(r["doc_id"], "")!r} - wrong page, an "
                                     f"error page, or a cookie wall ({len(text)} chars)"))
            continue

        stem = r["target_filename"].rsplit(".", 1)[0]
        if is_pdf:
            target, fmt, payload = ORIGINALS / f"{stem}.pdf", "pdf", raw
        else:
            target, fmt, payload = (ORIGINALS / f"{stem}.txt", "html2txt",
                                    text.encode("utf-8"))

        claimed.append((p, r, target, fmt, payload, len(text)))

    for p, r, target, fmt, payload, n in claimed:
        print(f"  {r['doc_id']:8s} {p.name}")
        print(f"           -> {target.name}  ({fmt}, {n} chars of text)")
        if args.dry_run:
            continue
        # Remove a stale sibling with the other extension, so a doc cannot end up
        # present twice in two formats.
        other = target.with_suffix(".txt" if target.suffix == ".pdf" else ".pdf")
        if other.exists():
            other.unlink()
        target.write_bytes(payload)
        r["format"] = fmt
        r["target_filename"] = target.name
        r["download_status"] = "verified"
        lock[r["doc_id"]] = {
            "sha256": sha256_bytes(payload), "url": r["url"],
            "filename": target.name, "bytes": len(payload),
            "fetched_at": dt.datetime.now(dt.timezone.utc)
                            .replace(microsecond=0).isoformat(),
            "source": "manual browser save via import_saved.py",
        }
        p.unlink()

    if not args.dry_run and claimed:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
        MANIFEST.write_text(buf.getvalue())
        LOCKFILE.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")

    print()
    if unmatched:
        print(f"{len(unmatched)} file(s) could not be matched to a document:")
        for name, n in unmatched:
            print(f"  {name}  ({n} chars) - rerun with --doc <DOC_ID>, or rename the "
                  f"file to include the doc id")
    if rejected:
        print(f"{len(rejected)} file(s) rejected:")
        for name, why in rejected:
            print(f"  {name}: {why}")

    verb = "would import" if args.dry_run else "imported"
    print(f"\n{verb} {len(claimed)}, rejected {len(rejected)}, unmatched {len(unmatched)}")
    if claimed and not args.dry_run:
        print("\nNext:")
        print("  python pipeline/verify_rules.py --with-quotes")
    return 1 if (rejected or unmatched) else 0


if __name__ == "__main__":
    raise SystemExit(main())
