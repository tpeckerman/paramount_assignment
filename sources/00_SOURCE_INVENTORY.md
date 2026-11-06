# Source Inventory — Age Ratings & Broadcast Restrictions for Linear TV (UK, France, EU)

Compiled: 2026-11-06
Scope: **linear (broadcast) television only.** On-demand / streaming services are a different
regime in both countries and are out of scope for Task 1.

## How to read `authority_rank`

Used to resolve contradictions. Lower number wins.

| Rank | Source type | Meaning |
|---|---|---|
| 1 | `statute` | Primary legislation / directive. Sets the duty, rarely the operational detail. |
| 2 | `regulator_binding` | The regulator's own binding code / recommendation / deliberation. **This is the operative layer for actual decisions.** |
| 3 | `regulator_guidance` | Regulator guidance explaining how it applies its own binding rules. Not itself binding but is how the regulator reasons. |
| 4 | `precedent` | Published enforcement decisions. Shows applied thresholds. |
| 5 | `regulator_summary` | The regulator's own plain-language web summary. Useful, but has been observed to be imprecise (see conflict C-01). |
| 6 | `classification_body` | Film classification bodies (BBFC, CNC). Not TV regulators; relevant only as an **input** when the content is a theatrical film. |
| 7 | `secondary` | Government department pages, parliamentary answers, academic/legal commentary. Used only to corroborate or disambiguate. |

---

## UNITED KINGDOM

Regulator: **Ofcom** (Office of Communications). There is **no per-programme age rating for linear TV in the UK.**
Decisions are made against Code rules plus the watershed, judged in context.

| # | Document | Type | Rank | Scope | URL |
|---|---|---|---|---|---|
| UK-S1 | Ofcom Broadcasting Code, **Section One: Protecting the Under-Eighteens** | regulator_binding | 2 | All Ofcom-licensed TV & radio. Rules 1.3–1.6 do **not** apply to BBC ODPS. | https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-one-protecting-under-eighteens |
| UK-S2 | Ofcom Broadcasting Code, **Section Two: Harm and Offence** | regulator_binding | 2 | Same. Supplies the binding **definition of "context"**, which Section One depends on. Must be read with S1. | https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-two-harm-offence |
| UK-G1 | Ofcom Guidance: *Protecting the Under-Eighteens — Observing the watershed on television and music videos* | regulator_guidance | 3 | TV. Covers pre/post-watershed transition and **music videos** specifically. | https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf |
| UK-G2 | Ofcom Guidance Notes, Section One | regulator_guidance | 3 | Interpretation aid for S1. | https://www.ofcom.org.uk/__data/assets/pdf_file/0017/24704/section1.pdf |
| UK-G3 | Ofcom Guidance Notes, Section Two | regulator_guidance | 3 | Interpretation aid for S2. | https://www.ofcom.org.uk/__data/assets/pdf_file/0023/104657/Section-2-Guidance-Notes.pdf |
| UK-M1 | Ofcom Statement: *Review of the mandatory daytime protection rules* (5 Nov 2018) | regulator_binding | 2 | Created/extended the **PIN-based "mandatory daytime protection" (MDP)** regime. Effective 1 Jan 2019. | https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf |
| UK-P1 | Ofcom Broadcast and On Demand Bulletins (enforcement decisions) | precedent | 4 | Applied thresholds. Example: *Toofan*, NTV, 29 May 2026 11:30 — violent film not appropriately scheduled, breach of Rule 1.3. | https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf |
| UK-L1 | Communications Act 2003, s.319 (standards objectives) and s.3(4)(h) | statute | 1 | Legal basis for Ofcom's duty that "persons under the age of eighteen are protected" (s.319(2)(a)). | https://www.legislation.gov.uk/ukpga/2003/21/section/319 |
| UK-L2 | The Audiovisual Media Services Regulations 2020 (SI 2020/1062) | statute | 1 | Implemented revised AVMSD duties into UK law; content standards for broadcast TV remain in the Ofcom Code. | https://www.legislation.gov.uk/uksi/2020/1062/note/made |
| UK-C1 | BBFC classification | classification_body | 6 | **Not a TV regulator.** Relevant because the Ofcom Code refers to BBFC ratings (Rules 1.17, 1.22, 1.23, 1.24, 1.25, 1.26) for films and film-equivalent material. | https://www.bbfc.co.uk |

