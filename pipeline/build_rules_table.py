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
U_S1 = "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-one-protecting-under-eighteens"
U_S2 = "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code/section-two-harm-offence"
U_G1 = "https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf"
U_M1 = "https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf"
U_L1 = "https://www.legislation.gov.uk/ukpga/2003/21/section/319"
U_FR1 = "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000446802"  # 2005 ORIGINAL
U_FR1C = ("https://www.arcom.fr/se-documenter/espace-juridique/textes-juridiques/recommandation-du-7-juin-2005-aux-editeurs-de-services-de-television-concernant-la-signaletique-jeunesse-et-la-classification-des-programmes")  # CURRENT consolidated French text - cite this for current law
U_FR2 = "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/deliberation-no-2014-17-march-5-2014-amending-notice-no-2005-5-june-7-2005-television-service-editors-concerning-youth-signage-and-classification-programmes"
U_FRV = "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france"
U_FRL = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205"
U_CONV = "https://www.arcom.fr/sites/default/files/2023-05/MeD_C8.pdf"
U_EU = "https://www.legislation.gov.uk/eudr/2010/13/article/6a"

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
    "Children are people under fifteen.", "EN", "high")

add("UK-DEF-002", "UK", "Ofcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "definition", "n/a",
    "'Appropriate scheduling' is judged on: nature of content; likely number and age range of child viewers (taking into account school time, weekends and holidays); programme start and finish time; nature of the channel/programme; likely audience expectations for that channel at that time and day.",
    "n/a", "n/a",
    "Broadcasters serving ECTT Parties must also consider time differences in the country of reception.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "S1 definitions", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

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
    "", "EN", "high")

add("UK-GEN-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "Broadcasters must take all reasonable steps to protect people under eighteen.",
    "n/a - general duty", "n/a",
    "Open-ended duty; informs every other decision.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.2", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

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
    "free_to_air; all_linear_tv_default", "scheduling_general", "watershed_bound",
    "Television broadcasters must observe the watershed. Material unsuitable for children should not, in general, be shown before 21:00 or after 05:30.",
    "Watershed 21:00-05:30.", "window=21:00-05:30",
    "Does NOT apply to BBC ODPS. Displaced by 20:00 for unprotected premium subscription film services (UK-SCH-003) and disapplied where mandatory daytime protection is in place (UK-FLM-003).",
    "bright_line", "clear",
    "The single most important UK bright line. Note it is an OPEN-ENDED period, structurally unlike the French closed windows.",
    "no", "UK-S1", "Rule 1.4", U_S1, "2021-03-03", "open", "approved",
    "the watershed applies from 21:00 to 05:30", "EN", "high")

add("UK-SCH-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film", "scheduling_general", "watershed_bound",
    "Premium subscription film services WITHOUT protection operate a 20:00 watershed rather than 21:00.",
    "Watershed 20:00.", "window=20:00-05:30",
    "Conditional on service type AND absence of protection. Requires service_type input.",
    "conditional", "clear",
    "Proves the watershed itself is service-dependent, not universal.", "no",
    "UK-S1", "Rule 1.4", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "medium")

add("UK-SCH-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "The transition to more adult material must not be unduly abrupt at the watershed. The strongest material should appear later in the schedule.",
    "No fixed interval specified.", "judgment:post_watershed_ramp",
    "A programme starting after 21:00 should not open with its strongest material; a programme crossing 21:00 must not suddenly become unsuitable.",
    "judgment_based", "clear",
    "No numeric threshold exists. Escalate to human review when a test case places strong material in the first minutes after 21:00.",
    "yes", "UK-S1 + UK-G1", "Rule 1.6; UK-G1 s.1", U_G1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-SCH-005", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "fear_distress", "context_dependent",
    "Clear information about content that may distress some children should be given, if appropriate, taking into account the context.",
    "n/a - information duty", "n/a",
    "'If appropriate' - discretionary, context-driven.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.7", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-DRG-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "drugs_alcohol_smoking", "context_dependent",
    "Drugs, smoking, solvents and alcohol must not be featured in programmes made primarily for children without strong editorial justification; and must not be condoned, encouraged or glamorised in other programmes before the watershed without editorial justification.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=editorial_justification",
    "Two different thresholds: 'strong editorial justification' for children's programmes vs 'editorial justification' elsewhere pre-watershed.",
    "conditional", "clear",
    "The two-tier justification standard is easy to flatten; keep both.", "no",
    "UK-S1", "Rule 1.10", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-VIO-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "context_dependent",
    "Violence, its after-effects and descriptions of violence (verbal or physical) must be appropriately limited in programmes broadcast before the watershed, and must be justified by the context.",
    "Restriction bites before 21:00; post-watershed governed by context.",
    "not_before=21:00;unless=appropriately_limited_and_context_justified",
    "'Appropriately limited' AND 'justified by the context' - a double test. Context per UK-DEF-003.",
    "judgment_based", "clear",
    "Primary violence rule. No intensity scale is given in the Code; applied thresholds come only from enforcement precedent.",
    "yes", "UK-S1", "Rule 1.11", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-VIO-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "context_dependent",
    "Programmes made primarily for children must not include material that condones or glamorises violent, dangerous or seriously antisocial behaviour likely to encourage imitation.",
    "Applies at all times to children's programmes.", "prohibited_in=children_programmes",
    "Turns on programme type, not clock time.",
    "judgment_based", "clear", "", "no",
    "UK-S1", "Rule 1.12", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-IMI-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "imitable_behaviour", "context_dependent",
    "Dangerous behaviour, or behaviour easily imitable by children in a manner that is harmful, must not be featured before the watershed unless there is editorial justification.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=editorial_justification",
    "Cross-refers to Rules 2.4 and 2.5.",
    "conditional", "clear", "", "no",
    "UK-S1", "Rule 1.13", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

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
    "", "EN", "high")

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
    "premium_subscription; pay_per_view", "sexual_content", "restricted_window",
    "'Adult sex material' (strong sexual images/language broadcast for the primary purpose of sexual arousal) may only be broadcast between 22:00 and 05:30, on premium subscription or pay-per-view/night services operating with MANDATORY RESTRICTED ACCESS.",
    "22:00-05:30 only, and only on eligible services with mandatory restricted access.",
    "window=22:00-05:30;requires=mandatory_restricted_access",
    "NOT unlocked by mandatory daytime protection - MDP expressly excludes adult sex material.",
    "conditional", "clear",
    "Three distinct UK access concepts must not be conflated: mandatory restricted access (this rule), mandatory daytime protection (films), and no protection. A model treating 'PIN protected' as one concept will wrongly allow this in daytime.",
    "no", "UK-S1 + UK-M1", "Rule 1.18", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

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
    "", "EN", "high")

