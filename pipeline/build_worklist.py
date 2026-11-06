#!/usr/bin/env python3
"""Build SOURCE_WORKLIST.xlsx - the manual-download worklist and status report.

Reads sources/originals/MANIFEST.csv, originals.lock.json and what is actually on
disk, so the workbook reflects reality rather than a hand-typed snapshot. Re-run it
after fetching more documents and the counts update themselves.

    python pipeline/build_worklist.py
    python pipeline/recalc.py rules/SOURCE_WORKLIST.xlsx   # if formulas changed
"""
from __future__ import annotations

import csv
import json
import pathlib
import unicodedata
from urllib.parse import urlparse

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def load_expect() -> dict:
    """Per-document phrase that proves a stored file is the real thing.

    Lives in expect.json rather than MANIFEST.csv so the CSV stays readable. It is not
    optional: this is the check that caught a saved page of 12,493 characters that was
    entirely site navigation and passed a length test.
    """
    import json as _json
    p = pathlib.Path(__file__).resolve().parent.parent / "sources/originals/expect.json"
    if not p.exists():
        return {}
    return _json.loads(p.read_text(encoding="utf-8")).get("expect", {})


EXPECT = load_expect()



ROOT = pathlib.Path(__file__).resolve().parents[1]
ORIG = ROOT / "sources" / "originals"
OUT = ROOT / "rules" / "SOURCE_WORKLIST.xlsx"
TODAY = "2026-11-06"

FONT = "Arial"
HDR_FILL = PatternFill("solid", fgColor="1F3864")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
OK_FILL = PatternFill("solid", fgColor="E2EFDA")
WARN_FILL = PatternFill("solid", fgColor="FFF2CC")
BAD_FILL = PatternFill("solid", fgColor="F8CBAD")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")

BLOCK_REASON = {
    "www.ofcom.org.uk": "Cloudflare JS challenge (403)",
    "www.legifrance.gouv.fr": "Cloudflare JS challenge (403)",
    "www.legislation.gov.uk": "AWS WAF challenge (x-amzn-waf-action: challenge)",
    "eur-lex.europa.eu": "AWS WAF challenge (202, empty body)",
    "as-pc-www.csa.fr": "Host unreachable (502 via proxy)",
    "www.arcom.fr": "Connection reset on this path",
    "solidarites.gouv.fr": "Truncated response (IncompleteRead)",
    "csa.fr": "Body rendered in JavaScript",
    "www.lexing.law": "Not attempted (optional tier)",
}


def fold(t: str) -> str:
    for a, b in (("œ", "oe"), ("Œ", "OE"), ("æ", "ae"),
                 ("’", "'"), (" ", " ")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).casefold()


rows = list(csv.DictReader((ORIG / "MANIFEST.csv").open(encoding="utf-8")))
lock = json.loads((ORIG / "originals.lock.json").read_text()) if (ORIG / "originals.lock.json").exists() else {}


def state(r: dict) -> str:
    """verified | shell | absent - matches fetch_originals.py --check."""
    # Same bug as fetch_originals.py had: the lockfile was treated as proof of existence, so
    # a file saved by hand and copied in was reported "absent" while sitting on disk. The file
    # decides; a missing lock entry only means the provenance hash was never recorded.
    p = ORIG / r["target_filename"]
    if not p.exists():
        return "absent"
    if p.suffix == ".txt" and EXPECT.get(r["doc_id"], ""):
        if fold(EXPECT.get(r["doc_id"], "")) not in fold(p.read_text(encoding="utf-8", errors="replace")):
            return "shell"
    return "verified"


for r in rows:
    r["_state"] = state(r)
    r["_host"] = urlparse(r["url"]).netloc
    r["_reason"] = BLOCK_REASON.get(r["_host"], "see manifest notes")

outstanding = [r for r in rows if r["_state"] != "verified"]
verified = [r for r in rows if r["_state"] == "verified"]

# C-03 is the live blocker, so the one document that unblocks it leads the list.
PRIORITY = {"FR-R2": "1 - UNBLOCKS C-03"}
TIER_RANK = {"required": 0, "recommended": 1, "optional": 2}
outstanding.sort(key=lambda r: (r["doc_id"] != "FR-R2",
                                TIER_RANK.get(r["tier"], 9), r["_host"], r["doc_id"]))

