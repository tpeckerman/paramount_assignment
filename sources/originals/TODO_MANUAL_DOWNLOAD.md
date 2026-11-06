# Manual download list

Generated 24 outstanding of 29 documents. 5 already verified on disk.

Network access is open from the workspace now, but these publishers gate automated
clients behind browser challenges (Cloudflake/AWS WAF) or render their body in
JavaScript. Those are not worth defeating - open each in a browser, save the file,
and drop it in this folder under **exactly** the filename in the `save as` column.

After saving:

```bash
python pipeline/fetch_originals.py --check      # confirms each file is the document, not a shell
python pipeline/verify_rules.py --with-quotes   # the check that matters
```

If a page only offers HTML, use its *Télécharger / Imprimer / Print to PDF* option,
save as `.pdf`, and change that row's `format` to `pdf` in `MANIFEST.csv`.

## REQUIRED (16)

### UK-S1, Broadcasting Code Section One - Protecting the Under-Eighteens
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0019/132076/Broadcast-code-Section-1.pdf
- **save as:** `UK-S1_ofcom_code_section_1.pdf`
- **must contain:** `appropriate scheduling`
- **why blocked:** Cloudflare JS challenge

### UK-S1b, Broadcasting Code Section One (HTML current version)
- **url:** https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-one-protecting-under-eighteens
- **save as:** `UK-S1b_ofcom_code_section_1.txt`
- **must contain:** `appropriate scheduling`
- **why blocked:** Cloudflare JS challenge

### UK-S2, Broadcasting Code Section Two - Harm and Offence
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0020/132077/Broadcast-Code-Section-2.pdf
- **save as:** `UK-S2_ofcom_code_section_2.pdf`
- **must contain:** `meaning of`
- **why blocked:** Cloudflare JS challenge

### UK-S2b, Broadcasting Code Section Two (HTML current version)
- **url:** https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-two-harm-offence
- **save as:** `UK-S2b_ofcom_code_section_2.txt`
- **must contain:** `generally accepted standards`
- **why blocked:** Cloudflare JS challenge

### UK-G1, Guidance - Observing the watershed on television and music videos
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf
- **save as:** `UK-G1_ofcom_watershed_music_videos.pdf`
- **must contain:** `watershed`
- **why blocked:** Cloudflare JS challenge

### UK-M1, Statement - Review of the mandatory daytime protection rules
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf
- **save as:** `UK-M1_ofcom_mandatory_daytime_protection.pdf`
- **must contain:** `mandatory daytime protection`
- **why blocked:** Cloudflare JS challenge

### UK-L1, Communications Act 2003 section 319
- **url:** https://www.legislation.gov.uk/ukpga/2003/21/section/319/data.pdf
- **save as:** `UK-L1_communications_act_2003_s319.pdf`
- **must contain:** `persons under the age of eighteen`
- **why blocked:** AWS WAF challenge (x-amzn-waf-action: challenge)

### FR-R1, Recommandation 2005-5 du 7 juin 2005 - signaletique jeunesse (JORF original)
- **url:** https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000446802
- **save as:** `FR-R1_reco_2005-5_jorf_original.txt`
- **must contain:** `categorie iii`
- **why blocked:** Cloudflare JS challenge

### FR-A1, Deliberation 2012-57 du 23 octobre 2012 modifying 2005-5
- **url:** https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/deliberation-du-23-octobre-2012-modifiant-la-recommandation-ndeg-2005-5-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des-programmes
- **save as:** `FR-A1_delib_2012-57.txt`
- **must contain:** `pictogramme`
- **why blocked:** connection reset on this path

### FR-A2, Deliberation 2014-17 du 5 mars 2014 modifying 2005-5
- **url:** https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/deliberation-no-2014-17-march-5-2014-amending-notice-no-2005-5-june-7-2005-television-service-editors-concerning-youth-signage-and-classification-programmes
- **save as:** `FR-A2_delib_2014-17.txt`
- **must contain:** `categorie iii`
- **why blocked:** connection reset on this path

### FR-A2b, Deliberation 2014-17 (Arcom French text)
- **url:** https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/deliberation-ndeg-2014-17-du-5-mars-2014-modifiant-la-recommandation-ndeg-2005-5-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des
- **save as:** `FR-A2b_delib_2014-17_arcom_fr.txt`
- **must contain:** `categorie iii`
- **why blocked:** connection reset on this path