add("UK-SEX-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "context_dependent",
    "Representations of sexual intercourse must not occur before the watershed unless there is a SERIOUS EDUCATIONAL PURPOSE. Any discussion or portrayal of sexual behaviour before the watershed must be editorially justified and appropriately limited.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=serious_educational_purpose",
    "'Serious educational purpose' is a higher bar than ordinary editorial justification.",
    "conditional", "clear", "", "no",
    "UK-S1", "Rule 1.20", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-NUD-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "nudity", "context_dependent",
    "Nudity before the watershed must be justified by the context.",
    "Restriction bites before 21:00.", "not_before=21:00;unless=context_justified",
    "Nudity is NOT automatically post-watershed; context can justify it earlier.",
    "judgment_based", "clear",
    "Common over-rating trap: treating any nudity as automatically post-watershed.", "yes",
    "UK-S1", "Rule 1.21", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-FLM-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "prohibited",
    "No film REFUSED classification by the BBFC may be broadcast, unless it has subsequently been classified or the BBFC has confirmed it would not be subject to compulsory cuts under current standards. Restrictions also apply to cut versions.",
    "No permitted time unless subsequently classified/confirmed.", "prohibited;unless=subsequently_classified",
    "Survives MDP - unchanged by the 2018 review.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "UK-S1", "Rule 1.22", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-FLM-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "watershed_bound",
    "BBFC 18-rated films (or their equivalent) must not be broadcast before 21:00 on ANY service, except where there is mandatory daytime protection in place.",
    "Not before 21:00, unless MDP.", "not_before=21:00;unless=mandatory_daytime_protection",
    "Amended with effect 1 Jan 2019: the previous pay-per-view-specific carve-out was replaced by the general MDP concept.",
    "conditional", "clear",
    "THE clearest proof that rating does not determine hours: the same BBFC 18 film is barred pre-21:00 on one service and permitted at any hour on another, purely because of a technical access measure.",
    "no", "UK-S1 + UK-M1", "Rule 1.23", U_M1, "2019-01-01", "open", "approved",
    "", "EN", "high")

add("UK-FLM-003", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film; pay_per_view; scheduled_channels_on_vertically_integrated_pay_platforms",
    "film_carryover", "any_time_with_protection",
    "Where MANDATORY DAYTIME PROTECTION is in place, programmes unsuitable for children that would usually be scheduled post-watershed, and films up to BBFC 18 or equivalent, may be broadcast AT ANY TIME OF DAY. Clear information must be provided about the content and about the protection in place.",
    "Any time of day.", "any_time;requires=mandatory_daytime_protection",
    "MDP = a PIN protection system in place pre-2100 and post-0530, non-removable by the user, required on each entry, with accurate metadata. NOT available to free-to-air DTT (e.g. Freeview) or to channels not on a vertically integrated pay-TV platform. Excludes adult sex material. Does not cure R18 or refused-classification films.",
    "conditional", "clear",
    "service_type AND access_control are mandatory inputs. If absent, the correct output is a missing-information flag, NOT an assumption of free-to-air.",
    "no", "UK-M1", "Rule 1.24", U_M1, "2019-01-01", "open", "approved",
    "Mandatory daytime protection means there is a PIN protection system in place pre-2100 and post-0530.",
    "EN", "high")

add("UK-FLM-004", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "premium_subscription_film", "film_carryover", "watershed_bound",
    "Films up to BBFC 15 or equivalent may be broadcast from 20:00 on premium subscription film services WITHOUT mandatory daytime protection.",
    "Not before 20:00.", "not_before=20:00",
    "Carve-out retained in the 2018 review: Ofcom had proposed removing it and did not.",
    "conditional", "clear", "", "no",
    "UK-M1", "Rule 1.24", U_M1, "2019-01-01", "open", "approved",
    "", "EN", "medium")

add("UK-FLM-005", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "pay_per_view", "film_carryover", "any_time_with_protection",
    "Pay-per-view services may broadcast films up to BBFC 18 or equivalent at any time, provided mandatory daytime protection is in place. They must additionally provide content information, operate a detailed itemised billing system, and make subscribers aware of their child-protection systems.",
    "Any time of day.", "any_time;requires=mandatory_daytime_protection",
    "Billing and subscriber-information duties are additional and are not per-asset checkable.",
    "conditional", "clear", "", "no",
    "UK-S1 + UK-M1", "Rule 1.25", U_M1, "2019-01-01", "open", "approved",
    "", "EN", "high")

add("UK-FLM-006", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "prohibited",
    "BBFC R18-rated films must not be broadcast.",
    "No permitted time.", "prohibited",
    "None. Unchanged by the 2018 MDP review.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "UK-S1", "Rule 1.26", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-OCC-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "occult_paranormal", "watershed_bound",
    "Demonstrations of exorcism, occult practices or paranormal activity PRESENTED AS REAL must not be shown before the watershed. Programmes treating such activity as entertainment must not be broadcast when significant numbers of children may be expected to be watching. DRAMA, FILM AND COMEDY ARE EXEMPT.",
    "Not before 21:00 where presented as real.", "not_before=21:00;exempt=drama,film,comedy",
    "Three-way split: presented-as-real (pre-watershed ban), entertainment (audience-based restriction), fiction (exempt).",
    "conditional", "clear",
    "The fiction exemption is a frequent over-rating trap.", "no",
    "UK-S1", "Rule 1.27", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-WEL-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "participant_welfare", "context_dependent",
    "Due care must be taken over the physical and emotional welfare and the dignity of under-18s who take part in or are otherwise involved in programmes, IRRESPECTIVE OF ANY CONSENT given by the participant or a parent/guardian. Under-18s must not be caused unnecessary distress or anxiety.",
    "Applies at all times.", "n/a",
    "Consent is expressly irrelevant.",
    "judgment_based", "clear",
    "Relevant where a content description involves minors as participants; not a scheduling rule.", "no",
    "UK-S1", "Rules 1.28-1.29", U_S1, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-OFF-001", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "offence_general", "context_dependent",
    "Material which may cause offence must be justified by the context. Such material may include offensive language, violence, sex, sexual violence, humiliation, distress, violation of human dignity, and discriminatory treatment or language.",
    "Context-determined.", "judgment:context",
    "Supplies the harm categories the UK actually recognises - useful as the UK category vocabulary.",
    "judgment_based", "clear", "", "no",
    "UK-S2", "Rule 2.3", U_S2, "2021-03-03", "open", "approved",
    "", "EN", "high")