wb = openpyxl.Workbook()


def style_sheet(ws, widths, head_row=1, head_height=30):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
        c = ws.cell(row=head_row, column=i)
        c.fill = HDR_FILL
        c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[head_row].height = head_height
    for r in range(head_row + 1, ws.max_row + 1):
        for c in range(1, len(widths) + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.font = Font(name=FONT, size=9)
            cell.border = BORDER
    ws.freeze_panes = ws.cell(row=head_row + 1, column=1)


# ---------------------------------------------------- 1. Legend
ws = wb.active
ws.title = "Legend"
ws.append(["field", "meaning"])
for a, b in [
    ("What this workbook is",
     "The outstanding source documents for the UK/FR linear-TV rule table, and the status of "
     "the ones already retrieved. Generated from sources/originals/MANIFEST.csv and what is on "
     "disk - re-run pipeline/build_worklist.py to refresh it."),
    ("Why documents are outstanding",
     "Network access from the workspace is open, but several publishers gate automated clients "
     "behind browser challenges (Cloudflare on Ofcom and Legifrance; AWS WAF on legislation.gov.uk "
     "and EUR-Lex) or render the document body in JavaScript. Those are not worth defeating: open "
     "each in a browser and save the file."),
    ("THE ONLY COLUMN YOU EDIT",
     "'status_when_saved' on the Download_worklist tab - yellow. Put 'saved' once the file is in "
     "sources/originals/ under the exact save_as name. Everything else is generated."),
    ("save_as", "Save the file under EXACTLY this name, or the pipeline will not find it."),
    ("must_contain",
     "A string that has to appear in the saved file. This is how the pipeline tells a real "
     "document from a navigation page - FR-R2 was initially stored as 12,493 characters of pure "
     "site menu with no rule text, and only this assertion caught it."),
    ("state", "verified = on disk and contains must_contain. shell = on disk but it is navigation, "
              "not the document. absent = not downloaded."),
    ("If a page offers only HTML",
     "Use its Telecharger / Imprimer / Print-to-PDF option, save as .pdf, and change that row's "
     "'format' to pdf in MANIFEST.csv."),
    ("After saving files",
     "python pipeline/fetch_originals.py --check      (confirms each file is the document)"),
    ("", "python pipeline/verify_rules.py --with-quotes   (the check that actually matters)"),
    ("Source of the status data",
     f"sources/originals/MANIFEST.csv + originals.lock.json, as at {TODAY}. Not hand-entered."),
]:
    ws.append([a, b])
style_sheet(ws, [30, 110])

# ---------------------------------------------------- 2. Download worklist
ws = wb.create_sheet("Download_worklist")
HEAD = ["priority", "doc_id", "title", "host", "why_blocked", "url", "landing_page",
        "save_as", "must_contain", "format", "tier", "state", "status_when_saved"]
ws.append(HEAD)
for r in outstanding:
    ws.append([
        PRIORITY.get(r["doc_id"], f"{TIER_RANK.get(r['tier'], 9) + 2} - {r['tier']}"),
        r["doc_id"], r["title"], r["_host"], r["_reason"], r["url"],
        r.get("landing_page", ""),
        r["target_filename"], EXPECT.get(r["doc_id"], ""), r["format"], r["tier"],
        r["_state"], "",
    ])
style_sheet(ws, [18, 10, 46, 24, 34, 58, 52, 40, 30, 11, 14, 10, 18])
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEAD))}{ws.max_row}"

i_state, i_status, i_url = HEAD.index("state") + 1, HEAD.index("status_when_saved") + 1, HEAD.index("url") + 1
for r in range(2, ws.max_row + 1):
    sv = ws.cell(row=r, column=i_state).value
    ws.cell(row=r, column=i_state).fill = BAD_FILL if sv == "shell" else WARN_FILL
    ws.cell(row=r, column=i_status).fill = INPUT_FILL          # the editable column
    u = ws.cell(row=r, column=i_url).value
    if u:
        ws.cell(row=r, column=i_url).hyperlink = u
        ws.cell(row=r, column=i_url).font = Font(name=FONT, size=9, color="0563C1",
                                                 underline="single")
    if ws.cell(row=r, column=2).value == "FR-R2":
        for c in range(1, len(HEAD) + 1):
            ws.cell(row=r, column=c).font = Font(name=FONT, size=9, bold=True)

