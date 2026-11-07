#!/usr/bin/env python3
"""Build the long-format regulatory rule table as a multi-tab workbook."""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

TODAY = "2026-11-06"

COLS = [
    ("rule_id", 14), ("country", 9), ("regulator", 11), ("source_type", 20),
    ("authority_rank", 9), ("use_for_decision", 20), ("service_type", 26),
    ("content_category", 20), ("classification", 18), ("threshold_description", 60),
    ("time_restriction_text", 44), ("time_rule_machine", 40),
    ("exceptions_conditions", 52), ("determinacy", 16), ("ambiguity_flag", 22),
    ("ambiguity_note", 52), ("human_review_required", 10),
    ("source_doc", 20), ("clause_ref", 16), ("source_url", 42),
    ("valid_from", 12), ("valid_to", 10), ("status", 12),
    ("verbatim_quote", 48), ("quote_lang", 7),
    ("extraction_confidence", 10), ("last_checked", 12),
]

# order matches COLS
R = []


def add(rid, country, reg, stype, rank, use, svc, cat, cls, thr, trt, trm, exc,
        det, afl, ano, hrr, doc, clause, url, vfrom, vto, status, quote, qlang,
        conf, checked=TODAY):
    R.append([rid, country, reg, stype, rank, use, svc, cat, cls, thr, trt, trm,
              exc, det, afl, ano, hrr, doc, clause, url, vfrom, vto, status,
              quote, qlang, conf, checked])


# ----------------------------------------------------------------- URLs
U_S1 = "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-one-protecting-under-eighteens"
U_S2 = "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence"
U_FRS1C = ("https://www.arcom.fr/en/find-out-more/educational-resources/protection-young-people-and-persons-under-18")
U_EUB = "https://eur-lex.europa.eu/eli/dir/2018/1808/oj"
U_S3 = "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-three-crime-disorder-hatred-abuse"
U_S4 = ("https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-four-religion")
U_G1 = "https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf"
U_P1 = ("https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf")
U_G3 = ("https://www.ofcom.org.uk/siteassets/resources/documents/tv-radio-and-on-demand/broadcast-guidance/programme-guidance/broadcast-code-guidance/section-2-guidance-notes.pdf?v=322622")
U_G2 = ("https://www.ofcom.org.uk/siteassets/resources/documents/tv-radio-and-on-demand/broadcast-guidance/programme-guidance/broadcast-code-guidance/section1.pdf?v=328674")
U_M1 = "https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf"
U_L1 = "https://www.legislation.gov.uk/ukpga/2003/21/section/319"  # stable HTML
U_FR1 = "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000446802"  # 2005 ORIGINAL
U_FR1C = ("https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/recommandation-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des-programmes")  # CURRENT consolidated French text - cite this for current law
U_FR2 = "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/deliberation-no-2014-17-march-5-2014-amending-notice-no-2005-5-june-7-2005-television-service-editors-concerning-youth-signage-and-classification-programmes"
U_FRV = "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france"
U_FRL = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205"
U_CONV = "https://www.arcom.fr/sites/default/files/2023-05/MeD_C8.pdf"
U_EU = "https://www.legislation.gov.uk/eudr/2010/13/article/6a"  # stable HTML

C02 = ("C-02 RESOLVED 2026-11-06. The service mapping was originally taken from Arcom's "
       "garbled English machine translation. Now confirmed against the FRENCH text from two "
       "independent sources: Legifrance JORFTEXT000000446802 (the 2005 original) and the "
       "csa.fr consolidated page carrying the 'Modifiee par la deliberation n. 2014-17 du "
       "5 mars 2014' banner. Both read identically: 'pour les chaines cinema et les services "
       "de paiement a la seance, ces programmes ne doivent pas etre diffuses le mercredi avant "
       "20 h 30. Pour les autres services de television, ces programmes ne doivent pas etre "
       "diffuses avant 22 heures.' The Arcom French page for 2014-17 confirms art. 3 was "
       "replaced with the same wording.")
C03 = ("Source text dates from 2004 with compliance deadlines of 2005/2006/2008 all elapsed; "
       "CSA->Arcom (2022) and the 2021 AVMSD transposition decree both postdate it. "
       "Not confirmed still in force unamended. (C-03)")

# ================================================================ UK
add("UK-DEF-001", "UK", "Ofcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "definition", "n/a",
    "'Children' means people under fifteen. NOTE: the Section One principle protects under-EIGHTEENS, but every operative rule using the word 'children' means under 15.",
    "n/a", "n/a",
    "Affects application of Rules 1.3, 1.10, 1.13, 1.27. Conflating the two ages mis-applies those rules.",
    "bright_line", "clear",
    "Recorded explicitly because it is a known conflation trap (C-05).", "no",
    "UK-S1", "S1 definitions", U_S1, "2021-03-03", "open", "approved",
    "Children are people under the age of fifteen years", "EN", "high")

add("UK-DEF-002", "UK", "Ofcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "definition", "n/a",
    "'Appropriate scheduling' is judged on: nature of content; likely number and age range of child viewers (taking into account school time, weekends and holidays); programme start and finish time; nature of the channel/programme; likely audience expectations for that channel at that time and day.",
    "n/a", "n/a",
    "Broadcasters serving ECTT Parties must also consider time differences in the country of reception.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "S1 definitions", U_S1, "2021-03-03", "open", "approved",
    "protected by appropriate scheduling from material that is unsuitable", "EN", "high")

add("UK-DEF-003", "UK", "Ofcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "definition", "n/a",
    "Binding definition of 'context' (8 factors): editorial content; the service; TIME OF BROADCAST; what is scheduled before and after; degree of harm/offence likely; likely size and composition of audience and audience expectation; extent to which content can be signalled in advance; effect on those coming across it unawares.",
    "n/a", "n/a",
    "This is the mechanism by which the SAME content is compliant at one hour and a breach at another with no rating change. Section One must be read with Section Two.",
    "judgment_based", "clear",
    "Central to the whole UK design: time of broadcast is a formal component of context.", "no",
    "UK-S2", "S2 'meaning of context'", U_S2, "2021-03-03", "open", "approved",
    "Context includes (but is not limited to):", "EN", "high")

add("UK-GEN-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "serious_harm", "prohibited",
    "Material that might SERIOUSLY impair the physical, mental or moral development of people under eighteen.",
    "No permitted time. Absolute prohibition.", "prohibited",
    "None. No contextual justification, no technical measure and no scheduling cures this.",
    "bright_line", "clear",
    "Hard pre-check: should be enforced in code, not left to prompt reasoning.", "no",
    "UK-S1", "Rule 1.1", U_S1, "2021-03-03", "open", "approved",
    "might seriously impair the physical, mental or moral development", "EN", "high")

add("UK-GEN-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "Broadcasters must take all reasonable steps to protect people under eighteen.",
    "n/a - general duty", "n/a",
    "Open-ended duty; informs every other decision.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.2", U_S1, "2021-03-03", "open", "approved",
    "must take all reasonable steps to protect people under eighteen", "EN", "high")

add("UK-SCH-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "Children must be protected by appropriate scheduling from material unsuitable for them.",
    "Determined by the appropriate-scheduling factors, not a fixed clock time.",
    "judgment:appropriate_scheduling",
    "Does NOT apply to BBC ODPS. This is the rule most often cited in enforcement (see UK-P1 precedent).",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.3", U_S1, "2021-03-03", "open", "approved",
    "Children must...be protected by appropriate scheduling from material that is unsuitable for them...",
    "EN", "high")

add("UK-SCH-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "free_to_air; all_linear_tv", "scheduling_general", "watershed_bound",
    "Television broadcasters must observe the watershed. Material unsuitable for children should not, in general, be shown before 21:00 or after 05:30.",
    "Watershed 21:00-05:30.", "window=21:00-05:30",
    "Does NOT apply to BBC ODPS. Displaced by 20:00 for unprotected premium subscription film services (UK-SCH-003) and disapplied where mandatory daytime protection is in place (UK-FLM-003).",
    "bright_line", "clear",
    "The single most important UK bright line. Note it is an OPEN-ENDED period, structurally unlike the French closed windows.",
    "no", "UK-S1", "Rule 1.4", U_S1, "2021-03-03", "open", "approved",
    "should not, in general, be shown before 2100 or after 0530", "EN", "high")

add("UK-SCH-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film", "scheduling_general", "watershed_bound",
    "Premium subscription film services WITHOUT protection operate a 20:00 watershed rather than 21:00.",
    "Watershed 20:00.", "window=20:00-05:30",
    "Conditional on service type AND absence of protection. Requires service_type input.",
    "conditional", "clear",
    "Proves the watershed itself is service-dependent, not universal.", "no",
    "UK-S1", "Rule 1.4", U_S1, "2021-03-03", "open", "approved",
    "The watershed is at 2100", "EN", "medium")

add("UK-SCH-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "The transition to more adult material must not be unduly abrupt at the watershed. The strongest material should appear later in the schedule.",
    "No fixed interval specified.", "judgment:post_watershed_ramp",
    "A programme starting after 21:00 should not open with its strongest material; a programme crossing 21:00 must not suddenly become unsuitable.",
    "judgment_based", "clear",
    "No numeric threshold exists. Escalate to human review when a test case places strong material in the first minutes after 21:00.",
    "yes", "UK-S1 + UK-G1", "Rule 1.6; UK-G1 s.1", U_G1, "2021-03-03", "open", "approved",
    "It should not commence with the strongest material", "EN", "high")

add("UK-SCH-005", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "fear_distress", "context_dependent",
    "Clear information about content that may distress some children should be given, if appropriate, taking into account the context.",
    "n/a - information duty", "n/a",
    "'If appropriate' - discretionary, context-driven.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.7", U_S1, "2021-03-03", "open", "approved",
    "For television programmes broadcast before the watershed", "EN", "high")

add("UK-DRG-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "drugs_alcohol_smoking", "context_dependent",
    "Drugs, smoking, solvents and alcohol must not be featured in programmes made primarily for children without strong editorial justification; and must not be condoned, encouraged or glamorised in other programmes before the watershed without editorial justification.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=editorial_justification",
    "Two different thresholds: 'strong editorial justification' for children's programmes vs 'editorial justification' elsewhere pre-watershed.",
    "conditional", "clear",
    "The two-tier justification standard is easy to flatten; keep both.", "no",
    "UK-S1", "Rule 1.10", U_S1, "2021-03-03", "open", "approved",
    "must not be featured in programmes made primarily for children", "EN", "high")

add("UK-VIO-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "context_dependent",
    "Violence, its after-effects and descriptions of violence (verbal or physical) must be appropriately limited in programmes broadcast before the watershed, and must be justified by the context.",
    "Restriction bites before 21:00; post-watershed governed by context.",
    "not_before=21:00;unless=appropriately_limited_and_context_justified",
    "'Appropriately limited' AND 'justified by the context' - a double test. Context per UK-DEF-003.",
    "judgment_based", "clear",
    "Primary violence rule. No intensity scale is given in the Code; applied thresholds come only from enforcement precedent.",
    "yes", "UK-S1", "Rule 1.11", U_S1, "2021-03-03", "open", "approved",
    "must be appropriately limited in programmes broadcast before the watershed", "EN", "high")

add("UK-VIO-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "context_dependent",
    "Programmes made primarily for children must not include material that condones or glamorises violent, dangerous or seriously antisocial behaviour likely to encourage imitation.",
    "Applies at all times to children's programmes.", "prohibited_in=children_programmes",
    "Turns on programme type, not clock time.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.12", U_S1, "2021-03-03", "open", "approved",
    "easily imitable by children in a manner that is harmful or dangerous", "EN", "high")

add("UK-IMI-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "imitable_behaviour", "context_dependent",
    "Dangerous behaviour, or behaviour easily imitable by children in a manner that is harmful, must not be featured before the watershed unless there is editorial justification.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=editorial_justification",
    "Cross-refers to Rules 2.4 and 2.5.",
    "conditional", "clear", "", "no",
    "UK-S1", "Rule 1.13", U_S1, "2021-03-03", "open", "approved",
    "Dangerous behaviour, or the portrayal of dangerous behaviour", "EN", "high")

add("UK-LNG-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "strong_language", "watershed_bound",
    "THE MOST OFFENSIVE LANGUAGE must not be broadcast before the watershed.",
    "Prohibited before 21:00. No contextual justification available pre-watershed.",
    "not_before=21:00",
    "Absolute pre-watershed. Post-watershed use still subject to Rule 2.3 context.",
    "bright_line", "clear",
    "Note: 'the most offensive language' is a defined Ofcom concept informed by its periodic audience-attitudes research; the Code itself does not enumerate the words.",
    "yes", "UK-S1", "Rule 1.14", U_S1, "2021-03-03", "open", "approved",
    "The most offensive language must not be broadcast before the watershed",
    "EN", "high")

add("UK-LNG-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "strong_language", "prohibited",
    "Offensive language must not be broadcast in programmes made for younger children.",
    "Applies at all times to programmes for younger children.",
    "prohibited_in=programmes_for_younger_children",
    "Turns on programme type, not clock time.",
    "bright_line", "clear", "", "no",
    "UK-S1", "Rule 1.15", U_S1, "2021-03-03", "open", "approved",
    "Offensive language must not be used in programmes made for younger children", "EN", "high")

add("UK-LNG-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "strong_language", "context_dependent",
    "Offensive language must not be broadcast before the watershed unless justified by the context. In any event, FREQUENT USE of such language must be avoided before the watershed.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=context_justified;frequency_cap=avoid_frequent",
    "The frequency limb is independent of the context limb ('in any event').",
    "judgment_based", "clear",
    "Requires CUMULATIVE counting, not presence/absence. Extraction stage must record counts with timecodes.",
    "yes", "UK-S1", "Rule 1.16", U_S1, "2021-03-03", "open", "approved",
    "frequent use of such language must be avoided before the watershed",
    "EN", "high")

add("UK-SEX-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "prohibited",
    "Material equivalent to the BBFC R18 rating must not be broadcast at any time.",
    "No permitted time.", "prohibited",
    "None. Survives every access/technical measure including MDP.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "UK-S1", "Rule 1.17", U_S1, "2021-03-03", "open", "approved",
    "Material equivalent to the...R18-rating must not be broadcast at any time.",
    "EN", "high")

add("UK-SEX-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film; pay_per_view", "sexual_content", "restricted_window",
    "'Adult sex material' (strong sexual images/language broadcast for the primary purpose of sexual arousal) may only be broadcast between 22:00 and 05:30, on premium subscription or pay-per-view/night services operating with MANDATORY RESTRICTED ACCESS.",
    "22:00-05:30 only, and only on eligible services with mandatory restricted access.",
    "window=22:00-05:30;requires=mandatory_restricted_access",
    "NOT unlocked by mandatory daytime protection - MDP expressly excludes adult sex material.",
    "conditional", "clear",
    "Three distinct UK access concepts must not be conflated: mandatory restricted access (this rule), mandatory daytime protection (films), and no protection. A model treating 'PIN protected' as one concept will wrongly allow this in daytime.",
    "no", "UK-S1 + UK-M1", "Rule 1.18", U_S1, "2021-03-03", "open", "approved",
    "broadcast for the primary purpose of sexual arousal or stimulation", "EN", "high")

add("UK-SEX-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "context_dependent",
    "Material broadcast after the watershed containing strong or explicit sexual images/language, but which is NOT 'adult sex material', must be justified by the context.",
    "Post-watershed only, subject to context.", "not_before=21:00;unless=context_justified",
    "Boundary with Rule 1.18 turns on 'primary purpose of sexual arousal'.",
    "judgment_based", "clear",
    "Escalate because the 1.18/1.19 boundary carries a large consequence: if material is "
    "'adult sex material' it is confined to 22:00-05:30 behind mandatory restricted access, "
    "whereas under 1.19 it is merely context-justified post-watershed. The test turns on "
    "'primary purpose', which is an editorial judgment, not a content feature.", "yes",
    "UK-S1", "Rule 1.19", U_S1, "2021-03-03", "open", "approved",
    "images and/or language of a strong or explicit sexual nature", "EN", "high")

add("UK-SEX-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "context_dependent",
    "Representations of sexual intercourse must not occur before the watershed unless there is a SERIOUS EDUCATIONAL PURPOSE. Any discussion or portrayal of sexual behaviour before the watershed must be editorially justified and appropriately limited.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=serious_educational_purpose",
    "'Serious educational purpose' is a higher bar than ordinary editorial justification.",
    "conditional", "clear", "", "no",
    "UK-S1", "Rule 1.20", U_S1, "2021-03-03", "open", "approved",
    "Representations of sexual intercourse must not occur before the watershed", "EN", "high")

add("UK-NUD-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "nudity", "context_dependent",
    "Nudity before the watershed must be justified by the context.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=context_justified",
    "Nudity is NOT automatically post-watershed; context can justify it earlier.",
    "judgment_based", "clear",
    "Common over-rating trap: treating any nudity as automatically post-watershed.", "yes",
    "UK-S1", "Rule 1.21", U_S1, "2021-03-03", "open", "approved",
    "Nudity before the watershed", "EN", "high")

add("UK-FLM-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "prohibited",
    "No film REFUSED classification by the BBFC may be broadcast, unless it has subsequently been classified or the BBFC has confirmed it would not be subject to compulsory cuts under current standards. Restrictions also apply to cut versions.",
    "No permitted time unless subsequently classified/confirmed.", "prohibited;unless=subsequently_classified",
    "Survives MDP - unchanged by the 2018 review.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "UK-S1", "Rule 1.22", U_S1, "2021-03-03", "open", "approved",
    "No film refused classification by the British Board of Film Classification", "EN", "high")