### Also considered and ruled out of scope
- **ASA / BCAP Advertising Codes** — advertising content, not programme content. Out of scope for this task.
- **BBC First Party / BBC Editorial Guidelines** — internal editorial standards; the BBC's linear TV is regulated under the Ofcom Code.

---

## FRANCE

Regulator: **Arcom** (Autorité de régulation de la communication audiovisuelle et numérique; replaced the CSA in 2022).
France **does** have a graded per-programme classification: the *signalétique jeunesse*,
five categories I–V (tous publics, -10, -12, -16, -18).

| # | Document | Type | Rank | Scope | URL |
|---|---|---|---|---|---|
| FR-R1 | **Recommandation n° 2005-5 du 7 juin 2005** aux éditeurs de services de télévision concernant la signalétique jeunesse et la classification des programmes — *as amended* | regulator_binding | 2 | Linear TV editors. **The core framework.** Defines categories I–V (art. 2) and programming conditions (art. 3). | https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000446802 |
| FR-R1-EN | Same, Arcom consolidated page (machine translation, DeepL) | regulator_binding | 2 | Consolidated view listing both amendments. **Translation is unreliable — see conflict C-02.** | https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/notice-june-7-2005-television-service-editors-concerning-youth-signs-and-classification-programmes-younger-viewers |
| FR-A1 | **Délibération n° 2012-57 du 23 octobre 2012** modifying FR-R1 | regulator_binding | 2 | Amended art. 4(2)(a) — category II on-screen signage duration. | https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/deliberation-du-23-octobre-2012-modifiant-la-recommandation-ndeg-2005-5-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des-programmes |
| FR-A2 | **Délibération n° 2014-17 du 5 mars 2014** modifying FR-R1 (JORF 9 Apr 2014) | regulator_binding | 2 | **Replaced arts. 1, 3 and 4; amended art. 2; inserted a new art. 5** (trailers & music videos). This is the current operative text for scheduling. | https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/deliberation-no-2014-17-march-5-2014-amending-notice-no-2005-5-june-7-2005-television-service-editors-concerning-youth-signage-and-classification-programmes |
| FR-R2 | **Recommandation n° 2004-7 du 15 décembre 2004** aux éditeurs et distributeurs de services de télévision diffusant des programmes de catégorie V | regulator_binding | 2 | **Category V (-18) only.** Art. 3 of FR-R1 defers to this entirely. Eligible services, hours, locking, marketing. | https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france |
| FR-R3 | Recommandation du 26 juillet 2005 — category V, overseas France | regulator_binding | 2 | Overseas départements. Out of core scope but noted. | https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/notice-july-26-2005-television-service-editors-and-distributors-showing-category-v-programs-overseas-france |
| FR-S1 | Arcom youth-signage public summary page | regulator_summary | 5 | Plain-language per-category meanings and broadcast times. **Imprecise — see conflict C-01.** | https://www.arcom.fr/en/news/images-always-have-impact-arcom-launches-its-new-youth-signage-awareness-raising-campaign |
| FR-L1 | **Loi n° 86-1067 du 30 septembre 1986**, art. 1 and **art. 15** | statute | 1 | Art. 15 is the statutory duty: Arcom must ensure protection of childhood and adolescence and respect for human dignity in programmes; and that programmes likely to harm minors' physical, mental or moral development are not made available unless the choice of broadcast time and appropriate technical means ensure minors will not normally see or hear them. | https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205 |
| FR-V1 | Channel **conventions** (per-channel agreements with Arcom) | regulator_binding | 2 | **Channel-specific.** Each channel's convention contains its own protection-of-minors articles, which can be stricter than the general recommendation. Cited alongside FR-R1 in Arcom enforcement (e.g. C8 decision, arts. 2-3-7, 2-4, 4-2-1). | https://www.arcom.fr/sites/default/files/2023-05/MeD_C8.pdf |
| FR-C1 | **CNC** / Commission de classification des œuvres cinématographiques — *visa d'exploitation* | classification_body | 6 | **Cinema releases only.** The CNC states its commission has no competence for television, DVD, VOD, video games or internet. Relevant only as an **input** for theatrical films: a cinema -12/-16/-18 interdiction feeds the TV classification, and TV classification is often strengthened relative to the cinema rating. | https://www.cnc.fr/cinema/actualites/proteger-sans-censurer--la-classification-des-oeuvres-cinematographiques_1924881 |
| FR-S2 | solidarites.gouv.fr — *Classification et signalétique de la télévision* | secondary | 7 | French government summary. **Used to disambiguate the garbled Arcom English translation of art. 3 (see C-02).** | https://solidarites.gouv.fr/classification-et-signaletique-de-la-television |

