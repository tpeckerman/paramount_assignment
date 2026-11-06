# Source notes

Moved out of `MANIFEST.csv` to keep the table readable. These are findings that cost
real effort to establish — several were discovered only by a document failing in a
specific way. Read this before trusting any single source.

## `UK-S1` — Broadcasting Code Section One - Protecting the Under-Eighteens

AUTHORITATIVE FORM. The only maintained version - Ofcom no longer publishes the Code in print, so there is no current consolidated PDF. UK-S0 is the Jan 2019 print edition and does NOT contain this text. CURRENT authoritative text. Published 2021-03-03, last updated 2023-03-16. Replaces the former /__data/assets/pdf_file/... PDF entry, which is the January 2019 print edition on the legacy site's asset path - see UK-S0.

## `UK-S2` — Broadcasting Code Section Two - Harm and Offence

AUTHORITATIVE FORM. The only maintained version - Ofcom no longer publishes the Code in print, so there is no current consolidated PDF. UK-S0 is the Jan 2019 print edition and does NOT contain this text. CURRENT authoritative text. Published 2021-03-03, last updated 2024-02-19. Supplies the binding 8-factor definition of 'context'. Replaces the former January 2019 PDF entry - see UK-S0.

## `UK-S3` — Ofcom Broadcasting Code Section Three - Crime, Disorder, Hatred and Abuse

IN SCOPE via the context route, not the watershed. Rules 3.2/3.3 are permitted 'except where it is justified by the context', and context is Section Two's defined term whose third factor is the time of broadcast. Added 2026-11-06 after the 'significant numbers of children' test was shown to be too narrow (see C-11).

## `UK-S4` — Ofcom Broadcasting Code, Section Four: Religion

AUTHORITATIVE FORM. The only maintained version - Ofcom no longer publishes the Code in print, so there is no current consolidated PDF. UK-S0 is the Jan 2019 print edition and does NOT contain this text. In scope for ONE rule only: Rule 4.7, which bars claims that a living person has special powers when significant numbers of children may be expected to be watching. That is a child-audience broadcast restriction outside Section One. The rest of Section Four (religious content standards) is out of scope.

## `UK-G1` — Guidance - Observing the watershed on television and music videos

URL REPAIRED 2026-11-06 from the retired __data/assets pattern. Watershed + music video guidance.

## `UK-G2` — Guidance Notes Section One

URL CORRECTED 2026-11-06: was the retired __data/assets/pdf_file/ pattern, same defect class as the broadcast-codes/broadcast-standards error. Current path confirmed. Carries the access-control implementation detail (default PIN) and the trailers statement.

## `UK-G3` — Guidance Notes Section Two

URL REPAIRED 2026-11-06 from the retired __data/assets pattern. Issue Twelve, 18 July 2017. HIGH PRIORITY: Section Two guidance expands the eight context factors, including time of broadcast, on which the whole UK analysis turns. Currently 0 rules mined from it.

## `UK-M1` — Statement - Review of the mandatory daytime protection rules

LANDING PAGE ONLY, not the statement text. Confirmed by reading it: roughly five lines of substance out of eighty, the rest menu and footer. It carries the key fact - the MDP extension came into force 1 January 2019 - but NOT the reasoning. The statement PDF (679 KB) is merely listed on the page. Fetch that PDF if the reasoning behind extending MDP to scheduled channels is ever needed; it is also what would settle C-14.

## `UK-P1` — Enforcement decision - Toofan NTV 29 May 2026 (Rule 1.3 breach)

Example of an applied threshold. Precedent is the only calibration source for judgment_based rows.

## `UK-L1` — Communications Act 2003 section 319

Stable URL that always shows the current consolidated text. The /data.pdf variant is a per-format path and is also WAF-gated. Legal basis: s.319(2)(a) duty that persons under eighteen are protected. URL switched to the publisher's direct PDF endpoint.

## `UK-L2` — Audiovisual Media Services Regulations 2020 (SI 2020/1062) explanatory note