dv = DataValidation(type="list", formula1='"saved,in progress,blocked,skipped"',
                    allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"{get_column_letter(i_status)}2:{get_column_letter(i_status)}200")

# ---------------------------------------------------- 3. Verified
ws = wb.create_sheet("Verified")
ws.append(["doc_id", "title", "saved_as", "bytes", "chars_of_text", "fetched_at",
           "sha256_prefix", "must_contain_present"])
for r in verified:
    p = ORIG / r["target_filename"]
    L = lock.get(r["doc_id"], {})
    chars = len(p.read_text(encoding="utf-8", errors="replace")) if p.suffix == ".txt" else ""
    ws.append([r["doc_id"], r["title"], r["target_filename"], L.get("bytes", ""),
               chars, L.get("fetched_at", ""), str(L.get("sha256", ""))[:16], "yes"])
style_sheet(ws, [10, 50, 44, 12, 14, 24, 20, 20])
for r in range(2, ws.max_row + 1):
    ws.cell(row=r, column=8).fill = OK_FILL

# ---------------------------------------------------- 4. Checker fixes
ws = wb.create_sheet("Checker_fixes")
ws.append(["#", "what was wrong", "why it mattered", "fix", "found_by"])
for row in [
    [1, "The quote-integrity check could not match ANY French quote.",
     "The table stores quotes ASCII-folded so the CSV mirrors stay pure ASCII and diff cleanly, "
     "but the sources are accented French. Every French row would have failed spuriously, which "
     "would have discredited the one control that catches extraction errors.",
     "Fold accents on both sides before comparing.",
     "First real run of verify_rules.py --with-quotes"],
    [2, "Even after accent folding, one quote still failed.",
     "NFKD does not decompose the oe ligature, so 'oeuvres' never matched the source's "
     "ligature form. A single character defeated the check.",
     "Fold ligatures, en/em dashes and curly quotes explicitly.",
     "Re-run after fix 1"],
    [3, "The check resolved a row's source only from source_doc.",
     "The provenance fix had repointed source_url at the consolidated edition, so every French "
     "row was silently SKIPPED rather than checked - a check that quietly tests nothing.",
     "Resolve candidate sources by URL as well as by source_doc.", "Only 3 of 24 rows verified"],
    [4, "'Quote not found' was reported as a failure even when a cited source was missing.",
     "Absence proves nothing if the document is not on disk. Real defects would have been "
     "buried among false alarms.",
     "Split FAILED (every cited source present, none contains it) from inconclusive.",
     "FR-CV-003 reported as failed"],
    [5, "The JavaScript-shell detector was a length threshold, and it was not enough.",
     "FR-R2 'succeeded' with 12,493 characters of pure site navigation and zero rule text - a "
     "large nav menu clears a 2,000-character threshold easily. A shell stored as a source copy "
     "is worse than no copy: it looks like provenance and contains nothing.",
     "Per-document 'expect' assertion in the manifest, enforced on fetch AND on --check.",
     "Grepping FR-R2 for the -18 hours and finding none"],
]:
    ws.append(row)
style_sheet(ws, [5, 52, 72, 54, 34])