### Also considered
- **Délibération n° 2011-64 du 20 décembre 2011** — protection of minors for **on-demand** (SMAD) services. Uses the same five categories but **different** conditions (e.g. category IV accessible only 22:30–05:00 when not behind payment). **Out of scope (non-linear) but a useful contrast: it proves rating ≠ fixed hours across service types.** https://www.lexing.law/wp-content/uploads/22492432.pdf
- **Délibération du 10 février 2004** — protection of minors on **radio** services. Out of scope.

---

## EUROPEAN UNION (baseline, not directly applicable)

| # | Document | Type | Rank | Scope | URL |
|---|---|---|---|---|---|
| EU-D1 | **AVMSD** — Directive 2010/13/EU as amended by Directive (EU) 2018/1808, **Article 6a** | statute | 1 | Sets the obligation on Member States; leaves the mechanism to national law. Art. 6a(1): measures so that minors "will not normally hear or see" harmful content, via e.g. broadcast times or age verification, proportionate to potential harm; "The most harmful content, such as gratuitous violence and pornography, shall be subject to the strictest measures." Art. 6a(3): Member States must ensure providers give viewers sufficient information using a **content-descriptor system**. | https://www.legislation.gov.uk/eudr/2010/13/article/6a |
| EU-O1 | European Audiovisual Observatory — protection of minors / AVMSD spotlight | secondary | 7 | Comparative mapping across Member States. Useful for Task 2 scaling. | https://www.obs.coe.int/en/web/observatoire/protection-of-minors |

**Why the EU layer matters for the design:** Article 6a is the reason both frameworks exist in the shape they do,
and it explains the structural asymmetry — it mandates the *outcome* (minors won't normally see it) and
permits *either* scheduling *or* technical measures. France chose a graded descriptor system with fixed hours;
the UK chose a single watershed plus contextual judgement plus a PIN regime. **Neither is derivable from an age
rating alone.** The UK is no longer bound by the directive but retained equivalent duties via SI 2020/1062.

---

## Conflicts and ambiguities found during collection

### C-01 — Arcom summary page vs Arcom binding text (category III / -12 hours)
- **FR-S1** (Arcom public summary, rank 5) presents **-12** as broadcastable "during the day, under certain conditions",
  with the same wording it uses for -10.
- **FR-R1/FR-A2** (binding text, rank 2) and **FR-S2** (French government, rank 7) both state **-12 must not be
  broadcast before 22:00** on non-cinema channels, with a capped exception from 20:30.
- **Resolution:** binding text wins. The summary page is treated as unreliable for -12.
- **Residual risk:** the summary page may have been extracted imperfectly from a visually repetitive layout.
  Flagged for human confirmation against the live page.

### C-02 — Garbled machine translation of art. 3, category III
- The Arcom English page (FR-R1-EN) duplicates the cinema-channel sentence and then states "may not be shown before
  10 pm", leaving it unclear which rule attaches to which service type.
- **Resolution:** FR-S2 (French government) states it unambiguously: non-cinema channels → not before 22:00;
  cinema channels → not on Wednesdays before 20:30. This matches multiple French parliamentary answers.
- **Action required:** confirm against the **French original** on Légifrance before this row is marked `approved`.

### C-03 — Age of FR-R2 (category V regime)
- FR-R2 dates from 2004 and contains compliance deadlines of 1 Jan 2005 / 2006 / 2008, all long elapsed.
- Not yet confirmed whether it has been amended or superseded. Flagged `unverified`.

### C-04 — Full verbatim text could not be retrieved
- The workspace has no outbound network access to ofcom.org.uk / arcom.fr / legifrance.gouv.fr
  (egress proxy refuses the connection), and the web-fetch path returns **summaries, not verbatim text**,
  declining full reproduction.
- **Consequence:** the per-source files in this folder are **structured extracts with canonical URLs**,
  not official full text. Every rule row carries a `source_url` so the authoritative wording can be checked.
- **For Task 2 this is itself a finding:** an automated rule-ingestion pipeline cannot rely on
  model-mediated fetching for legal text. It needs direct document retrieval (allowlisted fetch or manual
  deposit of PDFs) so that a verbatim-quote integrity check is possible.