add("UK-FLM-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "watershed_bound",
    "BBFC 18-rated films (or their equivalent) must not be broadcast before 21:00 on ANY service, except where there is mandatory daytime protection in place.",
    "Not before 21:00, unless MDP.", "not_before=21:00;unless=mandatory_daytime_protection",
    "Amended with effect 1 Jan 2019: the previous pay-per-view-specific carve-out was replaced by the general MDP concept.",
    "conditional", "clear",
    "THE clearest proof that rating does not determine hours: the same BBFC 18 film is barred pre-21:00 on one service and permitted at any hour on another, purely because of a technical access measure.",
    "no", "UK-S1 + UK-M1", "Rule 1.23", U_M1, "2019-01-01", "open", "approved",
    "must not be broadcast before 2100, on any service", "EN", "high")

add("UK-FLM-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film; pay_per_view; scheduled_channels_with_mdp",
    "film_carryover", "any_time_with_protection",
    "Where MANDATORY DAYTIME PROTECTION is in place, programmes unsuitable for children that would usually be scheduled post-watershed, and films up to BBFC 18 or equivalent, may be broadcast AT ANY TIME OF DAY. Clear information must be provided about the content and about the protection in place.",
    "Any time of day.", "any_time;requires=mandatory_daytime_protection",
    "MDP = a PIN protection system in place pre-2100 and post-0530, non-removable by the user, required on each entry, with accurate metadata. NOT available to free-to-air DTT (e.g. Freeview) or to channels not on a vertically integrated pay-TV platform. Excludes adult sex material. Does not cure R18 or refused-classification films.",
    "conditional", "clear",
    "service_type AND access_control are mandatory inputs. If absent, the correct output is a missing-information flag, NOT an assumption of free-to-air.",
    "no", "UK-S1", "Rule 1.24", U_M1, "2019-01-01", "open", "approved",
    "PIN protection system in place pre-2100 and post-0530",
    "EN", "high")

add("UK-FLM-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film", "film_carryover", "watershed_bound",
    "Films up to BBFC 15 or equivalent may be broadcast from 20:00 on premium subscription film services WITHOUT mandatory daytime protection.",
    "Not before 20:00.", "not_before=20:00",
    "Carve-out retained in the 2018 review: Ofcom had proposed removing it and did not.",
    "conditional", "clear", "", "no",
    "UK-S1", "Rule 1.24", U_S1, "2019-01-01", "open", "approved",
    "pre-2000 and post 0530 for up to BBFC 15-rated films", "EN", "medium")

add("UK-FLM-005", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "pay_per_view", "film_carryover", "any_time_with_protection",
    "Pay-per-view services may broadcast films up to BBFC 18 or equivalent at any time, provided mandatory daytime protection is in place. They must additionally provide content information, operate a detailed itemised billing system, and make subscribers aware of their child-protection systems.",
    "Any time of day.", "any_time;requires=mandatory_daytime_protection",
    "Billing and subscriber-information duties are additional and are not per-asset checkable.",
    "conditional", "clear", "", "no",
    "UK-S1 + UK-M1", "Rule 1.25", U_M1, "2019-01-01", "open", "approved",
    "Pay per view services may broadcast up to BBFC 18-rated films", "EN", "high")

add("UK-FLM-006", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "prohibited",
    "BBFC R18-rated films must not be broadcast.",
    "No permitted time.", "prohibited",
    "None. Unchanged by the 2018 MDP review.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "UK-S1", "Rule 1.26", U_S1, "2021-03-03", "open", "approved",
    "BBFC R18-rated films must not be broadcast", "EN", "high")

add("UK-OCC-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "occult_paranormal", "watershed_bound",
    "Demonstrations of exorcism, occult practices or paranormal activity PRESENTED AS REAL must not be shown before the watershed. Programmes treating such activity as entertainment must not be broadcast when significant numbers of children may be expected to be watching. DRAMA, FILM AND COMEDY ARE EXEMPT.",
    "Not before 21:00 where presented as real.", "not_before=21:00;exempt=drama,film,comedy",
    "Three-way split: presented-as-real (pre-watershed ban), entertainment (audience-based restriction), fiction (exempt).",
    "conditional", "clear",
    "The fiction exemption is a frequent over-rating trap.", "no",
    "UK-S1", "Rule 1.27", U_S1, "2021-03-03", "open", "approved",
    "Demonstrations of exorcisms, occult practices and the paranormal", "EN", "high")

# --- Section Three. In scope via the context route, NOT the watershed. Rules 3.2/3.3 are
# --- permitted "except where it is justified by the context", and "context" is Section Two's
# --- defined term whose third factor is the time of broadcast. Added after the
# --- "significant numbers of children" scoping test was shown to be too narrow (C-11).
add("UK-HAT-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "hatred_discrimination", "context_dependent",
    "Material which contains HATE SPEECH must not be included in television services "
    "except where it is justified by the context.",
    "No clock time of its own. The context test imports the time of broadcast as one of its "
    "eight factors, so the hour is an input to the judgment but never determines it.",
    "judgment:context_includes_time_of_broadcast",
    "Hate speech is defined expansively (intolerance on grounds of disability, ethnicity, "
    "social origin, gender, sex, gender reassignment, nationality, race, religion or belief, "
    "sexual orientation, colour, genetic features, language, political or any other opinion, "
    "membership of a national minority, property, birth or age). Distinct from Rule 3.1, "
    "which is an ABSOLUTE prohibition on incitement with no context escape.",
    "judgment_based", "clear",
    "Weigh against Article 10 freedom of expression; Ofcom decisions here turn on editorial "
    "framing (debate, drama, news) more than on the hour. Never resolve this automatically: "
    "a later hour does not cure hate speech, it is only one factor among eight. Escalate every "
    "hit to a UK compliance reviewer.",
    "yes", "UK-S3", "Rule 3.2", U_S3, "2020-12-31", "open", "approved",
    "spread, incite, promote or justify hatred", "EN", "medium")

add("UK-HAT-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "hatred_discrimination", "context_dependent",
    "Material which contains ABUSIVE OR DEROGATORY TREATMENT of individuals, groups, "
    "religions or communities must not be included in television services except where it "
    "is justified by the context.",
    "No clock time of its own. Same context route as Rule 3.2.",
    "judgment:context_includes_time_of_broadcast",
    "Lower threshold than Rule 3.2: abuse or derogatory treatment need not reach hate speech. "
    "Cross-refers to Rule 4.2 (Religion). Catches comedy and satire aimed at a community, "
    "which is the common false-negative for an automated classifier.",
    "judgment_based", "clear",
    "The most likely rule in the whole table to be missed by a content-description pipeline, "
    "because the trigger is TREATMENT rather than depicted subject matter: a description listing "
    "no violence, sex or drugs can still breach this. Escalate to a UK compliance reviewer.",
    "yes", "UK-S3", "Rule 3.3", U_S3, "2020-12-31", "open", "approved",
    "abusive or derogatory treatment of individuals", "EN", "medium")

# --- "Other restrictions" limb of the requirement. In scope because each CONDITIONS or
# --- SUBSTITUTES FOR the age/time answer rather than sitting alongside it (SCOPE.md).
# --- Without UK-ACC-001 the token `requires=mandatory_daytime_protection` is an unexplained
# --- string and the any-hour permission it gates cannot be audited.
add("UK-ACC-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film; pay_per_view; scheduled_channels_with_mdp", "access_control", "n/a",
    "DEFINITION. 'Mandatory restricted access' means a PIN-protected system, or other "
    "equivalent protection, which CANNOT BE REMOVED BY THE USER and which restricts access "
    "solely to those authorised to view.",
    "Not a time rule. This is the definition the any-hour permissions are conditional on.",
    "n/a;standard=cannot_be_removed_by_user",
    "The operative words are 'cannot be removed by the user'. A service-level parental "
    "control the viewer can switch off is NOT mandatory restricted access, so a title relying "
    "on it for an any-hour permission is in breach. Distinct from 'mandatory daytime "
    "protection', the pre-2100/post-0530 variant - the two are not interchangeable.",
    "bright_line", "clear", "", "no",
    "UK-S1", "Rule 1.18 (meaning)", U_S1, "2020-12-31", "open", "approved",
    "which cannot be removed by the user", "EN", "high")

add("UK-ACC-002", "UK", "Ofcom", "guidance", 3, "yes",
    "premium_subscription_film; pay_per_view; scheduled_channels_with_mdp", "access_control", "n/a",
    "IMPLEMENTATION. Restricted access must be provided AS THE DEFAULT. A service may not "
    "satisfy the requirement by offering a PIN the viewer has to set up; the gate must be on "
    "before the viewer arrives.",
    "Not a time rule. Determines whether the any-hour permission is validly engaged.",
    "n/a;standard=on_by_default",
    "The most commonly misread requirement in the access-control set, because an opt-in PIN "
    "looks like compliance and is not. Guidance rather than Code text, hence rank 3, but it "
    "states how Ofcom reads a binding rule.",
    "bright_line", "clear", "", "no",
    "UK-G2", "Guidance Notes Section One, Rules 1.24-1.25", U_G2, "2015-03-30", "open",
    "approved",
    "as the default, rather than requiring PIN setting by the viewer", "EN", "medium")

add("UK-ACC-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film; pay_per_view; scheduled_channels_with_mdp", "audience_information", "n/a",
    "CONDITIONS PRECEDENT to the any-hour permission, from the CURRENT Code text. Clear "
    "information must be provided with the content to help adults assess its suitability "
    "for children, AND the mandatory daytime protection in place must be CLEARLY EXPLAINED "
    "TO ALL VIEWERS. A gate nobody has been told about does not satisfy the rule.",
    "Not a time rule itself, but the any-hour permission does not exist unless satisfied.",
    "n/a;requires=audience_information;requires=detailed_billing",
    "These read as housekeeping and are not - they are conditions on the permission. The "
    "UK's nearest analogue to the French signaletique, discharged by INFORMATION rather than "
    "a pictogram, so a pipeline looking for a French-style on-screen symbol will report the "
    "UK as having no equivalent, which is wrong.",
    "conditional", "clear",
    "The sufficiency of the information is a judgment; its ABSENCE is not. Treat a missing "
    "information commitment as a bright-line fail and the adequacy of wording as a review item.",
    "yes", "UK-S1", "Rules 1.24, 1.25", U_S1, "2020-12-31", "open", "approved",
    "must be clearly explained to all viewers", "EN", "high")

add("UK-TRL-002", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "trailers", "watershed_bound",
    "Trailers are caught by the under-eighteens scheduling rules in their own right. A "
    "trailer does NOT inherit the permission of the programme it advertises.",
    "The trailer is assessed against the slot it occupies, not the slot of its feature.",
    "standard=assessed_in_own_slot",
    "The practical trap: a compliant post-watershed film generates a trailer that runs in a "
    "daytime break and breaches, with no change to the trailer's content. A pipeline that "
    "reasons only about the feature asset cannot see this.",
    "bright_line", "clear", "", "no",
    "UK-G2", "Guidance Notes Section One", U_G2, "2015-03-30", "open", "approved",
    "both programmes and trailers are subject to this rule", "EN", "medium")

# --- THE SUBSTITUTION PROOF. The watershed is not relaxed by a technical measure, it is
# --- DISAPPLIED. Ranked above the general watershed rule so it wins on conflict. Without this
# --- row a decision engine bars a title pre-21:00 that the Code permits at any hour.
add("UK-SCH-007", "UK", "Ofcom", "regulator_binding", 1, "yes",
    "all_linear_tv", "scheduling_general", "exempt",
    "THE WATERSHED DOES NOT APPLY AT ALL to a channel while mandatory daytime protection is "
    "in place. This is a disapplication, not a relaxation: the time question is removed "
    "rather than adjusted.",
    "No window. The watershed ceases to bind while MDP is in place.",
    "any_time;override=watershed_disapplied_when_mdp_in_place",
    "Read with Rules 1.24 and 1.25. This is the concrete mechanism behind AVMSD art. 6a "
    "offering scheduling OR technical measures as ALTERNATIVES, and the reason this system "
    "reports three axes rather than two: an access control can remove the hours question "
    "entirely. Ranked 1 so it defeats the general watershed rule (UK-SCH-002) on conflict.",
    "bright_line", "clear",
    "Verify the MDP is genuinely non-removable before applying this. The disapplication is "
    "only as good as the gate: if the protection fails UK-ACC-001's 'cannot be removed by the "
    "user' test, the watershed snaps back and the title is in breach from the first frame.",
    "yes", "UK-S1", "Rule 1.4 (meaning of the watershed)", U_S1, "2020-12-31", "open",
    "approved",
    "does not apply to channels when mandatory daytime protection", "EN", "high")

# --- The six locking criteria in full. The predicted rules captured THAT a decoder lock
# --- exists; the primary specifies it precisely enough to AUDIT against, which is the
# --- difference between "a PIN is required" and a testable compliance standard.
add("FR-CV-008", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "access_control", "V_-18",
    "LOCKING SPECIFICATION for category V. The personal code must be AT LEAST FOUR DIGITS, "
    "must NOT be 0000, must NOT be visible on screen, and must be used EXCLUSIVELY for this "
    "purpose. The subscriber MUST NOT be able to deactivate the lock. It must re-arm on every "
    "change of broadcast context - channel change, standby, decoder shutdown, decoder or card "
    "change - activate for each new category V programme, and stay synchronised for its whole "
    "duration.",
    "Not a time rule. These are the conditions the 00:00-05:00 permission depends on.",
    "n/a;requires=decoder_lock;standard=four_digits_not_0000;standard=cannot_be_deactivated",
    "The French analogue of the UK 'cannot be removed by the user' test, but far more "
    "prescriptive. A service meeting the UK standard does NOT automatically meet this one: "
    "the exclusivity requirement - the code may not double as a general parental PIN - and "
    "the re-arm-on-context-change requirement have no UK equivalent.",
    "bright_line", "clear",
    "Engineering compliance, not editorial. Verify with the platform operator rather than the "
    "scheduling team: a broadcaster may not know whether its distributor's decoder satisfies "
    "criteria (e) or (f).",
    "yes", "FR-R2", "notice of 15 Dec 2004, II.B.1(a)-(f)", U_FRV, "2004-12-15", "open",
    "approved",
    "must include at least four digits (except 0000)", "EN", "high")

add("FR-CV-009", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "scope", "V_-18",
    "COMPLIANCE DEADLINES HAVE ALL ELAPSED: criteria (a)-(d) by 1 Jan 2005, (f) by 1 Jan 2006, "
    "(e) by 1 Jan 2008, and the transitional regime ended 1 Jan 2008. The scheme is fully in "
    "force with NO transitional relief available. Publishers and distributors must also report "
    "to the regulator ANNUALLY on implementation.",
    "Not a time rule.",
    "n/a;requires=annual_report",
    "Recorded because those elapsed dates were the specific reason this instrument's currency "
    "was doubted. Elapsed means FULLY IN FORCE, not expired - the opposite of the worry. An "
    "old instrument whose deadlines have all passed is the strongest kind of current law.",
    "bright_line", "clear", "", "no",
    "FR-R2", "notice of 15 Dec 2004, II.B.2 and III.B", U_FRV, "2004-12-15", "open",
    "approved",
    "a report on the implementation of the measures taken", "EN", "high")

# ===================== FROM THE GUIDANCE: calibration and worked examples =====================
# These come from guidance rather than Code text. Several describe situations the Code does not
# mention, and the most useful are the ones that contradict a natural assumption.

# --- The watershed is not a cliff edge. A scheduler treating 21:00 as a gate can pass every
# --- bright-line check and still breach.
add("UK-SCH-008", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "scheduling_general", "watershed_bound",
    "TRANSITION. Material scheduled to start before but continue past 21:00 must not ABRUPTLY "
    "become unsuitable, and content commencing after the watershed must observe a SMOOTH "
    "TRANSITION to more adult material. It must not open with the strongest content it holds.",
    "Applies across the 21:00 and 05:30 boundaries rather than at a single instant.",
    "not_before=21:00;standard=smooth_transition",
    "The watershed is a ramp, not a gate. A film cleared for 21:00 that opens on its most "
    "violent scene breaches this even though every clock-time check passes. REGULATOR "
    "EXAMPLES: Hell's Kitchen USA (ITV2) and Amores Perros (TCM) were both decided on this "
    "point. Viewers can be concerned at strong adult material immediately after the watershed "
    "when a significant number of children could still be watching.",
    "judgment_based", "clear",
    "Needs the running order, not just the start time - information a content description "
    "usually does not carry. Flag whenever a post-watershed asset's first scene is among its "
    "strongest.",
    "yes", "UK-G1", "Rule 1.6 guidance", U_G1, "2015-03-30", "open", "approved",
    "It should not commence with the strongest material", "EN", "high")