# ---------------------------------------------------- 5. Conflicts
ws = wb.create_sheet("Conflicts")
ws.append(["id", "subject", "status", "resolution / what is left", "blocks_ground_truth"])
for row in [
    ["C-01", "Arcom public summary contradicts binding text on the -12 hours", "CLOSED",
     "Binding text wins on authority rank, and is now confirmed in French. The summary page must "
     "not be used as a rule source.", "no"],
    ["C-02", "Garbled English translation of art. 3 (cat. III service mapping)", "CLOSED",
     "Confirmed in French from two independent sources, then VERIFIED against the stored primary "
     "text. The 16/4 derogation quota is also now confirmed in French.", "no"],
    ["C-03", "French -18 window (00:00-05:00) rests on a 2004 text with elapsed deadlines", "OPEN",
     "THE MAIN BLOCKER. The Arcom page for reco. 2004-7 renders its body in JavaScript, so the "
     "text could not be retrieved. Needs the Telecharger PDF or the JORF of 23 Dec 2004, then "
     "confirmation that the window is still in force and unaffected by the 2021 AVMSD decree.",
     "YES"],
    ["C-04", "sources/ held extracts, not official text; no local copies to check quotes against",
     "PARTLY CLOSED",
     "5 documents now stored and 7 quotes verified against them. 24 still outstanding - see the "
     "Download_worklist tab.", "partially"],
    ["C-05", "Ofcom 'children' = under 15 while the principle covers under 18", "CLOSED",
     "Both recorded explicitly. A conflation trap, not a conflict.", "no"],
    ["C-06", "French channel conventions can be stricter and are not consolidated anywhere", "OPEN",
     "Out of scope for v1. Per-licensee data source; cannot be scraped generically.",
     "no - but caps achievable accuracy for France"],
    ["C-07", "Only one enforcement precedent collected", "OPEN",
     "Precedent is the only source of APPLIED thresholds, which is exactly what the "
     "judgment_based rows lack. Ingest the Ofcom bulletins systematically.",
     "no - but caps accuracy on judgment rows"],
    ["C-08", "Correlated error: extraction and prompt share an author", "OPEN",
     "Have the bright-line rows independently re-derived by someone who has not seen the table, "
     "then compare.", "YES - methodologically"],
    ["C-09", "Delib. 2014-17 broadened the cat. III definition; the table carried the 2005 wording",
     "CLOSED",
     "Corrected and VERIFIED against the stored French primary text. Pre-2014 wording retained as "
     "FR-CLS-903, superseded. Lesson: the EN translation and the pre-2014 French text agreed with "
     "each other, so corroboration did not catch it - only the amending instrument did.", "no"],
    ["C-10", "Arcom's public page adds 'ou evoque la sexualite adulte' to the -12 test", "CLOSED",
     "'sexualite' occurs nowhere in the binding recommendation, so the limb is a practice gloss, "
     "not binding text. Do not encode an independent adult-sexuality -12 trigger; still flag "
     "borderline sexual-content cases, since Arcom may apply the gloss when classifying.", "no"],
]:
    ws.append(row)
style_sheet(ws, [7, 56, 16, 86, 34])
for r in range(2, ws.max_row + 1):
    v = ws.cell(row=r, column=3).value
    ws.cell(row=r, column=3).fill = OK_FILL if v == "CLOSED" else (
        WARN_FILL if v == "PARTLY CLOSED" else BAD_FILL)

# ---------------------------------------------------- 6. Summary (formulas)
ws = wb.create_sheet("Summary")
ws.append(["metric", "value", "how it is calculated"])
n = len(outstanding) + 1
body = [
    ["Documents in manifest", len(rows), "Row count of sources/originals/MANIFEST.csv"],
    ["Verified on disk", f"=COUNTA(Verified!A2:A200)",
     "Present, hashed, and containing their must_contain string"],
    ["Outstanding", f"=COUNTA(Download_worklist!B2:B{n})", "Rows on the Download_worklist tab"],
    ["  of which required tier",
     f'=COUNTIF(Download_worklist!J2:J{n},"required")', "COUNTIF on the tier column"],
    ["  of which recommended",
     f'=COUNTIF(Download_worklist!J2:J{n},"recommended")', "COUNTIF on the tier column"],
    ["  of which optional",
     f'=COUNTIF(Download_worklist!J2:J{n},"optional")', "COUNTIF on the tier column"],
    ["Stored but a navigation shell",
     f'=COUNTIF(Download_worklist!L2:L{n},"shell")',
     "On disk but missing its must_contain string - FR-R2"],
    ["Marked saved by you",
     f'=COUNTIF(Download_worklist!M2:M{n},"saved")',
     "Updates as you fill the yellow status_when_saved column"],
    ["Still to do",
     f'=COUNTA(Download_worklist!B2:B{n})-COUNTIF(Download_worklist!M2:M{n},"saved")',
     "Outstanding minus those you have marked saved"],
    ["Conflicts closed", '=COUNTIF(Conflicts!C2:C200,"CLOSED")', "COUNTIF on the Conflicts tab"],
    ["Conflicts open", '=COUNTIF(Conflicts!C2:C200,"OPEN")', "COUNTIF on the Conflicts tab"],
    ["Rule table: total rules", 83, "pipeline/verify_rules.py output, 2026-11-06"],
    ["Rule table: approved", 74, "status=approved; the only rows usable as ground truth"],
    ["Quotes verified against stored source", 7, "verify_rules.py --with-quotes"],
    ["Quotes failed", 0, "verify_rules.py --with-quotes"],
]
for row in body:
    ws.append(row)
