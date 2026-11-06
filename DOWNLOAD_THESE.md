# Documents to download

**0 outstanding, 20 verified** (generated 2026-11-06 by `pipeline/build_worklist.py` - do not edit by hand).

Network access from the workspace is open, but these publishers gate automated clients
behind browser challenges or render the document body in JavaScript. Open each in a
browser and save it - then let the importer do the fiddly part.

## How to save one

1. Open the **url** below in a browser.
2. Save it **any way that is convenient** - the filename does not matter:
   - `Cmd/Ctrl+S` -> HTML (pick *Web Page, HTML Only* if offered)
   - `Cmd/Ctrl+P` -> *Save as PDF*
3. Put the file in `sources/originals/incoming/`
4. Run:

```bash
python pipeline/import_saved.py                 # sorts out name, format and extraction
python pipeline/verify_rules.py --with-quotes   # the check that actually matters
```

`import_saved.py` works out which document each file is (from its content, not its
name), converts HTML to text, renames it to the manifest's `save as`, sets `format`
and `download_status`, and records its sha256. It **refuses** a file that does not
contain its document's *must contain* string, so a saved cookie banner or error page
cannot slip in as a source copy. If two near-identical documents both match, it says
so - rerun with `--doc <DOC_ID>`.

You do not need to match the *save as* names by hand; they are listed so you can
check what landed.

`--check` rewrites `download_status` in `MANIFEST.csv`, so the status cannot go stale.

> **If you only do one:** `FR-R2`. It is the sole source of the French -18 window and the
> only outstanding document that changes the rule table's status today (conflict C-03).
> The other 23 convert `skipped` quote checks into `verified` ones - worth having, not blocking.

## Already verified

| doc | file | size |
|---|---|---|
| `UK-S1` | `UK-S1_ofcom_code_section_1.txt` |  bytes |
| `UK-S2` | `UK-S2_ofcom_code_section_2.txt` |  bytes |
| `UK-S3` | `UK-S3_ofcom_code_section_3.txt` |  bytes |
| `UK-S4` | `UK-S4_ofcom_code_section_4.txt` |  bytes |
| `UK-G1` | `UK-G1_ofcom_watershed_music_videos.pdf` |  bytes |
| `UK-G2` | `UK-G2_ofcom_guidance_section_1.pdf` |  bytes |
| `UK-G3` | `UK-G3_ofcom_guidance_section_2.pdf` |  bytes |
| `UK-M1` | `UK-M1_ofcom_mdp_statement.txt` |  bytes |
| `UK-P1` | `UK-P1_ofcom_decision_toofan.pdf` |  bytes |
| `UK-L1` | `UK-L1_communications_act_2003_s319.txt` | 18693 bytes |
| `UK-L2` | `UK-L2_avms_regulations_2020_note.txt` | 12976 bytes |
| `FR-R1c` | `FR-R1c_reco_2005-5_arcom_fr.txt` | 15662 bytes |
| `FR-R2` | `FR-R2_reco_2004-7_category_V.txt` | 12515 bytes |
| `FR-S1c` | `FR-S1c_signaletique_jeunesse_fr.txt` |  bytes |
| `FR-S2` | `FR-S2_solidarites_classification.txt` |  bytes |
| `FR-L1` | `FR-L1_loi_86-1067.txt` |  bytes |
| `FR-V1` | `FR-V1_arcom_mise_en_demeure_C8.pdf` | 251754 bytes |
| `FR-C1` | `FR-C1_cnc_classification.txt` | 23415 bytes |
| `EU-D1` | `EU-D1_avmsd_article_6a.txt` |  bytes |
| `EU-D1b` | `EU-D1b_directive_2018_1808.txt` |  bytes |
