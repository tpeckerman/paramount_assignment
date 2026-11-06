# Documents to download

**16 outstanding, 3 verified** (generated 2026-11-06 by `pipeline/build_worklist.py` - do not edit by hand).

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

## Required (10)

| ✓ | doc | what it is | save as | why blocked | url |
|---|---|---|---|---|---|
| [ ] | `FR-R2` **← DO THIS ONE** | Recommandation 2004-7 du 15 decembre 2004 - category V progra... | `FR-R2_reco_2004-7_category_V.txt` | Connection reset on this path | [link](https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france) |
| [ ] | `FR-S2` | solidarites.gouv.fr - Classification et signaletique de la te... | `FR-S2_solidarites_classification.txt` | Truncated response (IncompleteRead) | [link](https://solidarites.gouv.fr/classification-et-signaletique-de-la-television) |
| [ ] | `FR-L1` | Loi 86-1067 du 30 septembre 1986 (arts. 1 and 15) | `FR-L1_loi_86-1067.txt` | Cloudflare JS challenge (403) | [link](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205) |
| [ ] | `EU-D1` | AVMSD Directive 2010/13/EU article 6a (consolidated) | `EU-D1_avmsd_article_6a.pdf` | AWS WAF challenge (x-amzn-waf-action: challenge) | [link](https://www.legislation.gov.uk/eudr/2010/13/article/6a/data.pdf) |
| [ ] | `UK-L1` | Communications Act 2003 section 319 | `UK-L1_communications_act_2003_s319.pdf` | AWS WAF challenge (x-amzn-waf-action: challenge) | [link](https://www.legislation.gov.uk/ukpga/2003/21/section/319/data.pdf) |
| [ ] | `UK-G1` | Guidance - Observing the watershed on television and music vi... | `UK-G1_ofcom_watershed_music_videos.pdf` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf) |
| [ ] | `UK-M1` | Statement - Review of the mandatory daytime protection rules | `UK-M1_ofcom_mandatory_daytime_protection.pdf` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf) |
| [ ] | `UK-S1` | Broadcasting Code Section One - Protecting the Under-Eighteens | `UK-S1_ofcom_code_section_1.txt` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-one-protecting-under-eighteens) |
| [ ] | `UK-S2` | Broadcasting Code Section Two - Harm and Offence | `UK-S2_ofcom_code_section_2.txt` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence) |
| [ ] | `UK-S4` | Ofcom Broadcasting Code, Section Four: Religion | `UK-S4_ofcom_code_section_4.txt` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-four-religion) |

## Recommended (6)

| ✓ | doc | what it is | save as | why blocked | url |
|---|---|---|---|---|---|
| [ ] | `FR-S1c` | La signaletique jeunesse (CSA/Arcom FRENCH public page) | `FR-S1c_signaletique_jeunesse_fr.txt` | Host unreachable (502 via proxy) | [link](https://as-pc-www.csa.fr/Proteger/Protection-de-la-jeunesse-et-des-mineurs/La-signaletique-jeunesse) |
| [ ] | `EU-D1b` | Directive (EU) 2018/1808 (amending directive) | `EU-D1b_directive_2018_1808.pdf` | AWS WAF challenge (202, empty body) | [link](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32018L1808) |
| [ ] | `UK-L2` | Audiovisual Media Services Regulations 2020 (SI 2020/1062) ex... | `UK-L2_avms_regulations_2020_note.txt` | AWS WAF challenge (x-amzn-waf-action: challenge) | [link](https://www.legislation.gov.uk/uksi/2020/1062/note/made) |
| [ ] | `UK-G2` | Guidance Notes Section One | `UK-G2_ofcom_guidance_section_1.pdf` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/__data/assets/pdf_file/0017/24704/section1.pdf) |
| [ ] | `UK-G3` | Guidance Notes Section Two | `UK-G3_ofcom_guidance_section_2.pdf` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/__data/assets/pdf_file/0023/104657/Section-2-Guidance-Notes.pdf) |
| [ ] | `UK-P1` | Enforcement decision - Toofan NTV 29 May 2026 (Rule 1.3 breach) | `UK-P1_ofcom_decision_toofan.pdf` | Cloudflare JS challenge (403) | [link](https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf) |

## Already verified

| doc | file | size |
|---|---|---|
| `FR-R1c` | `FR-R1c_reco_2005-5_arcom_fr.txt` | 15662 bytes |
| `FR-V1` | `FR-V1_arcom_mise_en_demeure_C8.pdf` | 251754 bytes |
| `FR-C1` | `FR-C1_cnc_classification.txt` | 23415 bytes |