add("UK-IMI-002", "UK", "Ofcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "imitable_behaviour", "context_dependent",
    "Programmes must not include material (whether in individual programmes OR IN PROGRAMMES TAKEN TOGETHER) which, taking into account the context, condones or glamorises violent, dangerous or seriously antisocial behaviour and is likely to encourage others to copy such behaviour.",
    "Applies at all times, context-determined.", "judgment:context",
    "'In programmes taken together' makes cumulative, cross-programme assessment explicit.",
    "judgment_based", "clear",
    "Cross-programme accumulation cannot be assessed from a single asset description - flag for channel-level review.",
    "yes", "UK-S2", "Rule 2.4", U_S2, "2021-03-03", "open", "approved",
    "", "EN", "high")

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
    "", "EN", "high")

add("UK-MUS-001", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv; music_channels", "music_videos", "context_dependent",
    "Pre-watershed music videos: sexualised images not banned but must be editorially justified and appropriately limited; explicit sexual behaviour avoided; intrusive or prolonged shots of body parts increase sexual impact; BDSM imagery not prohibited but explicit imagery avoided (shot length, repetition and overall theme considered); provocative/sexualised dancing limited; lyrics clearly focused on sex avoided.",
    "Thresholds tighten before 21:00.", "not_before=21:00;unless=limited_and_justified",
    "NICHE MUSIC CHANNELS STILL CARRY RESPONSIBILITY toward possible child viewers - a small or genre-specific audience does not remove the duty. Whether the video was supplied as a child-audience edit (e.g. marked 'pre 9pm') is a relevant input.",
    "judgment_based", "clear",
    "Lyrics that seem mild on audio alone can become highly sexualised when paired with sexual imagery - so audio and video must be assessed TOGETHER, not independently. Independent tagging systematically under-rates music videos.",
    "yes", "UK-G1", "UK-G1 s.2", U_G1, "", "open", "approved",
    "", "EN", "high")

add("UK-MUS-002", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv; music_channels", "nudity", "watershed_bound",
    "Pre-watershed music videos should not show performers inadequately covered, particularly the breasts, genitals or buttocks. Underwear and bikinis are not prohibited; whether the clothing is PRESENTED SEXUALLY is what matters.",
    "Restriction bites before 21:00.", "not_before=21:00",
    "Fetish clothing combined with sexual behaviour needs particular care.",
    "conditional", "clear", "", "no",
    "UK-G1", "UK-G1 s.2", U_G1, "", "open", "approved",
    "", "EN", "high")

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
    "", "EN", "high")

add("UK-TRL-001", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv", "trailers", "watershed_bound",
    "Trailers shown before the watershed for post-watershed programmes must contain only material appropriate for pre-watershed broadcast. Viewers do not choose to watch trailers. Trailers may need restricting around children's programming, family shows and sports coverage.",
    "Pre-watershed trailers held to pre-watershed standard.", "not_before=21:00;standard=pre_watershed_content",
    "The parent programme's own permitted slot does NOT license its trailer.",
    "judgment_based", "clear", "", "no",
    "UK-G1", "UK-G1 s.1", U_G1, "", "open", "approved",
    "", "EN", "high")

add("UK-SCH-006", "UK", "Ofcom", "regulator_guidance", 3, "yes",
    "all_linear_tv", "scheduling_general", "context_dependent",
    "Specific care areas: family viewing shows (suit family viewing throughout; extra caution if running past 21:00; daytime repeats need separate thought); soaps (each episode scheduled on its own merits - a long-running storyline does not itself supply context); post-watershed content edited for daytime (some content remains unsuitable regardless of editing; FREQUENT BLEEPING HAS A CUMULATIVE EFFECT).",
    "Context-determined.", "judgment:appropriate_scheduling",
    "+1 (timeshift) services need specific attention: a 21:00 broadcast becomes 22:00 on +1, but a 20:00 broadcast becomes 21:00.",
    "judgment_based", "clear",
    "The +1 point is a good adversarial test case - it changes the answer with no change to content.",
    "no", "UK-G1", "UK-G1 s.1", U_G1, "", "open", "approved",
    "", "EN", "high")

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
    "", "FR", "high")

add("FR-VIO-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "category_independent",
    "Between 06:00 and 22:00, and a fortiori in programmes intended for young audiences, violence - INCLUDING PSYCHOLOGICAL VIOLENCE - must not be able to be perceived as continuous, as the only solution to conflicts, or in an exacerbated form.",
    "Restriction applies 06:00-22:00.", "restricted_window=06:00-22:00",
    "CATEGORY-INDEPENDENT: a programme can be category I or II and still breach this. Replaced by delib. 2014-17.",
    "judgment_based", "clear",
    "A solution that only reasons about the I-V categories will miss this rule entirely.", "yes",
    "FR-R1 (as amd. FR-A2)", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "la violence, meme psychologique", "FR", "high")