# --- A +1 channel makes the identical file compliant on one service and not on the other.
add("UK-SCH-009", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "scheduling_general", "watershed_bound",
    "TIMESHIFT (+1) SERVICES. Where the same content is broadcast an hour later on a +1 "
    "service, the later transmission must itself be suitable for the audience it will then "
    "reach. Broadcasters may need to schedule EARLIER on the main service so the +1 "
    "transmission still concludes before children return from school.",
    "Effective hours differ between a service and its +1 by one hour, in both directions.",
    "not_before=21:00;override=plus_one_shifts_effective_slot",
    "The same file is compliant on one service and in breach on the other, with no editorial "
    "change whatsoever. A pipeline keyed to 'the asset' cannot represent this; it must reason "
    "per transmission. Note the risk runs the counter-intuitive way too: content placed while "
    "children are at school lands an hour later, when they are home.",
    "conditional", "clear",
    "Requires knowing whether a +1 service exists for the channel and whether the asset is "
    "carried on it. Rarely present in a content description - ask.",
    "yes", "UK-G1", "+1 services guidance", U_G1, "2015-03-30", "open", "approved",
    "the same content is broadcast an hour later", "EN", "high")

# --- Why trailers do not inherit: the viewer cannot opt out of something unannounced.
add("UK-TRL-003", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "trailers", "watershed_bound",
    "TRAILERS ARE UNANNOUNCED. Because trailers are not signposted in advance, viewers meet "
    "them unawares, so a trailer for post-watershed content shown pre-watershed must contain "
    "ONLY pre-watershed-appropriate material. Trailers restricted away from children's "
    "programmes should also be kept away from sport and family entertainment, which attract "
    "significant child audiences.",
    "Judged in its own slot, never inheriting the advertised programme's permission.",
    "standard=assessed_in_own_slot;not_near=children_programmes;not_near=family_audience_programmes",
    "This supplies the REASON behind the inheritance rule and extends it: the restriction is "
    "not only around children's programming but around anything drawing a child audience, "
    "which includes live sport - a slot nobody thinks of as a child-protection risk. "
    "REGULATOR EXAMPLES: Candy Bar Girls (Channel 5) and the Stylista trailer (Channel Five).",
    "conditional", "clear",
    "A trailer carrying images that would warrant a warning before the full programme is "
    "unlikely to be acceptable pre-watershed at all.",
    "yes", "UK-G1", "Trailers guidance", U_G1, "2015-03-30", "open", "approved",
    "so they come across them unawares", "EN", "high")

# --- Bleeping is not a cure.
add("UK-LAN-010", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "strong_language", "watershed_bound",
    "MASKING IS NOT AUTOMATIC COMPLIANCE. Where masked ('bleeped') offensive language is "
    "frequent, the cumulative effect on viewers can be similar to that of the unedited "
    "language. Frequent use may require more rigorous editing, or may mean the programme is "
    "not appropriate pre-watershed at all.",
    "Does not create its own window; governs whether a pre-watershed edit works.",
    "judgment:cumulative_effect_of_masking",
    "The common and expensive mistake: assume a post-watershed programme can be made "
    "daytime-safe by bleeping. Frequency is the trigger, not the presence of masking, so an "
    "edit can be technically thorough and still fail. Some content cannot be edited down to "
    "pre-watershed at all because of adult THEMES rather than specific words.",
    "judgment_based", "clear",
    "Requires a count and distribution of instances, which a content description rarely "
    "gives. Escalate any pre-watershed broadcast of material originally made for after it.",
    "yes", "UK-G1", "Post-watershed content edited for pre-watershed transmission",
    U_G1, "2015-03-30", "open", "approved",
    "cumulative effect on viewers similar to that of", "EN", "high")

add("UK-SCH-010", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "scheduling_general", "watershed_bound",
    "AUDIENCE COMPOSITION BEFORE 21:00 IS NOT UNIFORM. The watershed matters most for children "
    "aged 5 to 8, and trust in pre-watershed programming is essential particularly in the "
    "approach to 19:30. Programmes starting before the watershed and ending after it may hold "
    "special appeal for children, ESPECIALLY DURING SCHOOL HOLIDAYS.",
    "The nearer to 19:30, the stronger the expectation - a gradient, not a flat pre-21:00 band.",
    "not_before=21:00;judgment:proximity_to_1930;judgment:school_holidays",
    "Contradicts the intuition that 20:55 is nearly post-watershed and therefore nearly free. "
    "And school holidays change the audience without changing the clock, so the same slot on "
    "the same channel carries a different risk in August.",
    "judgment_based", "clear",
    "Transmission DATE is needed, not only the time. A content description that gives a slot "
    "but no date cannot settle this.",
    "yes", "UK-G2", "Guidance Notes Section One, Rules 1.3-1.6", U_G2, "2015-03-30", "open",
    "approved",
    "especially during school holidays", "EN", "high")

add("UK-IMI-010", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "imitable_behaviour", "watershed_bound",
    "EASILY IMITABLE METHODS. Hanging, or preparations for hanging, must be treated with "
    "particular care if easily imitable, above all before the watershed, unless the setting "
    "gives strong grounds for believing imitation is unlikely.",
    "Pre-watershed is the aggravating factor; the concern does not vanish after 21:00.",
    "not_before=21:00;judgment:imitability_and_setting",
    "The operative test is IMITABILITY plus SETTING, not the presence of the act. A period "
    "drama and a contemporary bedroom scene are judged differently on identical events, which "
    "is why RUN 1 records `treatment` as a separate field from what happens.",
    "judgment_based", "clear",
    "Overlaps with the suicide and self-harm rules and must never be auto-decided. Escalate "
    "to a UK compliance reviewer in every case.",
    "yes", "UK-G2", "Guidance Notes Section One, Rule 1.13", U_G2, "2015-03-30", "open",
    "approved",
    "if easily imitable", "EN", "high")

add("UK-CTX-010", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "definition", "n/a",
    "AUDIENCE SIZE AND BROADCASTER SIZE. A larger audience, such as on a mainstream channel "
    "with popular appeal, raises the contextual justification required. A small broadcaster is "
    "NOT thereby permitted to transmit potentially harmful material without adequate "
    "protection: the obligation applies to all programmes regardless of reach.",
    "Not a time rule. Expands the time-of-broadcast factor in the context definition.",
    "n/a;judgment:audience_size",
    "Resolves a real asymmetry: audience size can make a decision STRICTER but never looser. "
    "Expect the reverse argument from a niche channel; it is not available.",
    "judgment_based", "clear",
    "The channel's typical audience size and profile is required, and is almost never in a "
    "content description.",
    "yes", "UK-G3", "Guidance Notes Section 2, meaning of context", U_G3, "2017-07-18",
    "open", "approved",
    "The timing of a broadcast may affect the composition of its audience", "EN", "high")

add("UK-WRN-002", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "audience_information", "n/a",
    "WARNINGS MUST BE ADEQUATE, NOT MERELY PRESENT. The effectiveness of a warning depends on "
    "its frequency and its positioning within the programme. For a longer programme a single "
    "message at the beginning may not be sufficient.",
    "Not a time rule. Governs whether an information-based mitigation actually works.",
    "n/a;requires=warning;standard=frequency_and_positioning",
    "Matters because a warning is one of the main ways a broadcaster earns a slot it would "
    "not otherwise get. A pipeline that records 'warning: yes' as a boolean cannot represent "
    "this, and will credit an inadequate warning with mitigation it has not earned.",
    "judgment_based", "clear",
    "Needs the warning's wording, placement and repetition - not just that one exists. Treat "
    "a bare 'warning given' claim as unverified.",
    "yes", "UK-G3", "Guidance Notes Section 2, Rule 2.3", U_G3, "2017-07-18", "open",
    "approved",
    "a single message at the beginning", "EN", "high")

# --- The clearest authority for this system's central architectural claim, and it is Ofcom's
# --- own words rather than my inference. The Code deliberately BROKE the old link between a
# --- film's certificate and its permitted slot.
add("UK-FLM-010", "UK", "Ofcom", "guidance", 3, "yes",
    "all_linear_tv", "film_carryover", "watershed_bound",
    "A BBFC CERTIFICATE DOES NOT SET THE SLOT. The legacy ITC code scheduled films by strict "
    "reference to their BBFC rating; the Ofcom Code has in the main DISPENSED with that link. "
    "Films are scheduled like any other content, appropriately for the audience. A recent BBFC "
    "classification is a useful INDICATION of suitability, not a determinant.",
    "No window of its own. Governs how much weight a certificate carries in the hours decision.",
    "judgment:certificate_is_evidence_not_determinant",
    "The single most important row for anyone building on this table, because it is the "
    "regulator stating the rating/hours separation directly rather than me inferring it. "
    "CALIBRATION the guidance supplies: since 'children' means people under fifteen and "
    "material unsuitable for children should not generally be shown before 2100, it is "
    "UNLIKELY that a recently BBFC 15-rated film could be scheduled during the day. That is a "
    "usable threshold for a judgment rule - a presumption against, not a prohibition.",
    "judgment_based", "clear",
    "Treat a BBFC certificate as evidence feeding the scheduling judgment, never as the "
    "answer. Reporting a certificate as though it were a broadcast decision is a category "
    "error this rule exists to prevent.",
    "yes", "UK-G2", "Guidance Notes Section One, Rules 1.22-1.26", U_G2, "2015-03-30",
    "open", "approved",
    "dispensed with these rules relating scheduling to ratings", "EN", "high")

# ===================== FROM ENFORCEMENT: Toofan (NTV), bulletin 553, 7 Sep 2026 ==============
# The only decided case in the table. It calibrates where the Code only gestures.

add("UK-PRE-010", "UK", "Ofcom", "precedent", 4, "yes",
    "all_linear_tv", "violence", "watershed_bound",
    "DECIDED CASE. A BBFC 15 action film containing frequent graphic violence - mass "
    "shootings, a beheading with the severed head then carried on screen, a man choked to "
    "death - broadcast at 11:30 BREACHED Rule 1.3. Ofcom weighed the BBFC 15 certificate as "
    "indicating unsuitability for under-15s, the absence of any warning or signposting, and "
    "the repeated depictions of killing as unsuitable for daytime viewing.",
    "11:30 is far pre-watershed; the finding does not fix a permissible hour, only that this "
    "one was not.",
    "not_before=21:00;precedent=bbfc15_graphic_violence_breaches_at_1130",
    "The table's only hard calibration point for violence. Useful as an ANCHOR, not a "
    "threshold: it says this combination at this hour breached, not where the line sits. "
    "Note what did NOT save the broadcaster - an apology, an internal investigation, the "
    "explanation that a newly appointed scheduler made an unintentional error, and refresher "
    "training already completed. Mitigation after transmission does not undo a breach, which "
    "is the whole argument for catching it beforehand.",
    "judgment_based", "clear",
    "One case is not a calibration set. Treat as the single datum it is, and collect more "
    "before relying on interpolation between it and anything else.",
    "yes", "UK-P1", "Bulletin issue 553, Toofan, NTV", U_P1, "2026-09-07", "open", "approved",
    "well before the watershed without any warning or signposting", "EN", "high")

# --- The axes are independent, demonstrated by a regulator rather than argued by me.
add("UK-CTX-011", "UK", "Ofcom", "precedent", 4, "yes",
    "all_linear_tv", "definition", "n/a",
    "CONTEXT CAN JUSTIFY THE CONTENT AND STILL NOT JUSTIFY THE SLOT. In Toofan, Ofcom opened "
    "under both the scheduling rule and the offence rule, then DROPPED the offence limb - the "
    "violence was sufficiently contextualised within the film - while still finding a "
    "SCHEDULING breach on the same broadcast.",
    "Not a time rule. Governs how the offence and scheduling determinations relate.",
    "n/a;standard=offence_and_scheduling_decided_separately",
    "The strongest available authority for this system's three-axis design, and it comes from "
    "a decided case rather than from inference. Editorial context defended the material as "
    "material; it did nothing for the hour. So a pipeline that resolves 'is this justified by "
    "the context?' once, and reuses the answer for both questions, will reach the wrong "
    "result in exactly this shape of case - and this shape is common, because a competent "
    "film almost always contextualises its own violence.",
    "bright_line", "clear",
    "Run the offence and scheduling determinations separately and report both. Never let a "
    "finding of editorial justification discharge the scheduling question.",
    "yes", "UK-P1", "Bulletin issue 553, footnote 2 and Rule 1.3 decision", U_P1,
    "2026-09-07", "open", "approved",
    "sufficiently contextualised within the film", "EN", "high")

# --- A factor the Code does not mention and I did not have.
add("UK-SCH-011", "UK", "Ofcom", "precedent", 4, "yes",
    "all_linear_tv", "scheduling_general", "watershed_bound",
    "THE CULTURAL AND RELIGIOUS CALENDAR AFFECTS AUDIENCE COMPOSITION. Ofcom weighed that the "
    "broadcast fell during the three-day Eid-ul-Adha celebrations, when many Muslim families "
    "and communities gather together, as increasing the likelihood that children were in the "
    "audience.",
    "Does not move the watershed. Raises the expected child audience within existing hours.",
    "not_before=21:00;judgment:cultural_or_religious_calendar",
    "Nothing in the Code text says this; it emerges only from a decided case. It generalises "
    "badly and that is the point - the relevant festivals depend on the channel's community, "
    "so a system scaled across countries CANNOT infer them from a single calendar. Pairs with "
    "the school-holidays factor: both change who is watching without changing the clock or "
    "the content.",
    "judgment_based", "clear",
    "Needs the transmission DATE and knowledge of the channel's audience. A date alone is not "
    "enough without knowing which communities the service serves - ask a local expert rather "
    "than deriving it from a public-holiday table.",
    "yes", "UK-P1", "Bulletin issue 553, Rule 1.3 decision", U_P1, "2026-09-07", "open",
    "approved",
    "increasing the likelihood that children could have been watching", "EN", "high")

add("UK-WRN-003", "UK", "Ofcom", "precedent", 4, "yes",
    "all_linear_tv", "audience_information", "n/a",
    "WARNINGS SHOULD CONVEY SEVERITY, NOT ONLY PRESENCE. Ofcom's research found audiences "
    "expect content warnings to indicate not only that violence is present but how severe it "
    "is, using terms such as 'graphic' or 'explicit'. Audiences also expect graphic and "
    "realistic violence to be post-watershed and rely on warnings to manage viewing.",
    "Not a time rule. Determines whether a warning earns the mitigation claimed for it.",
    "n/a;requires=warning;standard=indicates_severity",
    "Makes a boolean 'warning: yes' field inadequate. A warning saying 'contains violence' "
    "before content audiences would describe as graphic does not meet the expectation this "
    "describes, so it should not be credited as mitigation.",
    "judgment_based", "clear",
    "Capture the warning's actual wording. Treat an unquoted claim that a warning was given "
    "as unverified.",
    "yes", "UK-P1", "Bulletin issue 553, audience research cited in the decision", U_P1,
    "2026-09-07", "open", "approved",
    "not only the presence of violence but also its severity", "EN", "high")

add("UK-REL-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "religion", "audience_based",
    "Religious programmes containing claims that a LIVING PERSON (or group) has SPECIAL POWERS "
    "OR ABILITIES must treat such claims with due objectivity AND must not broadcast such claims "
    "when significant numbers of children may be expected to be watching.",
    "No clock time. Restriction is keyed to the likely child audience, not the watershed.",
    "not_when=significant_numbers_of_children_watching",
    "Double test, like Rule 2.5: due objectivity AND the audience restriction. Section Four "
    "otherwise concerns religious content standards and is out of scope.",
    "judgment_based", "clear",
    "THIS RULE SITS OUTSIDE SECTION ONE and was missing from v1. Found by reviewing sections "
    "3-10 for relevance. It is the close cousin of Rule 1.27 (occult/paranormal as "
    "entertainment), which uses the same 'significant numbers of children' test rather than the "
    "watershed - so a solution that only reads Section One misses a genuine child-audience "
    "broadcast restriction. Note the test is AUDIENCE-based, not time-based: there is no hour "
    "that automatically satisfies it.",
    "yes", "UK-S4", "Rule 4.7", U_S4, "2020-12-31", "open", "approved",
    "special powers or abilities", "EN", "high")

add("UK-WEL-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "participant_welfare", "context_dependent",
    "Due care must be taken over the physical and emotional welfare and the dignity of under-18s who take part in or are otherwise involved in programmes, IRRESPECTIVE OF ANY CONSENT given by the participant or a parent/guardian. Under-18s must not be caused unnecessary distress or anxiety.",
    "Applies at all times.", "n/a",
    "Consent is expressly irrelevant.",
    "judgment_based", "clear",
    "Relevant where a content description involves minors as participants; not a scheduling rule.", "no",
    "UK-S1", "Rules 1.28-1.29", U_S1, "2021-03-03", "open", "approved",
    "Due care must be taken over the welfare and the dignity", "EN", "high")

add("UK-OFF-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "offence_general", "context_dependent",
    "Material which may cause offence must be justified by the context. Such material may include offensive language, violence, sex, sexual violence, humiliation, distress, violation of human dignity, and discriminatory treatment or language.",
    "Context-determined.", "judgment:context",
    "Supplies the harm categories the UK actually recognises - useful as the UK category vocabulary.",
    "judgment_based", "clear", "", "no",
    "UK-S2", "Rule 2.3", U_S2, "2021-03-03", "open", "approved",
    "material which may cause offence is justified by the context", "EN", "high")

add("UK-IMI-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "imitable_behaviour", "context_dependent",
    "Programmes must not include material (whether in individual programmes OR IN PROGRAMMES TAKEN TOGETHER) which, taking into account the context, condones or glamorises violent, dangerous or seriously antisocial behaviour and is likely to encourage others to copy such behaviour.",
    "Applies at all times, context-determined.", "judgment:context",
    "'In programmes taken together' makes cumulative, cross-programme assessment explicit.",
    "judgment_based", "clear",
    "Cross-programme accumulation cannot be assessed from a single asset description - flag for channel-level review.",
    "yes", "UK-S2", "Rule 2.4", U_S2, "2021-03-03", "open", "approved",
    "condones or glamorises violent, dangerous or seriously antisocial", "EN", "high")