BACKGROUND ONLY, and correctly cited by NO rule. This is the explanatory note to the UK instrument implementing the revised AVMSD - it summarises what the regulations do rather than stating operative rules, and the substance it describes (proportionate measures to protect minors) is taken directly from EU-D1, which is the primary source. Kept as provenance for why the UK framework has its present shape. Prior expect string was 'audiovisual media services', which matched 5 of 22 documents and could not identify this one.

## `FR-R1c` — Recommandation 2005-5 consolidated (Arcom French text)

FRENCH consolidated text on the regulator site. Prefer this over the EN machine translation. JS-HEAVY PAGE: extraction may yield little or no rule text. fetch_originals.py flags a suspiciously short result; if it does, save the page's Telecharger/Imprimer PDF by hand into this folder under target_filename with a .pdf extension and update format to pdf.

## `FR-R2` — Recommandation 2004-7 du 15 decembre 2004 - category V programmes

SOLE SOURCE for the French -18 window. Closes C-03. Page body is drawn by JavaScript, so no fetch could ever read it; saved from a browser where it had already rendered. CAUTION: this is Arcom's own machine translation and the page itself warns that only the original French version is authentic - every quote drawn from it is EN and needs re-checking against the French by a French-qualified reviewer.

## `FR-S1c` — La signaletique jeunesse (CSA/Arcom FRENCH public page)

URL WAS BROKEN AND NEVER RESOLVED: pointed at as-pc-www.csa.fr, an internal STAGING hostname leaked into a public link, on the pre-2022 csa.fr domain (CSA became Arcom in 2022). Returned NXDOMAIN - never fetchable, no retry would have helped. Replaced with the current Arcom educational-resources page. SECONDARY source: corroboration only, never cite alone for a rule.

## `FR-S2` — solidarites.gouv.fr - Classification et signaletique de la television

Used to disambiguate C-02. States the cat. III / IV hours plainly in French.

## `FR-L1` — Loi 86-1067 du 30 septembre 1986 (arts. 1 and 15)

Art. 15 - statutory duty and the two-tier harm standard (nuire gravement vs nuire). JS-HEAVY PAGE: extraction may yield little or no rule text. fetch_originals.py flags a suspiciously short result; if it does, save the page's Telecharger/Imprimer PDF by hand into this folder under target_filename with a .pdf extension and update format to pdf.

## `FR-V1` — Mise en demeure C8 (example citing a channel convention)

NO STABLE LANDING PAGE RECORDED - Arcom's decisions index was not located, so if this /sites/default/files/ PDF URL rots the document must be found by searching Arcom's legal area. Shows a convention being cited alongside reco. 2005-5. Conventions themselves are not collected - C-06.

## `FR-C1` — CNC - Proteger sans censurer (classification des oeuvres cinematographiques)

Confirms the commission has no competence for television. Input only, not a rule source.

## `EU-D1` — AVMSD Directive 2010/13/EU article 6a (consolidated)

Stable URL for the consolidated article as retained in UK law. Framework baseline. Mandates the outcome and permits time OR technical measures. URL switched to the publisher's direct PDF endpoint. | CAVEAT: this is legislation.gov.uk, i.e. the UK RETAINED version of the directive, which may diverge from the EU text post-Brexit. Acceptable for the UK analysis; for an EU-wide claim cite EUR-Lex instead.

## `EU-D1b` — Directive (EU) 2018/1808 (amending directive)

URL WAS REJECTED BY EUR-LEX (Page Not Found). The old value did carry its query string (?uri=CELEX:32018L1808) - an earlier note here claiming it was truncated was wrong, misread from a browser address bar that displays the query trimmed. The likely cause is the unencoded colon; %3A is the safe form. Replaced with the ELI permalink, which takes no query at all and is designed as a permanent identifier. CELEX 32018L1808, OJ L 303, 28.11.2018, pp. 69-92. AMENDING directive: provenance only, not current rule text. MIRROR if EUR-Lex blocks you: legislation.gov.uk/eudr/2018/1808 (UK retained version - read, do not cite).