add("FR-VIO-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "category_independent",
    "Programmes on HISTORICAL OR CONTROVERSIAL subjects may be broadcast before 22:00 if the editor provides EDUCATIONAL SUPPORT going beyond a mere written or spoken warning.",
    "Permits pre-22:00 broadcast subject to the condition.",
    "not_before=22:00;unless=educational_support_beyond_warning",
    "A warning alone is expressly insufficient.",
    "conditional", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-VIO-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "fear_distress", "category_independent",
    "For difficult images or testimony concerning particularly dramatic events, in news and other programmes, the editor must take precautions and WARN THE PUBLIC IN ADVANCE.",
    "Applies at all times.", "n/a;requires=advance_warning",
    "Applies to news, which France otherwise exempts from classification.",
    "conditional", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 1", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-CLS-001", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "I_tous_publics",
    "Category I - programmes for all audiences. NO pictogram.",
    "No restriction.", "none",
    "The editor classifies via an internal commission de visionnage.",
    "bright_line", "clear", "", "no",
    "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "categorie I (aucune signaletique) : les programmes pour tous publics", "FR", "high")

add("FR-CLS-002", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "II_-10",
    "Category II (-10) - programmes CERTAIN SCENES of which are liable to shock minors under 10.",
    "See FR-SCH-001.", "see=FR-SCH-001", "",
    "judgment_based", "clear", "", "no",
    "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "", "FR", "high")

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
    "wording is kept as FR-CLS-903. Verified 2026-11-06 against the STORED French primary "
    "text (FR-R1c/FR-R1d), which reads '...notamment lorsque le programme recourt de facon "
    "repetee a la violence physique ou psychologique'. C-10 RESOLVED by the same check: the "
    "words 'sexualite adulte' do NOT occur anywhere in the binding recommendation, so the "
    "'ou evoque la sexualite adulte' limb on Arcom's public page (FR-S1c) is a PRACTICE GLOSS, "
    "not binding text. Do not treat adult sexuality as an independent -12 trigger; the "
    "binding trigger is repeated violence. Arcom may still apply the gloss in practice, so "
    "flag borderline sexual-content cases for review rather than clearing them.",
    "yes", "FR-R1 (as amd. FR-A2)", "art. 2 al. 5", U_FR1C, "2014-04-09", "open", "approved",
    "les programmes pouvant troubler les mineurs de 12 ans, notamment lorsque le programme "
    "recourt de facon repetee a la violence physique ou psychologique", "FR", "high")

add("FR-CLS-903", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "all_linear_tv", "classification_scheme", "III_-12",
    "SUPERSEDED (2005-2014 wording). Category III (-12) - programmes liable to disturb "
    "under-12s, in particular where THEIR SCENARIO resorts in a repeated AND SYSTEMATIC way to "
    "physical or psychological violence.",
    "n/a - historical", "see=FR-CLS-003",
    "Replaced by delib. 2014-17 (JORF 2014-04-09), which removed 'et systematique' and changed "
    "'leur scenario' to 'le programme'.",
    "judgment_based", "clear",
    "Retained to demonstrate the versioning rule: a replaced provision is closed with a "
    "valid_to and status=superseded, never overwritten, so a past decision can still be "
    "explained by the rule version in force at the time. Naming convention: 9xx = historical.",
    "no", "FR-R1", "art. 2 al. 5", U_FR1, "2005-07-08", "2014-04-08", "superseded",
    "leur scenario recourt de facon repetee et systematique a la violence physique ou "
    "psychologique", "FR", "high")

add("FR-CLS-004", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "IV_-16",
    "Category IV (-16) - cinematographic works banned to under-16s in cinemas, and programmes OF AN EROTIC CHARACTER OR OF GREAT VIOLENCE, liable to harm the physical, mental or moral development of under-16s.",
    "See FR-SCH-005/006.", "see=FR-SCH-005", "",
    "judgment_based", "clear", "", "no",
    "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "", "FR", "high")

add("FR-CLS-005", "FR", "Arcom", "regulator_binding", 2, "definition_only",
    "all_linear_tv", "classification_scheme", "V_-18",
    "Category V (-18) - cinematographic works banned to under-18s in cinemas, and PORNOGRAPHIC programmes or programmes of VERY GREAT VIOLENCE, reserved for a warned adult audience and liable to harm the physical, mental or moral development of under-18s.",
    "See FR-CV-001 to FR-CV-003.", "see=FR-CV-002", "",
    "judgment_based", "clear", "", "no",
    "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "", "FR", "high")

add("FR-FLM-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "film_carryover", "context_dependent",
    "The classification a film receives for CINEMA release MAY SERVE AS AN INDICATION for its television classification, but the editor must verify that the rating transfers without harm and MAY STRENGTHEN IT.",
    "n/a - classification input rule", "n/a",
    "French practice is explicitly to RAISE the age limit between cinema and television, because a child who could not enter the cinema can easily be in front of a TV set.",
    "judgment_based", "clear",
    "The CNC/cinema rating is an INPUT, never the output. The TV category is a separate determination and may be stricter.",
    "no", "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "", "FR", "high")

add("FR-FLM-002", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "all_linear_tv", "film_carryover", "n/a",
    "Reclassification procedure: works at least 20 YEARS since their last visa may be submitted for revision for TV broadcast, by JOINT request of editor and producer, at least 8 months before scheduling. Arcom forwards up to 20 requests per year to the Commission de classification, which must opine at least 1 month before broadcast.",
    "n/a - procedural", "n/a",
    "The only route by which the cinema classification commission revisits a rating for television purposes.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Procedural, not a per-asset rating rule. Recorded for completeness.", "no",
    "FR-R1", "art. 2", U_FR1C, "2005-07-08", "open", "approved",
    "", "FR", "medium")

add("FR-SCH-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "scheduling_general", "II_-10",
    "Category II (-10): broadcast timing is left to the EDITOR'S DISCRETION, but such programmes MAY NOT BE PLACED WITHIN PROGRAMMES INTENDED FOR CHILDREN.",
    "No clock restriction; placement restriction only.", "none;not_within=children_programmes",
    "Particular care required for trailers scheduled near children's programmes.",
    "conditional", "clear",
    "Note there is NO time restriction for -10 - only a placement restriction. A model that assumes every age label implies an hour will invent one.",
    "no", "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-SCH-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "III_-12",
    "Category III (-12) on services OTHER THAN cinema channels and pay-per-view: must not be broadcast BEFORE 22:00.",
    "Not before 22:00.", "not_before=22:00",
    "Subject to the exceptional derogation in FR-SCH-004. Cited against the CURRENT consolidated French text, not the 2005 JORF original: the hours happen to be unchanged since 2005, which is precisely why the amended art. 2 definition slipped past review (C-09).",
    "bright_line", "clear", C02, "no",
    "FR-R1 (as amd. FR-A2)", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
    "Pour les autres services de television, ces programmes ne doivent pas etre diffuses "
    "avant 22 heures.", "FR", "high")

add("FR-SCH-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "scheduling_general", "III_-12",
    "Category III (-12) on CINEMA CHANNELS and PAY-PER-VIEW services: must not be broadcast ON WEDNESDAYS BEFORE 20:30.",
    "Not Wednesdays before 20:30.", "not_before=20:30;days=Wed",
    "A day-of-week-specific rule. Historically tied to the French school week.",
    "bright_line", "clear", C02, "no",
    "FR-R1 (as amd. FR-A2)", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
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
    "yes", "FR-R1 (as amd. FR-A2)", "art. 3", U_FR1C, "2014-04-09", "open", "approved",
    "Ces diffusions exceptionnelles ne peuvent exceder seize programmes par an, dont au "
    "maximum quatre oeuvres cinematographiques interdites en salles aux mineurs de 12 ans", "FR", "high")

add("FR-SCH-005", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "IV_-16",
    "Category IV (-16) on services OTHER THAN cinema channels and pay-per-view: reserved for a warned audience; may only be broadcast AFTER 22:30.",
    "After 22:30.", "not_before=22:30",
    "No derogation equivalent to FR-SCH-004 is provided for category IV.",
    "bright_line", "clear",
    "Corroborated by the Arcom public summary ('as of 10:30 pm'), the French government page, and multiple parliamentary answers - so this row is better evidenced than the cat. III rows.",
    "no", "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "apres 22h30 sur les chaines autres que cinema", "FR", "high")

add("FR-SCH-006", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "scheduling_general", "IV_-16",
    "Category IV (-16) on CINEMA CHANNELS and PAY-PER-VIEW services: reserved for a warned audience; may be broadcast AFTER 20:30.",
    "After 20:30.", "not_before=20:30",
    "Two hours earlier than on other services - a pure service-type effect with identical content.",
    "bright_line", "clear",
    "Excellent demonstration that the age label alone does not determine the hour.", "no",
    "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "apres 20h30 sur les chaines cinema", "FR", "high")

add("FR-SCH-007", "FR", "Arcom", "regulator_binding", 2, "pointer",
    "all_linear_tv", "scheduling_general", "V_-18",
    "Category V (-18): broadcast is governed ENTIRELY by Recommandation n. 2004-7 of 15 December 2004.",
    "See FR-CV-002.", "see=FR-CV-002",
    "art. 3 of FR-R1 delegates completely; the -18 hours are NOT stated in FR-R1.",
    "bright_line", "clear",
    "A model asked for -18 hours must follow this pointer. Answering by analogy with -16 ('later than 22:30') is wrong.",
    "no", "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-PRO-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "human_dignity", "prohibited",
    "Programmes which OFFEND HUMAN DIGNITY - in particular those depicting SEXUAL VIOLENCE, PERVERSIONS OR DEGRADATION - are banned from broadcast.",
    "No permitted time.", "prohibited",
    "None. No category, service type, hour or technical measure unlocks this.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-PRO-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "sexual_content", "prohibited",
    "PORNOGRAPHIC programmes DEPICTING UNDER-18s are banned from broadcast.",
    "No permitted time.", "prohibited", "None.",
    "bright_line", "clear", "Hard pre-check in code.", "no",
    "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-PRO-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "violence", "prohibited",
    "Programmes of EXTREME OR GRATUITOUS VIOLENCE are banned from broadcast.",
    "No permitted time.", "prohibited",
    "None. Distinguish from category V 'very great violence', which IS broadcastable within 00:00-05:00 on eligible services.",
    "bright_line", "clear",
    "The boundary between 'very great violence' (cat. V, schedulable) and 'extreme or gratuitous violence' (banned) is a genuine judgment line and a likely source of disagreement. Flag near-threshold cases.",
    "yes", "FR-R1 (as amd. FR-A2)", "art. 3", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-SIG-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "The PICTOGRAM must remain on screen FOR THE WHOLE DURATION of the programme (categories II-V under the 2014 text).",
    "n/a - display obligation", "n/a",
    "Under the original 2005 text category II was 5 minutes at the start; 2012-57 and 2014-17 changed this.",
    "bright_line", "clear",
    "Signage is a SEPARATE obligation from scheduling: a programme can be correctly scheduled and still breach by failing to display the pictogram. The C8 enforcement decision was precisely about signage.",
    "no", "FR-R1 (as amd. FR-A1, FR-A2)", "art. 4", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-SIG-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "A WRITTEN MENTION must also appear, either at the bottom of the screen in white for AT LEAST 1 MINUTE at the start, OR full-screen before the programme for AT LEAST 12 SECONDS. Wording: II 'deconseille aux moins de dix ans'; III 'aux moins de douze ans'; IV 'aux moins de seize ans'; V 'aux moins de dix-huit ans' (or the assigned cinema-ban wording).",
    "n/a - display obligation", "n/a",
    "Decret n. 90-174 on prior public warnings continues to apply.",
    "bright_line", "clear", "", "no",
    "FR-R1 (as amd. FR-A1, FR-A2)", "art. 4", U_FR2, "2012-11-20", "open", "approved",
    "", "FR", "high")

add("FR-SIG-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "signage", "II_to_V",
    "The classification must be made known to the public AT THE TIME OF BROADCAST, in TRAILERS, and in PROGRAMME SCHEDULES communicated to the press.",
    "n/a - information obligation", "n/a", "",
    "bright_line", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 4", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-TRL-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "II_to_V",
    "Trailers must display the PICTOGRAM OF THE PROGRAMME'S CATEGORY THROUGHOUT the trailer, and must NOT contain scenes likely to offend young viewers.",
    "n/a - content and display obligation", "n/a", "",
    "bright_line", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-TRL-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "III_-12",
    "Category III (-12) trailers MAY NOT AIR CLOSE TO CHILDREN'S PROGRAMMES. Category II trailers near children's programmes require particular care.",
    "Placement restriction.", "not_near=children_programmes", "",
    "bright_line", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-TRL-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv", "trailers", "IV_-16",
    "Category IV (-16) trailers MAY NOT AIR BEFORE 20:30.",
    "Not before 20:30.", "not_before=20:30",
    "Note the trailer time (20:30) differs from the programme time on non-cinema channels (22:30).",
    "bright_line", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-MUS-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "exempt",
    "Music videos (videomusiques) are EXEMPT FROM SYSTEMATIC SIGNAGE.",
    "n/a", "exempt=systematic_signage",
    "A deliberate special regime, not an oversight.",
    "bright_line", "clear",
    "Contrast with the UK, which applies the ordinary watershed plus detailed content thresholds to music videos. The SAME music video can yield a hard UK verdict and a soft French one.",
    "no", "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-MUS-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "soft_restriction",
    "Music videos likely to offend young viewers SHOULD PREFERABLY be broadcast AFTER 22:00.",
    "Soft preference for after 22:00 - NOT an absolute prohibition.",
    "soft_prefer_not_before=22:00",
    "The wording is a preference ('de preference'), not a prohibition. Do not output this as a hard limit.",
    "judgment_based", "clear",
    "A key precision test: a model that renders this as 'prohibited before 22:00' is OVER-rating and misstating the legal force of the rule. Worth an explicit test case.",
    "yes", "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-MUS-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "all_linear_tv; music_channels", "music_videos", "context_dependent",
    "Programmes containing music videos whose THEMES ARE NOT AIMED AT CHILDREN OR TEENAGERS should nonetheless carry a WARNING.",
    "n/a - information duty", "n/a;requires=warning", "",
    "judgment_based", "clear", "", "no",
    "FR-R1 (as amd. FR-A2)", "art. 5", U_FR2, "2014-04-09", "open", "approved",
    "", "FR", "high")

add("FR-CV-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; high_production_commitment_channels; pay_per_view",
    "classification_scheme", "V_-18",
    "ELIGIBILITY GATE: only services with special access conditions may broadcast category V - 'cinema' channels, services with a high production-contribution commitment equivalent to cinema channels, or pay-per-view services - and only where access is limited so that under-18s cannot reach the content. Requests are EXAMINED INDIVIDUALLY by the regulator.",
    "Eligibility precondition, not a time rule.", "gate=service_eligibility",
    "On all other channels category V is TOTALLY PROHIBITED (see FR-CV-003).",
    "conditional", "unverified", C03, "yes",
    "FR-R2", "2004-7 I.A", U_FRV, "2004-12-23", "unknown", "unverified",
    "", "FR", "medium")

add("FR-CV-002", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; high_production_commitment_channels; pay_per_view",
    "scheduling_general", "V_-18",
    "Category V (-18) programmes may be broadcast only BETWEEN 00:00 (MIDNIGHT) AND 05:00.",
    "Closed window 00:00-05:00.", "window=00:00-05:00",
    "Conditional on the FR-CV-001 eligibility gate being satisfied first, plus locking (FR-CV-004) and signage.",
    "bright_line", "unverified",
    C03 + " Corroborated by the Arcom public summary page ('between midnight and 5 a.m.'), which raises confidence in the figure even though the source text's currency is unconfirmed.",
    "yes", "FR-R2", "2004-7", U_FRV, "2004-12-23", "unknown", "unverified",
    "Between midnight and 5am", "EN", "medium")

add("FR-CV-003", "FR", "Arcom", "regulator_binding", 2, "yes",
    "free_to_air; other_than_cinema_channels", "scheduling_general", "V_-18",
    "On services that are NOT eligible under FR-CV-001, category V programmes are subject to a TOTAL PROHIBITION ON BROADCAST.",
    "No permitted time on non-eligible services.", "prohibited",
    "None.",
    "bright_line", "unverified", C03, "yes",
    "FR-R2 + FR-S2", "2004-7 I.A", U_FRV, "2004-12-23", "unknown", "unverified",
    "Sauf sur les chaines autorisees, ces programmes font l'objet d'une interdiction totale de diffusion.",
    "FR", "medium")

add("FR-CV-004", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "access_control", "V_-18",
    "DIGITAL LOCKING: category V must be locked at the DECODER level requiring a personal code, with an on-screen lock message. The lock must reactivate when the broadcast context changes and stay synchronised with the programme. The code must be at least FOUR DIGITS, not 0000, hidden when entered, used only for this purpose, and IMPOSSIBLE FOR SUBSCRIBERS TO DISABLE.",
    "n/a - access-control obligation", "requires=decoder_lock",
    "Analogue services: from 1 Jan 2006 received WITHOUT access unless the subscriber opts in in writing.",
    "bright_line", "unverified", C03, "yes",
    "FR-R2", "2004-7 I.B", U_FRV, "2004-12-23", "unknown", "unverified",
    "This program is locked because it is harmful to persons under 18", "EN", "medium")

add("FR-CV-005", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "pay_tv_bundles", "commercial_conditions", "V_-18",
    "QUANTITY LIMITS: the regulator caps the number of category V broadcasts in each service's CONVENTION. Separately, if a non-pay-per-view bundle includes services showing MORE THAN 208 category V programmes per year (about 4 per week), the offer must also be available WITHOUT those services, on terms that do not favour the bundle.",
    "n/a - bundle composition rule", "n/a",
    "A channel/distributor-level obligation.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Not answerable from a single asset description. Must not be attempted by a per-asset prompt. " + C03,
    "yes", "FR-R2", "2004-7 I.C", U_FRV, "2004-12-23", "unknown", "unverified",
    "", "FR", "medium")

add("FR-CV-006", "FR", "Arcom", "regulator_binding", 2, "no_out_of_scope",
    "pay_tv_bundles", "commercial_conditions", "V_-18",
    "MARKETING CONDITIONS: category V content may not be included in promotional offers aimed at people without a qualifying subscription; pay-per-view category V may only be sold INDIVIDUALLY; opt-in offers may not be priced more favourably than versions without category V content.",
    "n/a - commercial rule", "n/a", "Distributor-level.",
    "bright_line", "out_of_scope_for_asset_decision",
    "Recorded for completeness only. " + C03, "yes",
    "FR-R2", "2004-7 I.C/D", U_FRV, "2004-12-23", "unknown", "unverified",
    "", "FR", "medium")

add("FR-CV-007", "FR", "Arcom", "regulator_binding", 2, "yes",
    "cinema_channels; pay_per_view", "signage", "V_-18",
    "Broadcasts of category V must display the -18 rating AND a WARNING about harm to minors and the legal sanctions under ARTICLE 227-22 of the French Penal Code. Distributors/publishers must regularly remind subscribers how the lock works; contracts must include this information; annual implementation reports go to the regulator.",
    "n/a - display and information obligation", "requires=on_screen_warning",
    "The penal-code warning is specific to category V.",
    "bright_line", "unverified", C03, "yes",
    "FR-R2", "2004-7", U_FRV, "2004-12-23", "unknown", "unverified",
    "", "FR", "medium")

add("FR-CNV-001", "FR", "Arcom", "regulator_binding", 2, "yes",
    "per_channel", "channel_override", "n/a",
    "CHANNEL CONVENTIONS: every conventionnee channel signs an individual convention with Arcom containing its own protection-of-minors articles, which CAN BE STRICTER than the general recommendation. Enforcement cites the convention alongside the recommendation (e.g. the C8 decision cites convention arts. 2-3-7, 2-4, 4-2-1 with reco. 2005-5 arts. 2 and 4).",
    "Channel-specific; may tighten any rule above.", "override=channel_specific",
    "Parliamentary material notes conventions have LOWERED the category III limit to 22:00 'or less, with permanent signage' for particular channels.",
    "conditional", "out_of_scope_for_asset_decision",
    "NOT COLLECTED IN v1 (C-06). There is no consolidated document containing all applicable French rules for a given broadcast: the set is statute + reco. 2005-5 as amended + (for -18) reco. 2004-7 + THAT CHANNEL'S convention. For Task 2 this is a per-licensee data source that cannot be scraped generically and needs a local expert.",
    "yes", "FR-V1", "per-channel convention", U_CONV, "", "open", "draft",
    "", "FR", "low")

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
    "", "EN", "high")

add("EU-FRM-003", "EU", "EU / ERGA", "statute", 1, "no_out_of_scope",
    "all_avms", "data_protection", "n/a",
    "Personal data of minors collected or generated pursuant to art. 6a(1) must not be processed for commercial purposes such as direct marketing, profiling or behaviourally targeted advertising.",
    "n/a", "n/a", "",
    "bright_line", "out_of_scope_for_asset_decision",
    "Not a content or scheduling rule. Recorded so the scope boundary is explicit.", "no",
    "EU-D1", "AVMSD art. 6a(2)", U_EU, "2018-12-18", "open", "approved",
    "", "EN", "high")

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
    ["rule_id", "Stable identifier. Format: (UK|FR|EU)-[A-Z]{2,4}-nnn.", "Cite this in prompt output so every decision is traceable to a row. Mnemonics: SCH scheduling, VIO violence, SEX sexual content, NUD nudity, LNG language, DRG drugs, IMI imitable behaviour, SUI suicide/self-harm, FLM film carry-over, MUS music videos, TRL trailers, SIG signage, CLS classification scheme, CV category V regime, PRO absolute prohibition, GEN general duty, DEF definition, LAW legal basis, SVC service scope, CNV channel convention, OCC occult, WEL participant welfare, OFF offence, FRM framework."],
    ["country", "Jurisdiction.", "UK / FR / EU"],
    ["regulator", "Body that issued the text.", "Ofcom / Arcom / Parliament / EU-ERGA"],
    ["source_type", "Nature of the source.", "statute / regulator_binding / regulator_guidance / precedent / regulator_summary / classification_body / secondary"],
    ["authority_rank", "Conflict resolution. LOWER WINS.", "1 statute, 2 regulator_binding, 3 guidance, 4 precedent, 5 regulator_summary, 6 classification_body, 7 secondary"],
    ["use_for_decision", "Whether a per-asset decision may rely on this row.", "yes / definition_only / framework_only / pointer / scope_rule / no_out_of_scope"],
    ["service_type", "Which services the rule binds. SEMICOLON-SEPARATED.", "free_to_air, cinema_channels, pay_per_view, premium_subscription_film, other_than_cinema_channels, music_channels, bbc_odps, all_linear_tv, per_channel, pay_tv_bundles, all_avms"],
    ["content_category", "Shared harm vocabulary across countries. THIS IS THE JOIN KEY to the content-extraction stage.", "violence, sexual_content, nudity, drugs_alcohol_smoking, strong_language, fear_distress, suicide_self_harm, imitable_behaviour, human_dignity, occult_paranormal, music_videos, trailers, film_carryover, signage, access_control, scheduling_general, classification_scheme, serious_harm, offence_general, participant_welfare, commercial_conditions, data_protection, legal_basis, definition, scope"],
    ["classification", "The age label or UK equivalent.", "FR: I_tous_publics, II_-10, III_-12, IV_-16, V_-18. UK: context_dependent, watershed_bound, prohibited, any_time_with_protection, restricted_window. Also: category_independent, exempt, soft_restriction, n/a"],
    ["threshold_description", "What the rule actually says, in structured prose.", "Free text. Capitals mark the operative words."],
    ["time_restriction_text", "The time effect in words.", "Free text."],
    ["time_rule_machine", "The time effect in a parseable form, for code. Semicolon-separated tokens.", "none | prohibited | any_time | n/a | not_before=HH:MM | window=HH:MM-HH:MM | restricted_window=HH:MM-HH:MM | soft_prefer_not_before=HH:MM | not_within=... | not_near=... | prohibited_in=... | days=... | except_days=... | unless=... | requires=... | gate=... | override=... | annual_quota=... | sub_quota=... | standard=... | frequency_cap=... | exempt=... | see=RULE_ID | judgment:... | framework:..."],
    ["exceptions_conditions", "Carve-outs, gates and inputs the rule depends on.", "Free text."],
    ["determinacy", "PROPERTY OF THE RULE. Governs how the test set is scored.", "bright_line = one correct answer, exact match required. conditional = bright line gated on an input; a correct missing-information request also passes. judgment_based = evaluative; score the reasoning and cited rule, accept a band, require escalation near thresholds."],
    ["ambiguity_flag", "PROPERTY OF OUR EXTRACTION. Do NOT merge with determinacy.", "clear / conflicting_sources / translation_uncertain / unverified / out_of_scope_for_asset_decision"],
    ["ambiguity_note", "What is uncertain and how it was resolved.", "Free text. Carries the C-0n conflict IDs."],
    ["human_review_required", "Escalate before relying on this row.", "yes / no"],
    ["source_doc", "Source ID from the Sources tab.", "e.g. UK-S1, FR-R1, EU-D1"],
    ["clause_ref", "Clause within the source.", "e.g. Rule 1.4, art. 3, AVMSD art. 6a(1)"],
    ["source_url", "Canonical URL (hyperlinked).", "For a row stating CURRENT law this is the CURRENT CONSOLIDATED text. The JORF/original-publication URL is cited only on superseded rows (9xx), where it is the correct source. Citing an original for current law is a provenance bug: it reads as authoritative while silently omitting later amendments."],
    ["valid_from", "Date the provision took effect.", "ISO date, or blank if undated guidance"],
    ["valid_to", "End of validity.", "open / unknown / ISO date"],
    ["status", "Fitness as ground truth.", "approved = usable. draft = do not use until the conflict is resolved. unverified = currency unconfirmed. superseded = historical, retained for versioning. NAMING: a rule_id in the 9xx range is a superseded version of the matching 0xx rule (FR-CLS-903 is the pre-2014 wording of FR-CLS-003)."],
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
    ["Before using as ground truth", "Filter status = approved. Rows marked draft or unverified have open conflicts (see Open_Questions) and must be resolved first. Currently 74 of 83 rows are approved. The remaining: all FR category V rows are unverified (C-03), FR-CNV-001 is draft (channel conventions not collected, C-06), and FR-CLS-903 is a deliberately retained superseded row."],
    ["Avoiding correlated error", "The biggest risk is that this table and the prompt share an author and therefore share mistakes - the exact failure Task 2 asks about. Mitigation: the bright-line rows (times, absolute prohibitions) should be INDEPENDENTLY RE-DERIVED from primary sources by a second pass that has not seen this table, then compared. verbatim_quote and source_url let a reviewer check a row without reading the prompt at all."],
    ["Versioning", "Never delete a row. When a source is replaced, set valid_to and status = superseded on the old row and add a new row. That preserves the ability to say which rule version produced a past decision."],
    ["Required inputs the rules imply", "country; service_type (free-to-air vs cinema channel vs pay-per-view vs premium subscription film); access measures in place (none / mandatory_daytime_protection / mandatory_restricted_access / decoder_lock); intended broadcast DATE and time (France has day-of-week and school-holiday rules); whether the asset is a theatrical film and its existing BBFC/CNC classification; whether it is a trailer or a music video. If any of these is missing and a candidate rule depends on it, the correct output is a missing-information flag, NOT an assumption."],
    ["Known hard pre-checks", "Absolute prohibitions should be enforced in CODE, not left to prompt reasoning: UK-GEN-001 (seriously impair), UK-SEX-001 (R18-equivalent), UK-FLM-001 (refused classification), UK-FLM-006 (R18 films), FR-LAW-001 (nuire gravement), FR-PRO-001/002/003 (human dignity, child pornography, extreme violence). No contextual argument or access measure should be able to override these."],
    ["What is NOT in v1", "French channel conventions (C-06); Ofcom Guidance Notes for Sections One and Two; systematic Ofcom enforcement precedent; BBFC classification guidelines; overseas France. See 99_EXTRACTION_NOTES_AND_LIMITS."],
]
sheet("How_to_use", howto, [30, 130], 22)

# ---- Sources tab
src = [["source_id", "document", "regulator", "source_type", "authority_rank",
        "scope / applicability", "url", "date / version", "notes"]]
src += [
    ["UK-S1", "Ofcom Broadcasting Code, Section One: Protecting the Under-Eighteens", "Ofcom", "regulator_binding", 2,
     "All Ofcom-licensed TV and radio. Rules 1.3-1.6 do NOT apply to BBC ODPS.", U_S1,
     "Published 2021-03-03, last updated 2023-03-16", "The core UK rulebook. Must be read with Section Two."],
    ["UK-S2", "Ofcom Broadcasting Code, Section Two: Harm and Offence", "Ofcom", "regulator_binding", 2,
     "Same as UK-S1.", U_S2, "Published 2021-03-03, last updated 2024-02-19",
     "Supplies the BINDING DEFINITION OF 'CONTEXT', on which Section One depends. Time of broadcast is one of its eight factors."],
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
     "CLOSED 2026-11-06. FR-CLS-003 now carries the current wording. The pre-2014 wording is retained as FR-CLS-903, status=superseded, valid_to=2014-04-08.",
     "None for the rule itself. The lesson matters more: the error survived because the English translation and the pre-2014 French text AGREED with each other, so cross-source corroboration did not catch it - only reading the amending instrument did. Treat any source whose amendment history is not explicit as suspect, and always diff the amending deliberation rather than trusting a page labelled 'consolidated'.",
     "closed", "no"],
    ["C-10", "Arcom's own FRENCH public page (FR-S1c) states the category III (-12) test as 'recourt de facon repetee a la violence physique ou psychologique, OU EVOQUE LA SEXUALITE ADULTE'. That adult-sexuality limb does not appear in the binding art. 2 wording we hold (as replaced by delib. 2014-17).",
     "FR-CLS-003",
     "None yet. Found 2026-11-06 while searching for the Legifrance id of delib. 2014-17.",
     "CLOSED 2026-11-06. The French primary text was downloaded and searched: 'sexualite' does not occur anywhere in the binding recommendation. The limb is a PRACTICE GLOSS on Arcom's public page, not binding text. The binding -12 trigger is repeated violence. Arcom may still apply the gloss when it classifies, so borderline sexual-content cases should be flagged for review rather than cleared - but the rule table should not encode an independent adult-sexuality trigger.",
     "closed", "no"],
    ["C-03", "Recommandation 2004-7 - the sole source of the French -18 hours - dates from 2004 with compliance deadlines of 2005/2006/2008, all elapsed. The CSA->Arcom transition (2022) and the 2021 AVMSD transposition decree both postdate it.",
     "FR-CV-001 to FR-CV-007",
     "Still open. All category V rows remain unverified. Attempted 2026-11-06: the Arcom page for reco. 2004-7 was fetched but returned 12,493 characters of pure site NAVIGATION and no rule text - it renders its body via JavaScript. The fetcher now detects this (per-document `expect` assertion) instead of storing the shell as a source copy.",
     "Obtain the real text: use the page's Telecharger/Imprimer PDF, or the JORF of 23 December 2004, and set format=pdf in the manifest. Then confirm (a) that the 00:00-05:00 window is still in force, and (b) whether the 2021 AVMSD transposition decree altered the category V regime. This is now the main blocker on the French side.",
     "local expert", "YES"],
    ["C-04", "No verbatim source text could be captured. The execution environment has no outbound access to ofcom.org.uk / arcom.fr / legifrance.gouv.fr (egress proxy refuses: connect_rejected), and the available web-fetch path returns model-written summaries, declining full reproduction.",
     "ALL rows (verbatim_quote column)",
     "Documented. Canonical URLs recorded on every row so authoritative wording can be checked by hand.",
     "Obtain the official PDFs (allowlisted direct fetch, or manual deposit into the Drive source folder), then add the quote-integrity check: every row's verbatim_quote must be programmatically confirmed to appear in the stored source file. Without that control, extraction errors are silent.",
     "engineering", "partially - limits automated verification"],
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
    ["C-07", "Ofcom enforcement precedent is represented by a single example. Precedent is the ONLY source of applied thresholds, which is exactly what the judgment_based rows lack.",
     "all UK judgment_based rows",
     "One example recorded (UK-P1).",
     "Ingest the Ofcom bulletins systematically and attach decided cases to the judgment_based rows as calibration anchors.",
     "engineering", "no - but caps achievable accuracy on judgment rows"],
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

# Diffable CSV mirrors, one per tab. These are what make a rule change reviewable
# in a pull request; the workbook itself is a binary blob git cannot diff.
_CSV_DIR = _RULES_DIR / "csv"
_CSV_DIR.mkdir(exist_ok=True)
for _name in wb.sheetnames:
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