add("UK-SUI-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "suicide_self_harm", "context_dependent",
    "METHODS of suicide and self-harm must not be included in programmes except where they are editorially justified AND ALSO justified by the context.",
    "Context-determined; no clock time.", "judgment:double_test",
    "DOUBLE test - both limbs required. A single-condition check under-rates.",
    "judgment_based", "clear",
    "Always escalate. Two reasons: the double test ('editorially justified' AND 'justified by "
    "the context') is easy to collapse into one, and the downside of an under-rating here is "
    "imitative harm rather than mere offence. No automated verdict should stand alone on "
    "suicide or self-harm method depiction.", "yes",
    "UK-S2", "Rule 2.5", U_S2, "2021-03-03", "open", "approved",
    "Methods of suicide and self-harm must not be included in programmes", "EN", "high")

add("UK-MUS-001", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv; music_channels", "music_videos", "context_dependent",
    "Pre-watershed music videos: sexualised images not banned but must be editorially justified and appropriately limited; explicit sexual behaviour avoided; intrusive or prolonged shots of body parts increase sexual impact; BDSM imagery not prohibited but explicit imagery avoided (shot length, repetition and overall theme considered); provocative/sexualised dancing limited; lyrics clearly focused on sex avoided.",
    "Thresholds tighten before 21:00.", "not_before=21:00;unless=limited_and_justified",
    "NICHE MUSIC CHANNELS STILL CARRY RESPONSIBILITY toward possible child viewers - a small or genre-specific audience does not remove the duty. Whether the video was supplied as a child-audience edit (e.g. marked 'pre 9pm') is a relevant input.",
    "judgment_based", "clear",
    "Lyrics that seem mild on audio alone can become highly sexualised when paired with sexual imagery - so audio and video must be assessed TOGETHER, not independently. Independent tagging systematically under-rates music videos.",
    "yes", "UK-G1", "UK-G1 s.2", U_G1, "", "open", "approved",
    "the sexualised clothing and dance routines of performers", "EN", "high")

add("UK-MUS-002", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv; music_channels", "nudity", "watershed_bound",
    "Pre-watershed music videos should not show performers inadequately covered, particularly the breasts, genitals or buttocks. Underwear and bikinis are not prohibited; whether the clothing is PRESENTED SEXUALLY is what matters.",
    "Restriction bites before 21:00.", "not_before=21:00",
    "Fetish clothing combined with sexual behaviour needs particular care.",
    "conditional", "clear", "", "no",
    "UK-G1", "UK-G1 s.2", U_G1, "", "open", "approved",
    "the sexualised clothing and dance routines of performers", "EN", "high")

add("UK-MUS-003", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv; music_channels", "suicide_self_harm", "context_dependent",
    "In music videos, violence should be limited and justified by context, and not explicit, gratuitous or easily imitable. Images of suicide are not banned but must be very carefully limited so that no details could prompt imitation.",
    "Context-determined, tighter pre-watershed.", "not_before=21:00;unless=very_carefully_limited",
    "Images of suicide are not banned outright, which makes this a calibration question rather "
    "than a yes/no one.",
    "judgment_based", "clear",
    "Escalate. 'Very carefully limited so that no details could prompt imitation' is a threshold "
    "about DETAIL, not about presence, so it cannot be decided from a content tag alone - it "
    "needs the actual shot description. Same imitative-harm downside as UK-SUI-001.", "yes",
    "UK-G1", "UK-G1 s.2", U_G1, "", "open", "approved",
    "bondage, dominance and sadomasochism in music videos", "EN", "high")

add("UK-TRL-001", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv", "trailers", "watershed_bound",
    "Trailers shown before the watershed for post-watershed programmes must contain only material appropriate for pre-watershed broadcast. Viewers do not choose to watch trailers. Trailers may need restricting around children's programming, family shows and sports coverage.",
    "Pre-watershed trailers held to pre-watershed standard.", "not_before=21:00;standard=pre_watershed_content",
    "The parent programme's own permitted slot does NOT license its trailer.",
    "judgment_based", "clear", "", "no",
    "UK-G1", "UK-G1 s.1", U_G1, "", "open", "approved",
    "include only content that is appropriate for a pre-watershed audience", "EN", "high")

add("UK-SCH-006", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "Specific care areas: family viewing shows (suit family viewing throughout; extra caution if running past 21:00; daytime repeats need separate thought); soaps (each episode scheduled on its own merits - a long-running storyline does not itself supply context); post-watershed content edited for daytime (some content remains unsuitable regardless of editing; FREQUENT BLEEPING HAS A CUMULATIVE EFFECT).",
    "Context-determined.", "judgment:appropriate_scheduling",
    "+1 (timeshift) services need specific attention: a 21:00 broadcast becomes 22:00 on +1, but a 20:00 broadcast becomes 21:00.",
    "judgment_based", "clear",
    "The +1 point is a good adversarial test case - it changes the answer with no change to content.",
    "no", "UK-G1", "UK-G1 s.1", U_G1, "", "open", "approved",
    "family viewing programmes", "EN", "high")

add("UK-SVC-001", "UK", "Ofcom", "regulator_binding", 2, "scope_rule",
    "bbc_odps", "scope", "n/a",
    "The scheduling requirements in Rules 1.3, 1.4, 1.5 and 1.6 DO NOT APPLY to BBC on-demand programme services.",
    "n/a", "n/a",
    "For BBC ODPS, 'context' excludes scheduling/time of broadcast and instead covers the manner of access, including measures to prevent children viewing.",
    "bright_line", "clear",
    "Out of scope for linear TV but recorded so the scope boundary is explicit and testable.", "no",
    "UK-S1", "S1 note / fn.6", U_S1, "2021-03-03", "open", "approved",
    "Scheduling requirements in Rules 1.3, 1.4, 1.5 and 1.6 do not apply to BBC ODPS.",
    "EN", "high")

add("UK-LAW-001", "UK", "Parliament", "statute", 1, "framework_only",
    "all_linear_tv", "legal_basis", "n/a",
    "Ofcom has a statutory duty to set standards ensuring 'that persons under the age of eighteen are protected'. This is the legal basis for Section One of the Broadcasting Code.",
    "n/a", "n/a",
    "Also s.3(4)(h). The AVMS Regulations 2020 (SI 2020/1062) implemented the revised AVMSD duties; content standards for broadcast TV remain in the Ofcom Code.",
    "bright_line", "clear",
    "Never cite as the operative rule for a decision - it sets the duty, not the threshold.", "no",
    "UK-L1", "s.319(2)(a)", U_L1, "2003-07-17", "open", "approved",
    "that persons under the age of eighteen are protected", "EN", "high")

# ================================================================ FRANCE
add("FR-LAW-001", "FR", "Arcom", "statute", 1, "yes",
    "all_linear_tv", "serious_harm", "prohibited",
    "No programme liable to SERIOUSLY harm (nuire gravement) the physical, mental or moral development of minors may be made available by a radio or television service.",
    "No permitted time.", "prohibited",
    "None. Tier 1 of the French two-tier harm standard - no time or technical measure cures it.",
    "bright_line", "clear",
    "The French analogue of Ofcom Rule 1.1. Hard pre-check in code.", "no",
    "FR-L1", "Loi 86-1067 art. 15", U_FRL, "1986-09-30", "open", "approved",
    "nuire gravement", "FR", "high")

add("FR-LAW-002", "FR", "Arcom", "statute", 1, "yes",
    "all_linear_tv", "legal_basis", "n/a",
    "Programmes liable to HARM (nuire) the physical, mental or moral development of minors must not be made available UNLESS it is ensured - by the CHOICE OF BROADCAST TIME and by ANY APPROPRIATE TECHNICAL PROCESS - that minors are not normally liable to see or hear them.",
    "Determined by the instrument chosen (time and/or technical measure).",
    "framework:time_and_or_technical",
    "Tier 2 of the two-tier standard. Mirrors AVMSD art. 6a(1). This is the statutory hook for the entire French time-restriction system AND for the category V locking regime.",
    "bright_line", "clear",
    "The two-tier structure (seriously harm vs harm) must be represented or absolute bans get treated as schedulable.",
    "no", "FR-L1", "Loi 86-1067 art. 15", U_FRL, "1986-09-30", "open", "approved",
    "nuire à l'épanouissement physique, mental ou moral des mineurs", "FR", "high")

add("FR-VIO-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "category_independent",
    "Between 06:00 and 22:00, and a fortiori in programmes intended for young audiences, violence - INCLUDING PSYCHOLOGICAL VIOLENCE - must not be able to be perceived as continuous, as the only solution to conflicts, or in an exacerbated form.",
    "Restriction applies 06:00-22:00.", "restricted_window=06:00-22:00",
    "CATEGORY-INDEPENDENT: a programme can be category I or II and still breach this. Replaced by delib. 2014-17.",
    "judgment_based", "clear",
    "A solution that only reasons about the I-V categories will miss this rule entirely.", "yes",
    "FR-R1c", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "la violence, meme psychologique", "FR", "high")

add("FR-VIO-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "category_independent",
    "Programmes on HISTORICAL OR CONTROVERSIAL subjects may be broadcast before 22:00 if the editor provides EDUCATIONAL SUPPORT going beyond a mere written or spoken warning.",
    "Permits pre-22:00 broadcast subject to the condition.",
    "not_before=22:00;unless=educational_support_beyond_warning",
    "A warning alone is expressly insufficient.",
    "conditional", "clear", "", "no",
    "FR-R1c", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "un accompagnement pédagogique visant à contextualiser les scènes", "FR", "high")

add("FR-VIO-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "fear_distress", "category_independent",
    "For difficult images or testimony concerning particularly dramatic events, in news and other programmes, the editor must take precautions and WARN THE PUBLIC IN ADVANCE.",
    "Applies at all times.", "n/a;requires=advance_warning",
    "Applies to news, which France otherwise exempts from classification.",
    "conditional", "clear", "", "no",
    "FR-R1c", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "images difficilement soutenables ou des témoignages", "FR", "high")

add("FR-CLS-001", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "I_tous_publics",
    "Category I - programmes for all audiences. NO pictogram.",
    "No restriction.", "none",
    "The editor classifies via an internal commission de visionnage.",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "categorie I (aucune signaletique) : les programmes pour tous publics", "FR", "high")

add("FR-CLS-002", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "II_-10",
    "Category II (-10) - programmes CERTAIN SCENES of which are liable to shock minors under 10.",
    "See FR-SCH-001.", "see=FR-SCH-001", "",
    "judgment_based", "clear", "", "no",
    "FR-R1c", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "certaines scènes susceptibles de heurter les mineurs de 10 ans", "FR", "high")

add("FR-CLS-003", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "III_-12",
    "Category III (-12) - cinematographic works BANNED TO UNDER-12s IN CINEMAS, and programmes "
    "liable to DISTURB under-12s, in particular where THE PROGRAMME resorts in a REPEATED way "
    "to physical or psychological violence.",
    "See FR-SCH-002/003/004.", "see=FR-SCH-002",
    "A cinema -12 interdiction pulls a film into at least this category. Per CSA practice a film carrying a CNC 'avertissement' is classified -12 for TV.",
    "judgment_based", "clear",
    "'Repeated' is a frequency/pattern test, not a severity test - requires counting across the "
    "asset. IMPORTANT: delib. 2014-17 replaced the fifth alinea of art. 2 and BROADENED this "
    "definition twice over - 'leur scenario recourt de facon repetee ET SYSTEMATIQUE' became "
    "'le programme recourt de facon repetee'. So (a) repetition alone now suffices, systematic "
    "use is no longer required, and (b) the test is the programme as a whole, not just its "
    "scenario. An extraction working from the pre-2014 wording UNDER-RATES. The superseded "
    "pre-2014 wording is recorded in the C-09 conflict entry rather than as a rule row, since "
    "the manifest now carries only current materials. Verified 2026-11-06 against the STORED French primary "
    "text (FR-R1c/FR-R1d), which reads '...notamment lorsque le programme recourt de facon "
    "repetee a la violence physique ou psychologique'. C-10 RESOLVED by the same check: the "
    "words 'sexualite adulte' do NOT occur anywhere in the binding recommendation, so the "
    "'ou evoque la sexualite adulte' limb on Arcom's public page (FR-S1c) is a PRACTICE GLOSS, "
    "not binding text. Do not treat adult sexuality as an independent -12 trigger; the "
    "binding trigger is repeated violence. Arcom may still apply the gloss in practice, so "
    "flag borderline sexual-content cases for review rather than clearing them.",
    "yes", "FR-R1c", "art. 2 al. 5", U_FR1C, "2014-04-09", "open", "approved",
    "les programmes pouvant troubler les mineurs de 12 ans, notamment lorsque le programme "
    "recourt de facon repetee a la violence physique ou psychologique", "FR", "high")

add("FR-FLM-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "context_dependent",
    "The classification a film receives for CINEMA release MAY SERVE AS AN INDICATION for its television classification, but the editor must verify that the rating transfers without harm and MAY STRENGTHEN IT.",
    "n/a - classification input rule", "n/a",
    "French practice is explicitly to RAISE the age limit between cinema and television, because a child who could not enter the cinema can easily be in front of a TV set.",
    "judgment_based", "clear",
    "The CNC/cinema rating is an INPUT, never the output. The TV category is a separate determination and may be stricter.",
    "no", "FR-R1c", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "peut servir d'indication pour leur classification", "FR", "high")

add("FR-FLM-002", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "all_linear_tv", "film_carryover", "n/a",
    "Reclassification procedure: works at least 20 YEARS since their last visa may be submitted for revision for TV broadcast, by JOINT request of editor and producer, at least 8 months before scheduling. Arcom forwards up to 20 requests per year to the Commission de classification, which must opine at least 1 month before broadcast.",
    "n/a - procedural", "n/a",
    "The only route by which the cinema classification commission revisits a rating for television purposes.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Procedural, not a per-asset rating rule. Recorded for completeness.", "no",
    "FR-R1c", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "un délai d'au moins vingt ans s'est écoulé", "FR", "medium")