### FR-R2, Recommandation 2004-7 du 15 decembre 2004 - category V programmes
- **url:** https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france
- **save as:** `FR-R2_reco_2004-7_category_V.txt`
- **must contain:** `minuit`
- **why blocked:** connection reset on this path

### FR-S1, Arcom youth signage public awareness page
- **url:** https://www.arcom.fr/en/news/images-always-have-impact-arcom-launches-its-new-youth-signage-awareness-raising-campaign
- **save as:** `FR-S1_arcom_youth_signage_summary.txt`
- **must contain:** `diffusion times`
- **why blocked:** connection reset on this path

### FR-L1, Loi 86-1067 du 30 septembre 1986 (arts. 1 and 15)
- **url:** https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205
- **save as:** `FR-L1_loi_86-1067.txt`
- **must contain:** `protection de l'enfance`
- **why blocked:** Cloudflare JS challenge

### FR-S2, solidarites.gouv.fr - Classification et signaletique de la television
- **url:** https://solidarites.gouv.fr/classification-et-signaletique-de-la-television
- **save as:** `FR-S2_solidarites_classification.txt`
- **must contain:** `categorie iii`
- **why blocked:** truncated response (IncompleteRead)

### EU-D1, AVMSD Directive 2010/13/EU article 6a (consolidated)
- **url:** https://www.legislation.gov.uk/eudr/2010/13/article/6a/data.pdf
- **save as:** `EU-D1_avmsd_article_6a.pdf`
- **must contain:** `will not normally hear or see`
- **why blocked:** AWS WAF challenge (x-amzn-waf-action: challenge)

## RECOMMENDED (6)

### UK-G2, Guidance Notes Section One
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0017/24704/section1.pdf
- **save as:** `UK-G2_ofcom_guidance_section_1.pdf`
- **must contain:** `watershed`
- **why blocked:** Cloudflare JS challenge

### UK-G3, Guidance Notes Section Two
- **url:** https://www.ofcom.org.uk/__data/assets/pdf_file/0023/104657/Section-2-Guidance-Notes.pdf
- **save as:** `UK-G3_ofcom_guidance_section_2.pdf`
- **must contain:** `generally accepted standards`
- **why blocked:** Cloudflare JS challenge

### UK-P1, Enforcement decision - Toofan NTV 29 May 2026 (Rule 1.3 breach)
- **url:** https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf
- **save as:** `UK-P1_ofcom_decision_toofan.pdf`
- **must contain:** `rule 1.3`
- **why blocked:** Cloudflare JS challenge

### UK-L2, Audiovisual Media Services Regulations 2020 (SI 2020/1062) explanatory note
- **url:** https://www.legislation.gov.uk/uksi/2020/1062/note/made
- **save as:** `UK-L2_avms_regulations_2020_note.txt`
- **must contain:** `audiovisual media services`
- **why blocked:** AWS WAF challenge (x-amzn-waf-action: challenge)

### EU-D1b, Directive (EU) 2018/1808 (amending directive)
- **url:** https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32018L1808
- **save as:** `EU-D1b_directive_2018_1808.pdf`
- **must contain:** `audiovisual media services`
- **why blocked:** AWS WAF challenge

### FR-S1c, La signaletique jeunesse (CSA/Arcom FRENCH public page)
- **url:** https://as-pc-www.csa.fr/Proteger/Protection-de-la-jeunesse-et-des-mineurs/La-signaletique-jeunesse
- **save as:** `FR-S1c_signaletique_jeunesse_fr.txt`
- **must contain:** `horaires de diffusion`
- **why blocked:** host unreachable (502 via proxy)

## OPTIONAL (2)

### FR-R3, Recommandation du 26 juillet 2005 - category V overseas France
- **url:** https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/notice-july-26-2005-television-service-editors-and-distributors-showing-category-v-programs-overseas-france
- **save as:** `FR-R3_reco_2005_category_V_overseas.txt`
- **must contain:** `categorie v`
- **why blocked:** connection reset on this path

### FR-X1, Deliberation 2011-64 du 20 decembre 2011 - on-demand (SMAD) services
- **url:** https://www.lexing.law/wp-content/uploads/22492432.pdf
- **save as:** `FR-X1_delib_2011-64_smad.pdf`
- **must contain:** `categorie iv`
- **why blocked:** see notes