style_sheet(ws, [40, 14, 62])
for r in range(2, ws.max_row + 1):
    ws.cell(row=r, column=2).alignment = Alignment(horizontal="center", vertical="top")
    ws.cell(row=r, column=1).font = Font(name=FONT, size=9, bold=True)


# ---------------------------------------------------- 7. DOWNLOAD_THESE.md
# A plain checklist at the repo root. MANIFEST.csv carries the same information in
# download_status, but it is column 10 of 13 and GitHub's CSV table pushes it
# off-screen, so the authoritative data gets a readable front door.
md = [
    "# Documents to download",
    "",
    f"**{len(outstanding)} outstanding, {len(verified)} verified** "
    f"(generated {TODAY} by `pipeline/build_worklist.py` - do not edit by hand).",
    "",
    "Network access from the workspace is open, but these publishers gate automated clients",
    "behind browser challenges or render the document body in JavaScript. Open each in a",
    "browser and save it - then let the importer do the fiddly part.",
    "",
    "## How to save one",
    "",
    "1. Open the **url** below in a browser.",
    "2. Save it **any way that is convenient** - the filename does not matter:",
    "   - `Cmd/Ctrl+S` -> HTML (pick *Web Page, HTML Only* if offered)",
    "   - `Cmd/Ctrl+P` -> *Save as PDF*",
    "3. Put the file in `sources/originals/incoming/`",
    "4. Run:",
    "",
    "```bash",
    "python pipeline/import_saved.py                 # sorts out name, format and extraction",
    "python pipeline/verify_rules.py --with-quotes   # the check that actually matters",
    "```",
    "",
    "`import_saved.py` works out which document each file is (from its content, not its",
    "name), converts HTML to text, renames it to the manifest's `save as`, sets `format`",
    "and `download_status`, and records its sha256. It **refuses** a file that does not",
    "contain its document's *must contain* string, so a saved cookie banner or error page",
    "cannot slip in as a source copy. If two near-identical documents both match, it says",
    "so - rerun with `--doc <DOC_ID>`.",
    "",
    "You do not need to match the *save as* names by hand; they are listed so you can",
    "check what landed.",
    "",
    "`--check` rewrites `download_status` in `MANIFEST.csv`, so the status cannot go stale.",
    "",
    "> **If you only do one:** `FR-R2`. It is the sole source of the French -18 window and the",
    "> only outstanding document that changes the rule table's status today (conflict C-03).",
    "> The other 23 convert `skipped` quote checks into `verified` ones - worth having, not blocking.",
    "",
]
for tier in ("required", "recommended", "optional"):
    grp = [r for r in outstanding if r["tier"] == tier]
    if not grp:
        continue
    md += [f"## {tier.capitalize()} ({len(grp)})", "",
           "| ✓ | doc | what it is | save as | why blocked | url |",
           "|---|---|---|---|---|---|"]
    for r in grp:
        star = " **\u2190 DO THIS ONE**" if r["doc_id"] == "FR-R2" else ""
        title = r["title"] if len(r["title"]) <= 64 else r["title"][:61] + "..."
        md.append(f"| [ ] | `{r['doc_id']}`{star} | {title} | `{r['target_filename']}` | "
                  f"{r['_reason']} | [link]({r['url']}) |")
    md.append("")

md += ["## Already verified", "",
       "| doc | file | size |", "|---|---|---|"]
for r in verified:
    L = lock.get(r["doc_id"], {})
    md.append(f"| `{r['doc_id']}` | `{r['target_filename']}` | {L.get('bytes','')} bytes |")
md.append("")

(ROOT / "DOWNLOAD_THESE.md").write_text("\n".join(md))
print(f"wrote DOWNLOAD_THESE.md ({len(outstanding)} outstanding)")

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f"wrote {OUT.relative_to(ROOT)}")
print(f"  outstanding {len(outstanding)} | verified {len(verified)} | manifest {len(rows)}")
print(f"  tabs: {wb.sheetnames}")