add("FR-SCH-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "II_-10",
    "Category II (-10): broadcast timing is left to the EDITOR'S DISCRETION, but such programmes MAY NOT BE PLACED WITHIN PROGRAMMES INTENDED FOR CHILDREN.",
    "No clock restriction; placement restriction only.", "none;not_within=children_programmes",
    "Particular care required for trailers scheduled near children's programmes.",
    "conditional", "clear",
    "Note there is NO time restriction for -10 - only a placement restriction. A model that assumes every age label implies an hour will invent one.",
    "no", "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "les horaires de diffusion de ces programmes sont laissés à l'appréciation", "FR", "high")

add("FR-SCH-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "III_-12",
    "Category III (-12) on services OTHER THAN cinema channels and pay-per-view: must not be broadcast BEFORE 22:00.",
    "Not before 22:00.", "not_before=22:00",
    "Subject to the exceptional derogation in FR-SCH-004. Cited against the CURRENT consolidated French text, not the 2005 JORF original: the hours happen to be unchanged since 2005, which is precisely why the amended art. 2 definition slipped past review (C-09).",
    "bright_line", "clear", C02, "no",
    "FR-R1c", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
    "Pour les autres services de television, ces programmes ne doivent pas etre diffuses "
    "avant 22 heures.", "FR", "high")

add("FR-SCH-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "scheduling_general", "III_-12",
    "Category III (-12) on CINEMA CHANNELS and PAY-PER-VIEW services: must not be broadcast ON WEDNESDAYS BEFORE 20:30.",
    "Not Wednesdays before 20:30.", "not_before=20:30;days=Wed",
    "A day-of-week-specific rule. Historically tied to the French school week.",
    "bright_line", "clear", C02, "no",
    "FR-R1c", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
    "pour les chaines cinema et les services de paiement a la seance, ces programmes ne "
    "doivent pas etre diffuses le mercredi avant 20 h 30.", "FR", "high")

add("FR-SCH-004", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "III_-12",
    "Category III (-12) EXCEPTIONAL DEROGATION: may be broadcast AFTER 20:30, EXCEPT on Tuesdays, Fridays, Saturdays, the eve of public holidays, and during school holidays. Capped at 16 PROGRAMMES PER YEAR, of which at most 4 may be works banned to under-12s in cinemas. Remains subject to art. 1 para. 1.",
    "After 20:30, with day and holiday exclusions.",
    "not_before=20:30;except_days=Tue,Fri,Sat,holiday_eve,school_holidays;annual_quota=16;sub_quota=4_cinema_banned_u12",
    "REQUIRES the broadcast DATE (not just time) and the French school-holiday calendar. The annual quota cannot be verified from a single asset description.",
    "conditional", "clear",
    C02 + " QUOTA ALSO CONFIRMED in the French primary text (2026-11-06): 'Ces diffusions "
    "exceptionnelles ne peuvent exceder seize programmes par an, dont au maximum quatre oeuvres "
    "cinematographiques interdites en salles aux mineurs de 12 ans'. The earlier caveat that the "
    "16/4 numbers rested only on the English rendering is withdrawn. Note the quotas remain "
    "channel-level facts: a per-asset prompt cannot verify them and must flag this for "
    "channel-level review.",
    "yes", "FR-R1c", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
    "Ces diffusions exceptionnelles ne peuvent exceder seize programmes par an, dont au "
    "maximum quatre oeuvres cinematographiques interdites en salles aux mineurs de 12 ans", "FR", "high")

add("FR-SCH-005", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "IV_-16",
    "Category IV (-16) on services OTHER THAN cinema channels and pay-per-view: reserved for a warned audience; may only be broadcast AFTER 22:30.",
    "After 22:30.", "not_before=22:30",
    "No derogation equivalent to FR-SCH-004 is provided for category IV.",
    "bright_line", "clear",
    "Corroborated by the Arcom public summary ('as of 10:30 pm'), the French government page, and multiple parliamentary answers - so this row is better evidenced than the cat. III rows.",
    "no", "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "reserves a un public averti, ces programmes sont diffusables seulement apres 20 h 30 "
    "sur les chaines cinema et les services de paiement a la seance et apres 22 h 30 sur les "
    "autres services de television", "FR", "high")

add("FR-SCH-006", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "scheduling_general", "IV_-16",
    "Category IV (-16) on CINEMA CHANNELS and PAY-PER-VIEW services: reserved for a warned audience; may be broadcast AFTER 20:30.",
    "After 20:30.", "not_before=20:30",
    "Two hours earlier than on other services - a pure service-type effect with identical content.",
    "bright_line", "clear",
    "Excellent demonstration that the age label alone does not determine the hour.", "no",
    "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "diffusables seulement apres 20 h 30 sur les chaines cinema et les services de paiement "
    "a la seance", "FR", "high")

add("FR-SCH-007", "FR", "Arcom", "regulator_binding", 2, "pointer",
    "all_linear_tv", "scheduling_general", "V_-18",
    "Category V (-18): broadcast is governed ENTIRELY by Recommandation n. 2004-7 of 15 December 2004.",
    "See FR-CV-002.", "see=FR-CV-002",
    "art. 3 of FR-R1 delegates completely; the -18 hours are NOT stated in FR-R1.",
    "bright_line", "clear",
    "A model asked for -18 hours must follow this pointer. Answering by analogy with -16 ('later than 22:30') is wrong.",
    "no", "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "soumise au respect de la recommandation n° 2004-7", "FR", "high")

add("FR-PRO-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "human_dignity", "prohibited",
    "Programmes which OFFEND HUMAN DIGNITY - in particular those depicting SEXUAL VIOLENCE, PERVERSIONS OR DEGRADATION - are banned from broadcast.",
    "No permitted time.", "prohibited",
    "None. No category, service type, hour or technical measure unlocks this.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "attentatoires à la dignité de la personne humaine", "FR", "high")

add("FR-PRO-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "prohibited",
    "PORNOGRAPHIC programmes DEPICTING UNDER-18s are banned from broadcast.",
    "No permitted time.", "prohibited", "None.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "pornographique mettant en scène des personnes mineures", "FR", "high")

add("FR-PRO-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "prohibited",
    "Programmes of EXTREME OR GRATUITOUS VIOLENCE are banned from broadcast.",
    "No permitted time.", "prohibited",
    "None. Distinguish from category V 'very great violence', which IS broadcastable within 00:00-05:00 on eligible services.",
    "bright_line", "clear",
    "The boundary between 'very great violence' (cat. V, schedulable) and 'extreme or gratuitous violence' (banned) is a genuine judgment line and a likely source of disagreement. Flag near-threshold cases.",
    "yes", "FR-R1c", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "violence ou de violence gratuite", "FR", "high")

add("FR-SIG-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "The PICTOGRAM must remain on screen FOR THE WHOLE DURATION of the programme (categories II-V under the 2014 text).",
    "n/a - display obligation", "n/a",
    "Under the original 2005 text category II was 5 minutes at the start; 2012-57 and 2014-17 changed this.",
    "bright_line", "clear",
    "Signage is a SEPARATE obligation from scheduling: a programme can be correctly scheduled and still breach by failing to display the pictogram. The C8 enforcement decision was precisely about signage.",
    "no", "FR-R1c", "art. 4", U_FR2, "2014-04-09", "open", "approved",
    "présent à l'écran pendant toute la durée de la diffusion", "FR", "high")

add("FR-SIG-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "A WRITTEN MENTION must also appear, either at the bottom of the screen in white for AT LEAST 1 MINUTE at the start, OR full-screen before the programme for AT LEAST 12 SECONDS. Wording: II 'deconseille aux moins de dix ans'; III 'aux moins de douze ans'; IV 'aux moins de seize ans'; V 'aux moins de dix-huit ans' (or the assigned cinema-ban wording).",
    "n/a - display obligation", "n/a",
    "Decret n. 90-174 on prior public warnings continues to apply.",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 4", U_FR2, "2012-11-20", "open", "approved",
    "en bas d'écran, en blanc, au minimum pendant une minute", "FR", "high")

add("FR-SIG-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "The classification must be made known to the public AT THE TIME OF BROADCAST, in TRAILERS, and in PROGRAMME SCHEDULES communicated to the press.",
    "n/a - information obligation", "n/a", "",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 4", U_FR2, "2014-04-09", "open", "approved",
    "portée à la connaissance du public au moment de la diffusion", "FR", "high")

add("FR-TRL-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "II_to_V",
    "Trailers must display the PICTOGRAM OF THE PROGRAMME'S CATEGORY THROUGHOUT the trailer, and must NOT contain scenes likely to offend young viewers.",
    "n/a - content and display obligation", "n/a", "",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "apparaît pendant toute la durée de la bande-annonce", "FR", "high")

add("FR-TRL-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "III_-12",
    "Category III (-12) trailers MAY NOT AIR CLOSE TO CHILDREN'S PROGRAMMES. Category II trailers near children's programmes require particular care.",
    "Placement restriction.", "not_near=children_programmes", "",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "ne peuvent être diffusées à proximité des émissions pour enfants", "FR", "high")

add("FR-TRL-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "IV_-16",
    "Category IV (-16) trailers MAY NOT AIR BEFORE 20:30.",
    "Not before 20:30.", "not_before=20:30",
    "Note the trailer time (20:30) differs from the programme time on non-cinema channels (22:30).",
    "bright_line", "clear", "", "no",
    "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "catégorie IV ne peuvent être diffusées avant 20 h 30", "FR", "high")

add("FR-MUS-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "exempt",
    "Music videos (videomusiques) are EXEMPT FROM SYSTEMATIC SIGNAGE.",
    "n/a", "exempt=systematic_signage",
    "A deliberate special regime, not an oversight.",
    "bright_line", "clear",
    "Contrast with the UK, which applies the ordinary watershed plus detailed content thresholds to music videos. The SAME music video can yield a hard UK verdict and a soft French one.",
    "no", "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "exonérées du caractère systématique de la signalétique", "FR", "high")

add("FR-MUS-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "soft_restriction",
    "Music videos likely to offend young viewers SHOULD PREFERABLY be broadcast AFTER 22:00.",
    "Soft preference for after 22:00 - NOT an absolute prohibition.",
    "soft_prefer_not_before=22:00",
    "The wording is a preference ('de preference'), not a prohibition. Do not output this as a hard limit.",
    "judgment_based", "clear",
    "A key precision test: a model that renders this as 'prohibited before 22:00' is OVER-rating and misstating the legal force of the rule. Worth an explicit test case.",
    "yes", "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "l'éditeur s'attache à les diffuser après 22 heures", "FR", "high")

add("FR-MUS-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "context_dependent",
    "Programmes containing music videos whose THEMES ARE NOT AIMED AT CHILDREN OR TEENAGERS should nonetheless carry a WARNING.",
    "n/a - information duty", "n/a;requires=warning", "",
    "judgment_based", "clear", "", "no",
    "FR-R1c", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "selon des thématiques qui ne s'adressent ni aux enfants", "FR", "high")

add("FR-CV-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; high_production_commitment_channels; pay_per_view",
    "classification_scheme", "V_-18",
    "ELIGIBILITY GATE: only services with special access conditions may broadcast category V - 'cinema' channels, services with a high production-contribution commitment equivalent to cinema channels, or pay-per-view services - and only where access is limited so that under-18s cannot reach the content. Requests are EXAMINED INDIVIDUALLY by the regulator.",
    "Eligibility precondition, not a time rule.", "gate=service_eligibility",
    "On all other channels category V is TOTALLY PROHIBITED (see FR-CV-003).",
    "conditional", "clear", "VERIFIED against the primary text 2026-11-06. Quotes are from Arcom's own ENGLISH translation, which warns that only the original French is authentic - a French-qualified reviewer should re-check them against it.", "yes",
    "FR-R2", "notice of 15 Dec 2004, I.A", U_FRV, "2004-12-15", "open", "approved",
    "subject to special access conditions", "EN", "high")

add("FR-CV-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; high_production_commitment_channels; pay_per_view",
    "scheduling_general", "V_-18",
    "Category V (-18) programmes may be broadcast only BETWEEN 00:00 (MIDNIGHT) AND 05:00.",
    "Closed window 00:00-05:00.", "window=00:00-05:00",
    "Conditional on the FR-CV-001 eligibility gate being satisfied first, plus locking (FR-CV-004) and signage.",
    "bright_line", "clear",
    C03 + " Corroborated by the Arcom public summary page ('between midnight and 5 a.m.'), which raises confidence in the figure even though the source text's currency is unconfirmed.",
    "yes", "FR-R2", "notice of 15 Dec 2004, I.B", U_FRV, "2004-12-15", "open", "approved",
    "can only be shown between midnight and 5am", "EN", "high")

add("FR-CV-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "V_-18",
    "On services that are NOT eligible under FR-CV-001, category V programmes are subject to a TOTAL PROHIBITION ON BROADCAST.",
    "No permitted time on non-eligible services.", "prohibited",
    "None.",
    "bright_line", "clear", "SECONDARY-SOURCED INFERENCE. The proof quote comes from a government summary page, not the primary instrument. The primary says only that the regulator 'only authorizes' eligible services; a total ban elsewhere follows reasonably from that but remains an INFERENCE. A French regulatory lawyer should confirm it before this row is used to refuse a broadcast.", "yes",
    "FR-R2 + FR-S2", "2004-7 I.A", U_FRV, "2004-12-15", "open", "approved",
    "Sauf sur les chaines autorisees, ces programmes font l'objet d'une interdiction totale de diffusion.",
    "FR", "medium")

add("FR-CV-004", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "access_control", "V_-18",
    "DIGITAL LOCKING: category V must be locked at the DECODER level requiring a personal code, with an on-screen lock message. The lock must reactivate when the broadcast context changes and stay synchronised with the programme. The code must be at least FOUR DIGITS, not 0000, hidden when entered, used only for this purpose, and IMPOSSIBLE FOR SUBSCRIBERS TO DISABLE.",
    "n/a - access-control obligation", "requires=decoder_lock",
    "Analogue services: from 1 Jan 2006 received WITHOUT access unless the subscriber opts in in writing.",
    "bright_line", "clear", "VERIFIED against the primary text 2026-11-06. Quotes are from Arcom's own ENGLISH translation, which warns that only the original French is authentic - a French-qualified reviewer should re-check them against it.", "yes",
    "FR-R2", "notice of 15 Dec 2004, II.B.1", U_FRV, "2004-12-15", "open", "approved",
    "This program is locked because it is harmful to persons under 18", "EN", "high")

add("FR-CV-005", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "pay_tv_bundles", "commercial_conditions", "V_-18",
    "QUANTITY LIMITS: the regulator caps the number of category V broadcasts in each service's CONVENTION. Separately, if a non-pay-per-view bundle includes services showing MORE THAN 208 category V programmes per year (about 4 per week), the offer must also be available WITHOUT those services, on terms that do not favour the bundle.",
    "n/a - bundle composition rule", "n/a",
    "A channel/distributor-level obligation.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Not answerable from a single asset description. Must not be attempted by a per-asset prompt. " + C03,
    "yes", "FR-R2", "notice of 15 Dec 2004, I.D", U_FRV, "2004-12-15", "open", "approved",
    "more than 208 category V programs per year", "EN", "high")

add("FR-CV-006", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "pay_tv_bundles", "commercial_conditions", "V_-18",
    "MARKETING CONDITIONS: category V content may not be included in promotional offers aimed at people without a qualifying subscription; pay-per-view category V may only be sold INDIVIDUALLY; opt-in offers may not be priced more favourably than versions without category V content.",
    "n/a - commercial rule", "n/a", "Distributor-level.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Recorded for completeness only. " + C03, "yes",
    "FR-R2", "notice of 15 Dec 2004, I.C and I.D", U_FRV, "2004-12-15", "open", "approved",
    "may only be sold individually", "EN", "high")

add("FR-CV-007", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "signage", "V_-18",
    "Broadcasts of category V must display the -18 rating AND a WARNING about harm to minors and the legal sanctions under ARTICLE 227-22 of the French Penal Code. Distributors/publishers must regularly remind subscribers how the lock works; contracts must include this information; annual implementation reports go to the regulator.",
    "n/a - display and information obligation", "requires=on_screen_warning",
    "The penal-code warning is specific to category V.",
    "bright_line", "clear", "VERIFIED against the primary text 2026-11-06. Quotes are from Arcom's own ENGLISH translation, which warns that only the original French is authentic - a French-qualified reviewer should re-check them against it.", "yes",
    "FR-R2", "notice of 15 Dec 2004, III.A", U_FRV, "2004-12-15", "open", "approved",
    "article 227-22 of the French penal code", "EN", "high")

add("FR-CNV-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "per_channel", "channel_override", "n/a",
    "CHANNEL CONVENTIONS: every conventionnee channel signs an individual convention with Arcom containing its own protection-of-minors articles, which CAN BE STRICTER than the general recommendation. Enforcement cites the convention alongside the recommendation (e.g. the C8 decision cites convention arts. 2-3-7, 2-4, 4-2-1 with reco. 2005-5 arts. 2 and 4).",
    "Channel-specific; may tighten any rule above.", "override=channel_specific",
    "Parliamentary material notes conventions have LOWERED the category III limit to 22:00 'or less, with permanent signage' for particular channels.",
    "conditional", "out_of_scope_for_asset_decision",
    "PROMOTED from draft 2026-11-07. What is now PROVEN from a stored source (FR-V1): a convention is an individual binding agreement between the regulator and the channel, breach of it is a manquement in its own right, and the regulator derives its enforcement power from the convention alongside the statute. What remains UNCOLLECTED is the CONTENT of any individual convention, so this row tells a decision that an extra layer of binding obligation exists for a French channel and that it must be checked, not what it says. C-06 stays open for that. | There is no consolidated document containing all applicable French rules for a given broadcast: the set is statute + reco. 2005-5 as amended + (for -18) reco. 2004-7 + THAT CHANNEL'S convention. For Task 2 this is a per-licensee data source that cannot be scraped generically and needs a local expert.",
    "yes", "FR-V1", "per-channel convention", U_CONV, "", "open", "approved",
    "aux stipulations précitées de l'article 2-3-7 de sa convention", "FR", "low")

# ================================================================ EU
add("EU-FRM-001", "EU", "EU / ERGA", "statute", 1, "framework_only",
    "all_avms", "legal_basis", "n/a",
    "Member States must ensure that audiovisual media services which MAY IMPAIR the physical, mental or moral development of minors are only made available in such a way that MINORS WILL NOT NORMALLY HEAR OR SEE THEM. Measures may include selecting the TIME OF BROADCAST, AGE VERIFICATION TOOLS, or OTHER TECHNICAL MEASURES, and must be PROPORTIONATE to the potential harm. The most harmful content, such as gratuitous violence and pornography, is subject to the strictest measures.",
    "Not itself a time rule - mandates an outcome and permits alternative means.",
    "framework:outcome_duty",
    "NOT directly applicable to a broadcast; binds Member States, who implement nationally. UK retained equivalent duties via SI 2020/1062.",
    "bright_line", "clear",
    "ROOT CAUSE of the 'rating does not equal hours' problem: the directive mandates the outcome and lists time, age verification and other technical measures as ALTERNATIVES. Two Member States can lawfully reach the same outcome with completely different instruments - France chose graded descriptors plus fixed hours; the UK chose a single watershed plus contextual judgement plus PIN. Never cite as the operative rule for a decision.",
    "no", "EU-D1", "AVMSD art. 6a(1)", U_EU, "2018-12-18", "open", "approved",
    "The most harmful content, such as gratuitous violence and pornography, shall be subject to the strictest measures.",
    "EN", "high")

add("EU-FRM-002", "EU", "EU / ERGA", "statute", 1, "framework_only",
    "all_avms", "signage", "n/a",
    "Member States must ensure providers give viewers SUFFICIENT INFORMATION about content which may impair minors' development, using A SYSTEM DESCRIBING THE POTENTIALLY HARMFUL NATURE of the content. Co-regulation is encouraged.",
    "n/a - descriptor obligation", "n/a",
    "Separate from and additional to the access/time measures in art. 6a(1).",
    "bright_line", "clear",
    "Independent corroboration for carrying a fixed content_category dimension separate from the age level: the regulators themselves concluded an age number alone is insufficient. EU notification material for the French 2021 decree states content indicators/descriptors (violence, sex, distress, etc.) were needed because the existing programme symbol gave no indication of the TYPE of harmful content.",
    "no", "EU-D1", "AVMSD art. 6a(3)", U_EU, "2018-12-18", "open", "approved",
    "provide sufficient information to viewers about content", "EN", "high")

add("EU-FRM-003", "EU", "EU / ERGA", "statute", 1, "no_out_of_scope",
    "all_avms", "data_protection", "n/a",
    "Personal data of minors collected or generated pursuant to art. 6a(1) must not be processed for commercial purposes such as direct marketing, profiling or behaviourally targeted advertising.",
    "n/a", "n/a", "",
    "bright_line", "out_of_scope_for_asset_decision",
    "Not a content or scheduling rule. Recorded so the scope boundary is explicit.", "no",
    "EU-D1", "AVMSD art. 6a(2)", U_EU, "2018-12-18", "open", "approved",
    "shall not be processed for commercial purposes", "EN", "high")

# ============================================================ WORKBOOK
wb = openpyxl.Workbook()

HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(bold=True, color="FFFFFF", size=10)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

STATUS_FILL = {
    "approved": PatternFill("solid", fgColor="E2EFDA"),
    "draft": PatternFill("solid", fgColor="FFF2CC"),
    "unverified": PatternFill("solid", fgColor="FCE4D6"),
    "superseded": PatternFill("solid", fgColor="D9D9D9"),
}
FLAG_FILL = {
    "clear": PatternFill("solid", fgColor="E2EFDA"),
    "conflicting_sources": PatternFill("solid", fgColor="F8CBAD"),
    "translation_uncertain": PatternFill("solid", fgColor="FFF2CC"),
    "unverified": PatternFill("solid", fgColor="FCE4D6"),
    "out_of_scope_for_asset_decision": PatternFill("solid", fgColor="D9E1F2"),
}

# ---- Rules tab
ws = wb.active
ws.title = "Rules"
names = [c[0] for c in COLS]
ws.append(names)
for i, (n, w) in enumerate(COLS, start=1):
    c = ws.cell(row=1, column=i)
    c.fill = HDR_FILL
    c.font = HDR_FONT
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 30

i_status = names.index("status") + 1
i_flag = names.index("ambiguity_flag") + 1
i_det = names.index("determinacy") + 1
i_hrr = names.index("human_review_required") + 1
i_url = names.index("source_url") + 1

for row in R:
    ws.append(row)

for r in range(2, ws.max_row + 1):
    for c in range(1, len(COLS) + 1):
        cell = ws.cell(row=r, column=c)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = BORDER
        cell.font = Font(size=9)
    sv = ws.cell(row=r, column=i_status).value
    if sv in STATUS_FILL:
        ws.cell(row=r, column=i_status).fill = STATUS_FILL[sv]
    fv = ws.cell(row=r, column=i_flag).value
    if fv in FLAG_FILL:
        ws.cell(row=r, column=i_flag).fill = FLAG_FILL[fv]
    if ws.cell(row=r, column=i_hrr).value == "yes":
        ws.cell(row=r, column=i_hrr).fill = PatternFill("solid", fgColor="FFF2CC")
    u = ws.cell(row=r, column=i_url).value
    if u:
        ws.cell(row=r, column=i_url).hyperlink = u
        ws.cell(row=r, column=i_url).font = Font(size=9, color="0563C1", underline="single")

ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{ws.max_row}"

dv = DataValidation(type="list",
                    formula1='"bright_line,conditional,judgment_based"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"{get_column_letter(i_det)}2:{get_column_letter(i_det)}400")

dv2 = DataValidation(
    type="list",
    formula1='"clear,conflicting_sources,translation_uncertain,unverified,out_of_scope_for_asset_decision"',
    allow_blank=True)
ws.add_data_validation(dv2)
dv2.add(f"{get_column_letter(i_flag)}2:{get_column_letter(i_flag)}400")

dv3 = DataValidation(type="list",
                     formula1='"approved,draft,unverified,superseded"', allow_blank=True)
ws.add_data_validation(dv3)
dv3.add(f"{get_column_letter(i_status)}2:{get_column_letter(i_status)}400")


def sheet(title, rows, widths, head_height=28):
    s = wb.create_sheet(title)
    for row in rows:
        s.append(row)
    for i, w in enumerate(widths, start=1):
        s.column_dimensions[get_column_letter(i)].width = w
    for i in range(1, len(widths) + 1):
        c = s.cell(row=1, column=i)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = Alignment(vertical="center", wrap_text=True)
    s.row_dimensions[1].height = head_height
    for r in range(2, s.max_row + 1):
        for c in range(1, len(widths) + 1):
            cell = s.cell(row=r, column=c)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.font = Font(size=9)
    s.freeze_panes = "A2"
    return s


# ---- Legend tab
legend = [["column", "what it holds", "allowed values / notes"]]
legend += [
    ["rule_id", "Stable identifier. Format: (UK|FR|EU)-[A-Z]{2,4}-nnn.", "Cite this in prompt output so every decision is traceable to a row. Mnemonics: SCH scheduling, VIO violence, SEX sexual content, NUD nudity, LNG language, DRG drugs, IMI imitable behaviour, SUI suicide/self-harm, FLM film carry-over, MUS music videos, TRL trailers, SIG signage, CLS classification scheme, CV category V regime, PRO absolute prohibition, GEN general duty, DEF definition, LAW legal basis, SVC service scope, CNV channel convention, OCC occult, WEL participant welfare, OFF offence, FRM framework, ACC access control, HAT hatred and abuse, REL religion, CTX context, WRN warnings, PRE enforcement precedent."],
    ["country", "Jurisdiction.", "UK / FR / EU"],
    ["regulator", "Body that issued the text.", "Ofcom / Arcom / Parliament / EU-ERGA"],
    ["source_type", "Nature of the source.", "statute / regulator_binding / regulator_guidance / precedent / regulator_summary / classification_body / secondary"],
    ["authority_rank", "Conflict resolution. LOWER WINS.", "1 statute, 2 regulator_binding, 3 guidance, 4 precedent, 5 regulator_summary, 6 classification_body, 7 secondary"],
    ["use_for_decision", "Whether a per-asset decision may rely on this row.", "yes / definition_only / framework_only / pointer / scope_rule / no_out_of_scope"],
    ["service_type", "Which services the rule binds. SEMICOLON-SEPARATED.", "CONTROLLED VOCABULARY, enforced by verify_rules.py: an unknown value now fails the build. free_to_air, cinema_channels, pay_per_view, premium_subscription_film, scheduled_channels_with_mdp, other_than_cinema_channels, music_channels, high_production_commitment_channels, bbc_odps, all_linear_tv, per_channel, pay_tv_bundles, all_avms. The check exists because two spellings of one service once silently dropped a rule from every decision slice using the other."],
    ["content_category", "Shared harm vocabulary across countries. THIS IS THE JOIN KEY to the content-extraction stage.", "violence, sexual_content, nudity, drugs_alcohol_smoking, strong_language, fear_distress, suicide_self_harm, imitable_behaviour, human_dignity, occult_paranormal, religion, music_videos, trailers, film_carryover, signage, access_control, scheduling_general, classification_scheme, serious_harm, offence_general, participant_welfare, commercial_conditions, data_protection, legal_basis, definition, scope" + " NOTE: this is a RETRIEVAL KEY, not a description of the rule. A ban on pornography depicting minors and a sex scene in a drama both carry sexual_content; read threshold_description to see what a rule actually covers. Coarse categories cause over-retrieval, which is safe, where under-retrieval is not."],
    ["classification", "The age label or UK equivalent.", "FR: I_tous_publics, II_-10, III_-12, IV_-16, V_-18. UK: context_dependent, watershed_bound, prohibited, any_time_with_protection, restricted_window. Also: category_independent, exempt, soft_restriction, n/a"],
    ["threshold_description", "What the rule actually says, in structured prose.", "Free text. Capitals mark the operative words."],
    ["time_restriction_text", "The time effect in words.", "Free text."],
    ["time_rule_machine", "The time effect in a parseable form, for code. Semicolon-separated tokens.", "none | prohibited | any_time | n/a | not_before=HH:MM | window=HH:MM-HH:MM | restricted_window=HH:MM-HH:MM | soft_prefer_not_before=HH:MM | not_within=... | not_near=... | not_when=... | prohibited_in=... | days=... | except_days=... | unless=... | requires=... | gate=... | override=... | annual_quota=... | sub_quota=... | standard=... | frequency_cap=... | exempt=... | see=RULE_ID | judgment:... | framework:..."],
    ["exceptions_conditions", "Carve-outs, gates and inputs the rule depends on.", "Free text."],
    ["determinacy", "PROPERTY OF THE RULE. Governs how the test set is scored.", "bright_line = one correct answer, exact match required. conditional = bright line gated on an input; a correct missing-information request also passes. judgment_based = evaluative; score the reasoning and cited rule, accept a band, require escalation near thresholds."],
    ["ambiguity_flag", "PROPERTY OF OUR EXTRACTION. Do NOT merge with determinacy.", "clear / conflicting_sources / translation_uncertain / unverified / out_of_scope_for_asset_decision"],
    ["ambiguity_note", "What is uncertain and how it was resolved.", "Free text. Carries the C-0n conflict IDs."],
    ["human_review_required", "Escalate before relying on this row.", "yes / no"],
    ["source_doc", "Source ID from the Sources tab.", "e.g. UK-S1, FR-R1, EU-D1"],
    ["clause_ref", "Clause within the source.", "e.g. Rule 1.4, art. 3, AVMSD art. 6a(1)"],
    ["source_url", "Canonical URL (hyperlinked).", "PREFER A STABLE HTML PAGE over a PDF where the publisher offers one: an HTML page keeps its address across revisions, whereas PDF URLs are minted per revision (Ofcom /siteassets/ PDFs carry a ?v=NNNNNN parameter), so a pinned PDF link rots silently at the next update. For a row stating CURRENT law this is the CURRENT CONSOLIDATED text. The JORF/original-publication URL is cited only on superseded rows (9xx), where it is the correct source. Citing an original for current law is a provenance bug: it reads as authoritative while silently omitting later amendments."],
    ["valid_from", "Date the provision took effect.", "ISO date, or blank if undated guidance"],
    ["valid_to", "End of validity.", "open / unknown / ISO date"],
    ["status", "Fitness as ground truth.", "approved = usable. draft = do not use until the conflict is resolved. unverified = currency unconfirmed. superseded = historical. NOTE: the manifest carries only CURRENT materials, so a superseded rule row would have no retrievable source; superseded wordings are recorded in the Open_Questions entry for the conflict that found them. A rule_id in the 9xx range is reserved for a historical version if one is ever carried again."],
    ["verbatim_quote", "Short quoted fragment that survived retrieval.", "INCOMPLETE - see 99_EXTRACTION_NOTES. Cannot yet support an automated quote-integrity check because no local copy of the source exists."],
    ["quote_lang", "Language of the quote.", "EN / FR"],
    ["extraction_confidence", "Confidence in this extraction.", "high / medium / low"],
    ["last_checked", "Date this row was last checked.", "ISO date"],
]
sheet("Legend", legend, [24, 46, 92], 24)

# ---- How to use tab
howto = [["topic", "guidance"]]
howto += [
    ["Purpose", "Ground truth for testing a prompt that outputs an age rating / classification and broadcast-time restrictions for UK and France, for LINEAR TELEVISION. On-demand and streaming are a different regime and are out of scope."],
    ["Shape", "LONG format: one row per rule. The wide, per-category view is on the Pivot_Readable tab and is derived from these rows - edit here, not there."],
    ["The join key", "content_category is the shared vocabulary. The content-extraction stage tags a scene with a content_category and the rule stage looks up rows with that category plus the relevant country and service_type. Keep the vocabulary closed; map each regulator's wording onto it rather than inventing new values."],
    ["Resolving conflicts", "Sort by authority_rank ascending; the lowest rank wins. Record the resolution in ambiguity_note. Worked example: C-01, where Arcom's own public summary page contradicted its binding text on the -12 hours and the binding text won."],
    ["Two kinds of ambiguity", "determinacy describes THE RULE (is it a bright line or a judgment call?). ambiguity_flag describes OUR EXTRACTION (are we sure we read it right?). They are independent: a bright_line rule can be translation_uncertain, and a judgment_based rule can be perfectly clear. Merging them makes the test set unscoreable."],
    ["Scoring by determinacy", "bright_line: exact match; any deviation is a defect. conditional: the correct answer, OR a correct missing-information request when the gating input was absent - both pass. judgment_based: score the cited rule and the reasoning, accept a band of outcomes, and require escalation near a threshold. Scoring a judgment_based row by exact match measures the test set, not the model."],
    ["Before using as ground truth", "Filter status = approved. All 103 rows are approved, and all 103 carry a verbatim quote that verifies character-for-character against the stored source, 0 failing. Coverage is a ratchet: an approved row with no quote fails the build (C-15). APPROVED STILL DOES NOT MEAN SAFE TO AUTOMATE - 38 rows are judgment_based and must route to a human (see Scoring by determinacy), and 42 rows are flagged needs_review for other reasons. Separately, C-08 remains open: this table and the prompt share an author, so the bright-line rows want independent re-derivation before anyone treats them as ground truth."],
    ["Avoiding correlated error", "The biggest risk is that this table and the prompt share an author and therefore share mistakes - the exact failure Task 2 asks about. Mitigation: the bright-line rows (times, absolute prohibitions) should be INDEPENDENTLY RE-DERIVED from primary sources by a second pass that has not seen this table, then compared. verbatim_quote and source_url let a reviewer check a row without reading the prompt at all."],
    ["Source form", "Prefer the publisher's stable HTML page to a PDF wherever one exists. An HTML page keeps its URL across revisions and shows the current text, so the citation stays good; a PDF URL is minted per revision and rots silently. Where a document is genuinely PDF-only - Ofcom guidance notes, statements, enforcement decisions - the manifest records a landing_page: the stable HTML page the current PDF is always reachable from, so a dead PDF link is recoverable rather than a dead end."],
    ["Versioning", "Never delete a row. When a source is replaced, set valid_to and status = superseded on the old row and add a new row. That preserves the ability to say which rule version produced a past decision."],
    ["Required inputs the rules imply", "country; service_type (free-to-air vs cinema channel vs pay-per-view vs premium subscription film); access measures in place (none / mandatory_daytime_protection / mandatory_restricted_access / decoder_lock); intended broadcast DATE and time (France has day-of-week and school-holiday rules); whether the asset is a theatrical film and its existing BBFC/CNC classification; whether it is a trailer or a music video. If any of these is missing and a candidate rule depends on it, the correct output is a missing-information flag, NOT an assumption."],
    ["Known hard pre-checks", "Absolute prohibitions should be enforced in CODE, not left to prompt reasoning: UK-GEN-001 (seriously impair), UK-SEX-001 (R18-equivalent), UK-FLM-001 (refused classification), UK-FLM-006 (R18 films), FR-LAW-001 (nuire gravement), FR-PRO-001/002/003 (human dignity, child pornography, extreme violence). No contextual argument or access measure should be able to override these."],
    ["What is NOT in v1", "French channel conventions, which can be stricter than the general law (C-06). Systematic enforcement precedent: ONE decided case is collected against 35 judgment_based rules, so thresholds are largely uncalibrated (C-07); the guidance names about a dozen further decisions and collecting those bulletins is the highest-value work left. BBFC classification guidelines. Overseas France. Also deliberately absent: everything outside the age/time decision - impartiality, fairness, privacy, commercial references - a scope choice recorded in SCOPE.md. The Ofcom Guidance Notes for Sections One and Two ARE now collected and mined; they supplied 9 rules the Code text alone does not yield. See 99_EXTRACTION_NOTES_AND_LIMITS."],
]
sheet("How_to_use", howto, [30, 130], 22)

# ---- Sources tab
src = [["source_id", "document", "regulator", "source_type", "authority_rank",
        "scope / applicability", "url", "date / version", "notes"]]
src += [
    ["UK-S1", "Ofcom Broadcasting Code, Section One: Protecting the Under-Eighteens", "Ofcom", "regulator_binding", 2,
     "All Ofcom-licensed TV and radio. Rules 1.3-1.6 do NOT apply to BBC ODPS.", U_S1,
     "HTML, last updated 2023-03-16", "The core UK rulebook. Must be read with Section Two. USE THE HTML: the downloadable PDFs are the January 2019 print edition (every page footer says so) and predate this text by four years."],
    ["UK-S2", "Ofcom Broadcasting Code, Section Two: Harm and Offence", "Ofcom", "regulator_binding", 2,
     "Same as UK-S1.", U_S2, "HTML, last updated 2024-02-19 (the PDF edition is January 2019)",
     "Supplies the BINDING DEFINITION OF 'CONTEXT', on which Section One depends. Time of broadcast is one of its eight factors."],
    ["UK-S0", "Ofcom Broadcasting Code - FULL PDF (all ten sections + Cross-promotion Code + ODPS rules)",
     "Ofcom", "regulator_binding", 2,
     "Everything in one file. Covers all programmes broadcast on or after 23:00 on 2020-12-31.",
     "https://www.ofcom.org.uk/siteassets/resources/documents/tv-radio-and-on-demand/broadcast-codes/code---jan-2019/broadcast-code-full.pdf?v=323671", "January 2019 - SUPERSEDED",
     "NOT CURRENT. The last consolidated PRINT edition. Ofcom's 31 Dec 2020 statement confirms the Code 'is now published on the Ofcom website and is no longer available in print', so no consolidated PDF has been maintained since. The Code in force covers programmes from 23:00 on 2020-12-31 and Sections One and Two were revised again in 2023 and 2024. Use ONLY to diff what changed since 2019; the per-section HTML is authoritative."],
    ["UK-S4", "Ofcom Broadcasting Code, Section Four: Religion", "Ofcom", "regulator_binding", 2,
     "In scope for Rule 4.7 only.", "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-four-religion", "HTML, current",
     "Rule 4.7 bars claims of special powers when significant numbers of children may be watching - a child-audience restriction outside Section One. Rest of Section Four out of scope."],
    ["UK-G1", "Ofcom Guidance: Protecting the Under-Eighteens - Observing the watershed on television and music videos",
     "Ofcom", "regulator_guidance", 3, "Television.", U_G1, "undated issue",
     "The ONLY UK source with operational detail on MUSIC VIDEOS and on the post-watershed ramp."],
    ["UK-G2", "Ofcom Guidance Notes, Section One", "Ofcom", "regulator_guidance", 3, "Interpretation aid for S1.",
     "https://www.ofcom.org.uk/__data/assets/pdf_file/0017/24704/section1.pdf", "Issue Six, 2015-03-30",
     "IDENTIFIED BUT NOT EXTRACTED in v1. Would sharpen the judgment_based thresholds."],
    ["UK-G3", "Ofcom Guidance Notes, Section Two", "Ofcom", "regulator_guidance", 3, "Interpretation aid for S2.",
     "https://www.ofcom.org.uk/__data/assets/pdf_file/0023/104657/Section-2-Guidance-Notes.pdf", "Issue Twelve, 2017-07-18",
     "IDENTIFIED BUT NOT EXTRACTED in v1."],
    ["UK-M1", "Ofcom Statement: Review of the mandatory daytime protection rules", "Ofcom", "regulator_binding", 2,
     "Premium subscription film, pay-per-view, and from 2019-01-01 scheduled channels on vertically integrated pay-TV platforms. NOT free-to-air DTT.",
     U_M1, "Published 2018-11-05, effective 2019-01-01",
     "Created the MDP regime and amended Rules 1.23-1.25. The clearest UK proof that rating does not determine hours."],
    ["UK-P1", "Ofcom Broadcast and On Demand Bulletins (enforcement decisions)", "Ofcom", "precedent", 4,
     "Applied thresholds.",
     "https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf",
     "ongoing",
     "Example: Toofan, NTV, 2026-05-29 11:30 - violent film not appropriately scheduled, breach of Rule 1.3. The only source of APPLIED thresholds for judgment_based rules; should be ingested systematically."],
    ["UK-L1", "Communications Act 2003, ss. 3(4)(h), 319(2)(a) & (f)", "UK Parliament", "statute", 1,
     "Legal basis for Ofcom's standards duty.", U_L1, "2003",
     "s.319(2)(a): 'that persons under the age of eighteen are protected'."],
    ["UK-L2", "The Audiovisual Media Services Regulations 2020 (SI 2020/1062)", "UK Parliament", "statute", 1,
     "Implemented revised AVMSD duties into UK law post-Brexit.",
     "https://www.legislation.gov.uk/uksi/2020/1062/note/made", "2020",
     "Confirms content standards for broadcast TV remain in the Ofcom Code."],
    ["UK-C1", "BBFC classification", "BBFC", "classification_body", 6,
     "Film classification. NOT a TV regulator.", "https://www.bbfc.co.uk", "ongoing",
     "In scope only as an INPUT: the Ofcom Code refers to BBFC ratings in Rules 1.17, 1.22, 1.23, 1.24, 1.25, 1.26."],
    ["FR-R1", "Recommandation n. 2005-5 du 7 juin 2005 (signaletique jeunesse et classification des programmes), as amended",
     "Arcom (ex-CSA)", "regulator_binding", 2,
     "Editors of linear TV services in France; all conventionnees et declarees channels.", U_FR1C,
     "JORF n.158, 2005-07-08, text n.92; amended 2012 and 2014",
     "THE CORE FRENCH FRAMEWORK. Art. 2 defines categories I-V; art. 3 sets programming conditions."],
    ["FR-A1", "Deliberation n. 2012-57 du 23 octobre 2012 modifying FR-R1", "Arcom (ex-CSA)", "regulator_binding", 2,
     "Amended art. 4(2)(a) - category II on-screen signage.",
     "https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/deliberation-du-23-octobre-2012-modifiant-la-recommandation-ndeg-2005-5-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des-programmes",
     "JORF 2012-11-20", ""],
    ["FR-A2", "Deliberation n. 2014-17 du 5 mars 2014 modifying FR-R1", "Arcom (ex-CSA)", "regulator_binding", 2,
     "Replaced arts. 1, 3, 4; amended art. 2; inserted a new art. 5 (trailers and music videos).", U_FR2,
     "JORF 2014-04-09", "THE CURRENT OPERATIVE TEXT for French scheduling. The Arcom ENGLISH page is a DeepL machine translation and is garbled at art. 3 - that was conflict C-02, now closed against the French text (FR-A2b / FR-R1c / FR-R1d). It also replaced the fifth alinea of art. 2, broadening the cat. III definition - see C-09. Always read the French."],
    ["FR-R2", "Recommandation n. 2004-7 du 15 decembre 2004 - category V programmes", "Arcom (ex-CSA)", "regulator_binding", 2,
     "Editors AND distributors broadcasting category V (-18), mainland France and overseas departements.", U_FRV,
     "JORF 2004-12-23",
     "THE SOLE SOURCE of the French -18 hours (00:00-05:00). Art. 3 of FR-R1 defers to it entirely. Upheld by Conseil d'Etat 2006-05-17, nos. 263081/277711. CURRENCY UNCONFIRMED (C-03)."],
    ["FR-R3", "Recommandation du 26 juillet 2005 - category V, overseas France", "Arcom (ex-CSA)", "regulator_binding", 2,
     "Overseas departements.",
     "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/notice-july-26-2005-television-service-editors-and-distributors-showing-category-v-programs-overseas-france",
     "2005-07-26", "Noted, NOT extracted in v1."],
    ["FR-S1", "Arcom youth-signage public awareness page", "Arcom", "regulator_summary", 5,
     "Plain-language per-category meanings and broadcast times.",
     "https://www.arcom.fr/en/news/images-always-have-impact-arcom-launches-its-new-youth-signage-awareness-raising-campaign",
     "current",
     "UNRELIABLE for -12: describes it with the same wording as -10 ('during the day, under certain conditions'), contradicting the binding text (C-01). Useful corroboration for -16 ('as of 10:30 pm') and -18 ('between midnight and 5 a.m.')."],
    ["FR-L1", "Loi n. 86-1067 du 30 septembre 1986, arts. 1 and 15", "French Parliament", "statute", 1,
     "All French audiovisual communication services.", U_FRL, "1986-09-30, as amended",
     "Art. 15 is the statutory duty and establishes the TWO-TIER HARM STANDARD: 'nuire gravement' = absolute prohibition; 'nuire' = permitted if broadcast time and/or technical means keep minors away."],
    ["FR-V1", "Channel conventions (per-channel agreements with Arcom)", "Arcom", "regulator_binding", 2,
     "CHANNEL-SPECIFIC. Can be stricter than the general recommendation.", U_CONV,
     "per channel, various",
     "NOT COLLECTED in v1 (C-06). Example: the C8 mise en demeure cites convention arts. 2-3-7, 2-4, 4-2-1 alongside reco. 2005-5. For Task 2: a per-licensee source that cannot be scraped generically."],
    ["FR-C1", "CNC / Commission de classification des oeuvres cinematographiques (visa d'exploitation)", "CNC", "classification_body", 6,
     "CINEMA RELEASES ONLY. The CNC states its commission is competent neither for television, DVD, VOD, video games nor the internet.",
     "https://www.cnc.fr/cinema/actualites/proteger-sans-censurer--la-classification-des-oeuvres-cinematographiques_1924881",
     "ongoing",
     "OUT OF SCOPE as a rule source; IN SCOPE as an optional input for theatrical films. A cinema interdiction pulls a film into at least the matching TV category; a CNC 'avertissement' maps to -12 for TV."],
    ["FR-S2", "solidarites.gouv.fr - Classification et signaletique de la television", "French government", "secondary", 7,
     "Government summary of the signaletique regime.", "https://solidarites.gouv.fr/classification-et-signaletique-de-la-television",
     "current",
     "Corroborated C-02 before the French primary text was located. States plainly: non-cinema channels not before 22h for -12; cinema channels not Wednesdays before 20h30; -16 after 22h30 / 20h30. Superseded as evidence by FR-R1 (Legifrance) and FR-R1d (csa.fr), both in French."],
    ["FR-X1", "Deliberation n. 2011-64 du 20 decembre 2011 - protection of minors, ON-DEMAND (SMAD) services",
     "Arcom (ex-CSA)", "regulator_binding", 2, "NON-LINEAR services established in France.",
     "https://www.lexing.law/wp-content/uploads/22492432.pdf", "JORF 2011-12-31",
     "OUT OF SCOPE (non-linear) but a VALUABLE CONTRAST: reuses the same five categories with DIFFERENT conditions (e.g. category IV not behind payment is accessible only 22:30-05:00). Proves the same category maps to different hours on different service types."],
    ["EU-D1", "AVMSD - Directive 2010/13/EU as amended by Directive (EU) 2018/1808, Article 6a", "EU / ERGA", "statute", 1,
     "Binds Member States, NOT directly applicable to a broadcast.", U_EU, "2018/1808",
     "The common ancestor of both national frameworks. Mandates an OUTCOME and permits time, age verification or other technical measures as ALTERNATIVES - the root cause of the rating-vs-hours asymmetry."],
    ["UK-S3", "Ofcom Broadcasting Code, Section Three - Crime, Disorder, Hatred and Abuse", "Ofcom", "regulator_binding", 2,
     "All Ofcom-licensed TV and radio.", U_S3, "current",
     "IN SCOPE via the context route, not the watershed. Rules 3.2/3.3 are permitted 'except where it is justified by the context', and context is Section Two's defined term whose third factor is the TIME OF BROADCAST. Wrongly excluded at first by a scoping test that searched for a single phrase (C-11)."],
    ["FR-R1c", "Arcom recommandation du 7 juin 2005, consolidated (as amended by deliberations 2012-57 and 2014-17)", "Arcom (ex-CSA)", "regulator_binding", 2,
     "French linear television services.", U_FR1C, "current consolidated",
     "THE operative French scheduling text, and it must be read consolidated: the 2014 amendment broadened the category III definition, so a row carrying the 2005 wording would UNDER-RATE content (C-09)."],
    ["FR-S1c", "Arcom - Protection of young people and persons under 18 (educational resources)", "Arcom", "regulator_summary", 5,
     "Public explainer covering all French services.", U_FRS1C, "current",
     "SECONDARY: corroboration only, never a rule source, because Arcom's own summary page has contradicted its binding text before (C-01). Its earlier URL was an internal STAGING hostname that never resolved, which the link triage had misreported as bot-blocked."],
    ["EU-D1b", "Directive (EU) 2018/1808, the amending directive", "EU", "statute", 1,
     "Amends 2010/13/EU. Binds Member States.", U_EUB, "CELEX 32018L1808",
     "PROVENANCE, not current rule text: the consolidated article is EU-D1. Held because amendment tracking requires knowing what changed and when, which is the check two separate extraction errors slipped past (C-09, C-14)."],
    ["EU-O1", "European Audiovisual Observatory - protection of minors / AVMSD spotlight", "Council of Europe", "secondary", 7,
     "Comparative mapping across Member States.", "https://www.obs.coe.int/en/web/observatoire/protection-of-minors",
     "ongoing", "Useful starting point for Task 2 scaling to dozens of countries."],
]
sheet("Sources", src, [11, 56, 16, 20, 9, 40, 44, 24, 72])

# ---- Open questions tab
oq = [["id", "issue", "affected_rows", "current_resolution", "action_required", "owner", "blocks_ground_truth"]]
oq += [
    ["C-01", "Arcom's own public summary page (FR-S1) describes -12 as broadcastable 'during the day, under certain conditions' - the identical wording it uses for -10. The binding text says not before 22:00 on non-cinema channels.",
     "FR-SCH-002, FR-SCH-003, FR-SCH-004",
     "CLOSED 2026-11-06. Binding text wins (authority_rank 2 beats 5), and that binding text is now confirmed in French from two independent sources (see C-02). FR-S1 is unreliable for -12 and must not be used as a rule source.",
     "None. Retained as the worked example of authority-rank conflict resolution, and as the reason regulator summary pages sit at rank 5 rather than rank 2.",
     "closed", "no"],
    ["C-02", "Arcom's English machine translation of art. 3 duplicated the cinema-channel sentence for cat. III and then said 'before 10 pm', leaving the service mapping ambiguous.",
     "FR-SCH-002, FR-SCH-003, FR-SCH-004, FR-CLS-003",
     "CLOSED 2026-11-06. Confirmed against the FRENCH text from two independent sources: Legifrance JORFTEXT000000446802 (the 2005 original) and the csa.fr consolidated page carrying the 'Modifiee par la deliberation n. 2014-17 du 5 mars 2014' banner. Both read identically: 'pour les chaines cinema et les services de paiement a la seance, ces programmes ne doivent pas etre diffuses le mercredi avant 20 h 30. Pour les autres services de television, ces programmes ne doivent pas etre diffuses avant 22 heures.' The Arcom French page for 2014-17 confirms art. 3 was replaced with the same wording. All affected rows promoted to approved.",
     "One residue: the '16 programmes per year, of which at most 4 cinema-banned-to-under-12s' quota in the cat. III derogation is still attested only in the English rendering. Confirm those two numbers in French. Does not block the hours.",
     "closed (quota numbers outstanding)", "no"],
    ["C-09", "Working C-02 exposed a substantive extraction error of our own. Delib. 2014-17 replaced the fifth alinea of art. 2 and BROADENED the category III definition, but the table still carried the 2005 wording: 'leur scenario recourt de facon repetee ET SYSTEMATIQUE' became 'le programme recourt de facon repetee'.",
     "FR-CLS-003 (corrected), FR-CLS-903 (superseded row added)",
     "CLOSED 2026-11-06. FR-CLS-003 now carries the current wording. Both wordings are recorded verbatim here: pre-2014 'leur scenario recourt de facon repetee ET SYSTEMATIQUE a la violence physique ou psychologique'; current 'notamment lorsque le programme recourt de facon repetee a la violence physique ou psychologique'. The superseded row FR-CLS-903 was later dropped when the manifest was reduced to current materials only - this entry is now the record of the old wording.",
     "None for the rule itself. The lesson matters more: the error survived because the English translation and the pre-2014 French text AGREED with each other, so cross-source corroboration did not catch it - only reading the amending instrument did. Treat any source whose amendment history is not explicit as suspect, and always diff the amending deliberation rather than trusting a page labelled 'consolidated'.",
     "closed", "no"],
    ["C-10", "Arcom's own FRENCH public page (FR-S1c) states the category III (-12) test as 'recourt de facon repetee a la violence physique ou psychologique, OU EVOQUE LA SEXUALITE ADULTE'. That adult-sexuality limb does not appear in the binding art. 2 wording we hold (as replaced by delib. 2014-17).",
     "FR-CLS-003",
     "None yet. Found 2026-11-06 while searching for the Legifrance id of delib. 2014-17.",
     "CLOSED 2026-11-06. The French primary text was downloaded and searched: 'sexualite' does not occur anywhere in the binding recommendation. The limb is a PRACTICE GLOSS on Arcom's public page, not binding text. The binding -12 trigger is repeated violence. Arcom may still apply the gloss when it classifies, so borderline sexual-content cases should be flagged for review rather than cleared - but the rule table should not encode an independent adult-sexuality trigger.",
     "closed", "no"],
    ["C-03", "French category V (-18) window rested on a 2004 instrument that could not be read",
     "FR-CV-001 to FR-CV-009, all now approved",
     "CLOSED 2026-11-06. The instrument is the Arcom notice of 15 December 2004. Its page body is drawn by JavaScript, so no fetch could ever retrieve it - every automated attempt returned an empty shell, and one early attempt returned 12,493 characters of pure site navigation that passed a naive length check. The user saved it from a browser, where the text had already rendered. CONFIRMED VERBATIM: 'Category V programs can only be shown between midnight and 5am.' The eligibility gate, the 208-per-year commercial threshold, the on-screen warning with article 227-22, and the six locking criteria are all confirmed against the primary.",
     "Six of the seven predicted rules verified verbatim; the rows had also carried the WRONG DATE for the instrument (23 rather than 15 December), now corrected. FR-CV-003 is SOUND BUT WEAKLY SOURCED - its proof quote is from a government summary while the primary says only that the regulator 'only authorizes' eligible services, so a total ban elsewhere is an inference, flagged in-row for a French regulatory lawyer. The doubt that created C-03 resolves in the OPPOSITE direction from the one feared: the deadlines have elapsed, meaning fully in force with no transitional relief. FINALLY, the stored text is Arcom's own ENGLISH translation, which warns that only the original French is authentic - every quote here is EN and a French-qualified reviewer must re-check them.",
     "closed", "no"],
    ["C-15", "Half the table carried no quote, so the quote check never looked at it",
     "all 103 approved rules",
     "CLOSED 2026-11-07. COVERAGE IS NOW 103 OF 103, all verifying against their stored source, 0 failing. The gap was an artifact of build order, not of the rules being unquotable: all 46 unquoted rows came from the FIRST commit, written when every fetch was being refused and there was no stored text to quote from. Leaving the field empty rather than paraphrasing was right at the time; not returning to it once the sources arrived was not. Not one rule written after the sources landed was missing a quote.",
     "THE METRIC WAS THE REAL DEFECT, and the lesson outlives the fix. 'VERIFIED 50, FAILED 0' counted only the rules that carried a quote, so the 52 without one were not failing - they were never shown to the check at all. A coverage number that counts only the rows which opted in will always report success. The verifier now prints the DENOMINATOR, and coverage is a RATCHET: an approved rule with no verbatim_quote FAILS the build, verified by removing one. Backfilling also exposed a second UK-FLM source misattribution (UK-FLM-004 cited the MDP statement for text that lives in Section One), which only became visible once the quote existed to be checked.",
     "closed", "no"],
    ["C-14", "UK access-control rows cited guidance predating the 2018 MDP restructure",
     "UK-ACC-002, UK-ACC-003 (both now approved)",
     "CLOSED 2026-11-06, and it resolved better than expected. With the current Section One text in hand, the substance of UK-ACC-003 turns out to be in the CURRENT CODE rather than only in the 2015 guidance: Rule 1.24 requires both that clear information be provided to help adults assess suitability AND - a condition the table did not have at all - that the mandatory daytime protection in place be CLEARLY EXPLAINED TO ALL VIEWERS. A gate nobody has been told about does not satisfy the rule. The row is re-sourced from guidance to binding text, raising its authority rank from 3 to 2. UK-ACC-002 stays on guidance, because the default-PIN point is an elaboration rather than Code text, but the requirement it elaborates - that the protection cannot be removed by the user - is in the current Code, so it explains a rule that still stands.",
     "The lesson survives the closure and should carry into Task 2: this was found only by reading the amending instrument's effect on the current consolidated text, exactly as C-09 was. Corroboration between same-vintage sources could never have surfaced it. The CI rule stands - no row may be approved while citing guidance older than the most recent amendment to the rule it interprets, unless the current binding text has been checked and the guidance confirmed still applicable, which is what happened here.",
     "closed", "no"],
    ["C-11", "Only Code Sections One and Two had been reviewed. Sections Three to Ten were assumed irrelevant to age ratings and broadcast hours.",
     "UK-REL-001 (added)",
     "CLOSED 2026-11-06, after the first answer was WRONG. I originally scoped the Code with one test - the phrase 'significant numbers of children', which is how Rules 1.27 and 4.7 key their child-audience restrictions - and concluded Sections Three and Five-Ten were out of scope. Section Three does not contain that phrase, so the test cleared it. But Rules 3.2 (hate speech) and 3.3 (abusive or derogatory treatment) are permitted 'except where it is justified by the context', and 'context' is Section Two's DEFINED term whose third factor is the TIME OF BROADCAST. So a Section Three judgment can turn on the hour. The test could not see that, so it was the wrong test, and everything it cleared was unproven rather than cleared. Added UK-HAT-001 and UK-HAT-002.",
     "THE RIGHT TEST IS TWO DOORS, NOT ONE: (a) 'significant numbers of children may be expected to be watching' -> Rules 1.27, 4.7; (b) 'justified by the context', which imports the time-of-broadcast factor -> Sections One, Two, Three. Sections Five-Eight instead use 'editorially justified', a narrower test that does NOT import the context definition and so never turns on the hour - verified against the live Section Five page, which uses 'editorially justified' only at Rule 5.3, uses 'justified by the context' in no rule, and mentions neither children nor the watershed nor any time of day. Sections Nine and Ten govern commercial references; Section Ten does use a context test, but for programmes about commercial companies - a sponsorship question, not a content-harm question - so it is out of scope on the same reasoning that excludes the ASA/BCAP advertising codes. IN SCOPE: Sections One, Two, Three, Four. LESSON: a single lexical test is not a scoping method. Any future country should be scoped by enumerating the escape clauses, not by searching for one phrase.",
     "closed (test corrected and re-run)", "no"],
    ["C-12", "Is broadcast-code-full.pdf (UK-S0) a usable substitute for the per-section HTML? It is one file covering all ten sections, which is operationally attractive.",
     "UK-S1, UK-S2, UK-S4, UK-S0",
     "NO - CLOSED 2026-11-06. It is the January 2019 print edition and predates the Code in force. Ofcom's 31 Dec 2020 statement states the Code 'is now published on the Ofcom website and is no longer available in print', so no consolidated PDF has been maintained since. The Code in force covers programmes broadcast on or after 23:00 on 31 Dec 2020; the 31 Dec 2020 amendments changed the Section Three hate-speech definition and Section Nine product placement plus minor updates; and Sections One and Two were revised again on 2023-03-16 and 2024-02-19. UK-S0 demoted to optional/original_superseded.",
     "None. But note the near-miss: an earlier version of this repo recorded UK-S0 as CONTAINING UK-S1/S2/S4 and advised fetching it to save three downloads. Following that advice would have pinned the UK rules to 2019 text and silently dropped the 2023 and 2024 revisions - the same class of error as C-09, where an outdated edition got treated as current. The lesson is that a bundle is only a shortcut if its currency is established FIRST, and 'it is a single tidy file' is exactly the kind of convenience that discourages checking.",
     "closed", "no"],
    ["C-04", "Source documents not collected, so quote integrity could not be checked",
     "the whole table",
     "CLOSED 2026-11-06. ALL 20 of 20 sources are now on disk and every quote that EXISTS resolves: 56 verified, 0 failed, 0 inconclusive. Note the denominator, which C-15 covers: only 56 of 102 approved rules carry a quote at all. The automated hosts refused automated clients, so the user retrieved the blocked documents from a browser; a Playwright fetcher on a GitHub runner collected two more before datacenter IPs were refused by Cloudflare.",
     "Collecting them was not a formality - it CHANGED THE TABLE. The quote check failed four rules the moment real sources landed: two paraphrases written as quotes, one citing the wrong document, and one whose quote ended in a full stop I had added, cutting the sentence before the words 'which cannot be removed by the user' that make the rule enforceable. Mining the guidance then added nine rules the Code text alone does not yield, including the fact that the watershed is a ramp rather than a gate, that a +1 service makes the identical file compliant on one channel and not another, and that bleeping does not automatically make a programme daytime-safe.",
     "closed", "no"],
    ["C-05", "Ofcom Section One uses 'children' = under FIFTEEN while the section's principle protects under-EIGHTEENS.",
     "UK-DEF-001, UK-SCH-001, UK-DRG-001, UK-IMI-001, UK-OCC-001",
     "Both recorded explicitly. No conflict - just a conflation trap.",
     "Note it in the prompt. Add a test case where the distinction changes the answer.",
     "prompt author", "no"],
    ["C-06", "French channel conventions can be stricter than the general recommendation and are not consolidated anywhere. There is no single document containing all applicable French rules for a given broadcast.",
     "FR-CNV-001 (and potentially any FR row)",
     "Out of scope for v1. The channel_specific_override concept is recorded.",
     "For Task 2: treat conventions as a per-licensee data feed. Cannot be scraped generically; needs a local expert or a licensee-supplied extract.",
     "local expert", "no - but caps achievable accuracy for France"],
    ["C-07", "Judgment-based thresholds are uncalibrated - almost no decided cases collected",
     "35 judgment_based rules",
     "PARTLY ADDRESSED 2026-11-06, not closed. The Toofan decision (bulletin 553, 7 Sep 2026) is now collected and mined, yielding four rules: a real threshold anchor (BBFC 15 with sustained graphic violence at 11:30 breaches Rule 1.3), proof from a regulator that the offence and scheduling determinations are separate, the cultural and religious calendar as an audience-composition factor that appears nowhere in the Code text, and the finding that warnings must convey SEVERITY rather than mere presence. The guidance notes added nine further rules with worked examples and named prior decisions.",
     "STILL THE TABLE'S WEAKEST AREA. 35 of 99 rules are judgment-based and ONE decided case cannot calibrate them - it is an anchor, not a scale: it says this combination at this hour breached, not where the line sits. The guidance cites roughly a dozen further decisions by name (The X Factor Final, Candy Bar Girls, Emmerdale, Coronation Street, EastEnders, Ice Road Truckers, Taggart, Midsomer Murders, Hell's Kitchen USA, Amores Perros, Stylista); collecting those bulletins is the single highest-value remaining work on this table. Until then, treat every judgment_based rule as routing to a human rather than as deciding anything.",
     "open", "yes"],
    ["C-08", "Correlated error risk: this table and the prompt would share an author and therefore share mistakes - the exact failure mode Task 2 asks about.",
     "ALL rows",
     "Two mitigations available: verbatim_quote + source_url let a reviewer check a row without reading the prompt; bright-line rows are checkable against primary sources with no knowledge of the solution.",
     "Have the bright-line rows INDEPENDENTLY RE-DERIVED from primary sources by a second pass that has not seen this table, then compare. Treat any divergence as a finding about both.",
     "second reviewer", "YES - methodologically"],
]
sheet("Open_Questions", oq, [8, 76, 30, 60, 76, 24, 20])

# ---- Pivot readable tab
piv = [["country", "classification / level", "service type", "earliest permitted broadcast time",
        "key content threshold", "determinacy", "status", "source rows"]]
piv += [
    ["FR", "I - tous publics", "all", "no restriction", "all audiences", "bright_line", "approved", "FR-CLS-001"],
    ["FR", "II - -10", "all", "no clock restriction; NOT within children's programmes",
     "certain scenes liable to shock under-10s", "conditional", "approved", "FR-CLS-002, FR-SCH-001"],
    ["FR", "III - -12", "other than cinema channels / PPV", "22:00",
     "liable to disturb under-12s; REPEATED physical or psychological violence (2014-17 dropped 'et systematique'); cinema -12 interdiction",
     "bright_line", "approved", "FR-CLS-003, FR-SCH-002"],
    ["FR", "III - -12", "cinema channels, pay-per-view", "20:30 on Wednesdays (restriction is Wednesday-specific)",
     "as above", "bright_line", "approved", "FR-SCH-003"],
    ["FR", "III - -12 (derogation)", "all", "20:30, except Tue/Fri/Sat/holiday eve/school holidays; max 16 per year (max 4 cinema-banned-u12)",
     "as above", "conditional", "approved (quota numbers indicative)", "FR-SCH-004"],
    ["FR", "IV - -16", "other than cinema channels / PPV", "22:30",
     "erotic character or great violence; liable to harm under-16s", "bright_line", "approved", "FR-CLS-004, FR-SCH-005"],
    ["FR", "IV - -16", "cinema channels, pay-per-view", "20:30", "as above", "bright_line", "approved", "FR-SCH-006"],
    ["FR", "V - -18", "cinema / high-production-commitment / PPV ONLY, with access guarantees",
     "00:00-05:00 (closed window) + decoder lock + on-screen warning",
     "pornographic or very great violence; cinema -18 interdiction", "bright_line", "UNVERIFIED (C-03)",
     "FR-CLS-005, FR-SCH-007, FR-CV-001, FR-CV-002, FR-CV-004"],
    ["FR", "V - -18", "all other services", "TOTAL PROHIBITION", "as above", "bright_line", "UNVERIFIED (C-03)", "FR-CV-003"],
    ["FR", "any category", "all", "06:00-22:00 violence limit applies REGARDLESS of category",
     "violence (incl. psychological) must not appear continuous, the only solution to conflicts, or exacerbated",
     "judgment_based", "approved", "FR-VIO-001"],
    ["FR", "prohibited outright", "all", "no permitted time",
     "offends human dignity (sexual violence, perversions, degradation); pornography depicting under-18s; extreme or gratuitous violence",
     "bright_line", "approved", "FR-PRO-001, FR-PRO-002, FR-PRO-003"],
    ["FR", "music videos", "all", "soft preference for after 22:00 - NOT a prohibition",
     "likely to offend young viewers; exempt from systematic signage", "judgment_based", "approved",
     "FR-MUS-001, FR-MUS-002"],
    ["UK", "no age rating exists for linear TV", "free-to-air (default)", "watershed 21:00-05:30",
     "material unsuitable for children, judged by appropriate scheduling and context", "bright_line + judgment",
     "approved", "UK-SCH-001, UK-SCH-002, UK-DEF-002, UK-DEF-003"],
    ["UK", "n/a", "premium subscription film, unprotected", "watershed 20:00", "as above", "conditional", "approved", "UK-SCH-003"],
    ["UK", "n/a", "premium subscription film", "20:00 for films up to BBFC 15, without MDP", "BBFC 15 or equivalent",
     "conditional", "approved", "UK-FLM-004"],
    ["UK", "n/a", "any service", "21:00 for BBFC 18 films, unless MDP is in place", "BBFC 18 or equivalent",
     "conditional", "approved", "UK-FLM-002"],
    ["UK", "n/a", "premium subscription film / PPV / scheduled channels on vertically integrated pay platforms",
     "ANY TIME with mandatory daytime protection (PIN pre-2100 and post-0530)",
     "unsuitable programmes and films up to BBFC 18. NOT available to free-to-air DTT. Excludes adult sex material.",
     "conditional", "approved", "UK-FLM-003, UK-FLM-005"],
    ["UK", "n/a", "premium subscription / PPV with mandatory restricted access", "22:00-05:30 ONLY",
     "'adult sex material' - strong sexual images/language for the primary purpose of sexual arousal",
     "conditional", "approved", "UK-SEX-002"],
    ["UK", "n/a", "all", "21:00 (absolute pre-watershed bar)", "the most offensive language", "bright_line", "approved", "UK-LNG-001"],
    ["UK", "prohibited outright", "all", "no permitted time",
     "material that might seriously impair under-18s' development; BBFC R18-equivalent material; R18 films; films refused BBFC classification",
     "bright_line", "approved", "UK-GEN-001, UK-SEX-001, UK-FLM-001, UK-FLM-006"],
    ["UK", "n/a", "all, incl. niche music channels", "21:00 thresholds tighten; no separate music-video regime",
     "sexualised imagery appropriately limited; no performers inadequately covered; lyrics and imagery assessed TOGETHER",
     "judgment_based", "approved", "UK-MUS-001, UK-MUS-002, UK-MUS-003"],
    ["EU", "framework only - not directly applicable", "all AVMS", "no time rule; mandates the outcome",
     "minors 'will not normally hear or see' content that may impair their development; measures proportionate; most harmful content strictest",
     "bright_line", "approved", "EU-FRM-001, EU-FRM-002"],
]
s = sheet("Pivot_Readable", piv, [8, 26, 40, 44, 54, 18, 18, 42])
s.insert_rows(1)
s["A1"] = ("DERIVED VIEW - do not edit. Generated from the Rules tab. "
           "Edit rules in the Rules tab, then regenerate. "
           "NOTE: the UK has NO per-programme age rating for linear TV - the correct UK output is a "
           "scheduling verdict plus the earliest permissible time, not an age label.")
s["A1"].font = Font(bold=True, size=10, color="C00000")
s["A1"].alignment = Alignment(wrap_text=True, vertical="center")
s.merge_cells("A1:H1")
s.row_dimensions[1].height = 42
s.freeze_panes = "A3"

import os as _os
import csv as _csv
from pathlib import Path as _Path

_RULES_DIR = _Path(__file__).resolve().parents[1] / "rules"
_RULES_DIR.mkdir(parents=True, exist_ok=True)
_XLSX = _RULES_DIR / "RULES_TABLE_v1.xlsx"
wb.save(_XLSX)

# Diffable CSV mirrors. The workbook is a binary blob git cannot diff, so a rule change
# would otherwise be unreviewable in a pull request.
#
# Only two tabs are mirrored. Rules.csv because the decision pipeline READS it, and
# Open_Questions.csv because the conflict log is worth reading on its own. The other four
# tabs (Legend, How_to_use, Sources, Pivot_Readable) are reference material that already
# exists inside the workbook; mirroring them doubled the file count for no reader.
_MIRROR = {"Rules", "Open_Questions"}
_CSV_DIR = _RULES_DIR / "csv"
_CSV_DIR.mkdir(exist_ok=True)
for _name in [n for n in wb.sheetnames if n in _MIRROR]:
    _ws = wb[_name]
    with (_CSV_DIR / f"{_name}.csv").open("w", newline="", encoding="utf-8") as _fh:
        _w = _csv.writer(_fh, quoting=_csv.QUOTE_ALL, lineterminator="\n")
        for _row in _ws.iter_rows(values_only=True):
            if all(_c is None for _c in _row):
                continue
            _w.writerow(["" if _c is None else str(_c) for _c in _row])

print(f"wrote {_XLSX.relative_to(_RULES_DIR.parent)} "
      f"({round(_os.path.getsize(_XLSX)/1024, 1)} KB) + {len(wb.sheetnames)} CSV mirrors")
print(f"rules rows: {len(R)}")
from collections import Counter
print("by country:", dict(Counter(r[1] for r in R)))
print("by status :", dict(Counter(r[22] for r in R)))
print("by determinacy:", dict(Counter(r[13] for r in R)))
print("by ambiguity_flag:", dict(Counter(r[14] for r in R)))
print("human_review_required=yes:", sum(1 for r in R if r[16] == "yes"))
assert all(len(r) == len(COLS) for r in R), "column count mismatch"
ids = [r[0] for r in R]
assert len(ids) == len(set(ids)), "duplicate rule_id"
print("tabs:", wb.sheetnames)
