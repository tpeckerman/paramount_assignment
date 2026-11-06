# FR-R2 — Recommandation n° 2004-7 du 15 décembre 2004 — Category V (-18) programmes

- **Regulator:** CSA (now Arcom)
- **Source type:** regulator_binding (authority rank 2)
- **URL:** https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france
- **Published:** JORF, 23 December 2004
- **Scope:** Mainland France and overseas départements. Editors **and distributors** of TV services
  broadcasting category V (-18) programmes.
- **Supersedes:** the CSA recommendation of 21 October 2003 (repealed by this one)
- **Litigation:** upheld by the Conseil d'État, 17 May 2006, nos. 263081 / 277711 (Association Comité
  Télévision et Libertés) — https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2006-05-17/263081
- **Related:** Recommandation du 26 juillet 2005 (overseas France)
- **Retrieval status:** STRUCTURED EXTRACT. **Flagged `unverified` — see currency warning below.**

> Article 3 of FR-R1 defers **entirely** to this text for category V. It is therefore the *only* source of
> the French -18 broadcast hours.

---

## Eligible services

Only services with **special access conditions** may broadcast category V programmes. Requests are
**examined individually** by the regulator. Eligible types:
- **"Cinema" channels** (*chaînes cinéma*);
- services with a **high production-contribution commitment** equivalent to cinema channels;
- **pay-per-view** services,
provided they guarantee that access is **limited so that under-18s cannot reach the content**.

→ On all other channels, category V is **totally prohibited**.

## Permitted broadcast hours

**Between 00:00 (midnight) and 05:00.**

> This is a **closed window**, structurally different from the UK watershed (an open-ended period from
> 21:00 to 05:30). Note also it is **narrower** than the French -16 rule (after 22:30) by two and a half
> hours, and that it is **not** derivable from the -18 label alone — the hours come from this separate text.

## Quantity limits

- The regulator **caps the number of category V broadcasts in each service's convention** (agreement).
- Separately, if a **non-pay-per-view bundle** includes services showing **more than 208 category V
  programmes per year** (≈ 4 per week), the offer **must also be available without those services**, on
  terms that do not favour the bundle.

## Locking / parental-control requirements

### Digital services
Category V programmes must be **locked at the decoder level**, requiring a **personal code**, displaying the
message *"This programme is locked because it is harmful to persons under 18"*. Requirements:
- the lock must **reactivate when the broadcast context changes**;
- it must stay **synchronised with the programme**;
- the code must be **at least four digits** and **not 0000**;
- it must be **hidden on screen** when entered;
- it must be **used only for this purpose**;
- it must be **impossible for subscribers to disable**.

Individual criteria carried compliance deadlines of 1 January **2005**, **2006** and **2008**.

### Analogue services
From **1 January 2006**, these services are received **without access** to category V programmes
**unless the subscriber opts in in writing**.

### Transitional digital rule
Until **1 January 2008**, non-pay-per-view category V services were received without access unless the
subscriber opted in in writing (choice to be made by 1 January 2006). Distributors could be exempted by
declaring all their terminals met the locking criteria, with the regulator able to revoke the exemption
after testing.

## Marketing and subscription conditions

- Category V content **may not be included in promotional offers** aimed at people without a subscription
  granting access to it.
- Pay-per-view category V programmes **may only be sold individually**.
- Opt-in offers **may not be priced more favourably** than versions without category V content.

## Information duties

- Distributors and publishers must **regularly remind subscribers** how the lock works and of the need for a
  confidential code; **contracts must include this information**.
- Broadcasts must display the **-18 rating** and a **warning** about harm to minors and the legal sanctions
  under **article 227-22 of the French Penal Code**.
- **Annual implementation reports** must be submitted to the regulator.

---

## ⚠ Currency warning (conflict C-03)

This text dates from **2004** and its internal deadlines (2005 / 2006 / 2008) have all long elapsed. It has
**not been confirmed** whether it remains in force unamended, or has been modified or replaced — in
particular given:
- the 2022 replacement of the CSA by Arcom;
- the 2018 revision of the AVMSD and its 2021 French transposition (Décret du 4 février 2021 on audiovisual
  media services), which introduced **content descriptors** alongside age signage.

**All rows derived from this document are marked `status = unverified` and
`human_review_required = yes`.** They must be checked against the current Arcom legal register before being
used as ground truth.

---

## Design implications

1. **The -18 hours (00:00–05:00) must be sourced from here, not inferred.** A model asked "what hours for
   -18 in France?" that answers "after 22:30, like -16, but later" or "after the watershed" is wrong.
   Good adversarial test case.
2. **Eligibility is a gate before the hours.** The correct decision order for French -18 content is:
   *(a)* is the service eligible at all? If not → **total prohibition**, and the hours are irrelevant.
   *(b)* if eligible → 00:00–05:00 **plus** locking **plus** signage **plus** warning.
   A prompt that outputs hours without first checking service eligibility will produce a dangerous answer
   for a free-to-air channel.
3. **Several obligations here are not per-programme at all** (bundle composition, pricing, contracts, annual
   reports, per-convention caps). These belong in the rule table for completeness but should be marked
   as **out of scope for a per-asset rating decision** — otherwise the prompt will try to answer questions
   it has no data for.
