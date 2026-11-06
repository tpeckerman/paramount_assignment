# FR-L1 / FR-C1 / FR-V1 — French legal basis, channel conventions, and the CNC's actual role

- **Retrieval status:** STRUCTURED EXTRACT.

---

## FR-L1 — Loi n° 86-1067 du 30 septembre 1986 (liberté de communication)

- **Source type:** statute (authority rank 1)
- **URL:** https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205

### Article 1
Guarantees freedom of audiovisual communication; its exercise may be limited only on the grounds the
article enumerates, **among which is the protection of childhood and adolescence**
(*la protection de l'enfance et de l'adolescence*).

### Article 15 — the operative statutory duty
Arcom (formerly the CSA) must ensure:
1. **the protection of childhood and adolescence and respect for human dignity** in programmes made
   available to the public by an audiovisual communication service;
2. that **no programme liable to seriously harm** the physical, mental or moral development of minors is
   made available by radio or television services;
3. that programmes **liable to harm** the physical, mental or moral development of minors are **not made
   available** by a broadcasting service **unless it is ensured — by the choice of the broadcast time and
   by any appropriate technical process — that minors are not normally liable to see or hear them**;
4. that programmes contain **no incitement to hatred or violence** on grounds of race, sex, religion or
   nationality.

> **Point 3 is the statutory hook for the whole French time-restriction system**, and note the structure:
> *choice of broadcast time* **or/and** *appropriate technical process*. It mirrors AVMSD art. 6a(1).
> This is the statutory reason France ended up with both fixed hours **and** the category V locking regime.

### Note on the two-tier harm standard
French law (following the directive) distinguishes:
- **"seriously harm"** (*nuire gravement*) → **absolute prohibition**, no time or technical measure cures it;
- **"harm"** (*nuire*) → permitted **if** time and/or technical measures keep minors away.

**This two-tier structure must be represented in the rule table.** It is the French analogue of Ofcom
Rule 1.1 (absolute) vs Rules 1.3–1.4 (schedulable), and it is the correct place to encode the
"offends human dignity / extreme violence / child pornography" absolute bans from FR-R1 art. 3.

---

## FR-V1 — Channel conventions (*conventions*)

- **Source type:** regulator_binding (authority rank 2), **channel-specific**
- **Example:** Arcom mise en demeure concerning C8 — https://www.arcom.fr/sites/default/files/2023-05/MeD_C8.pdf

Every *conventionnée* channel signs an individual **convention** with Arcom. These contain their own
protection-of-minors articles. The C8 decision cites the channel's convention of 29 May 2019
(**arts. 2-3-7, 2-4, 4-2-1**) **alongside** recommendation 2005-5 (arts. 2 and 4) and the deliberation of
17 April 2007 (participation of minors).

### Why this matters for the architecture
1. **A channel's convention can be stricter than the general recommendation.** Parliamentary material notes
   that conventions established by the CSA have *lowered* the category III limit to 22:00 "or less, with
   permanent signage" for particular channels — i.e. the convention is where per-channel variation lives.
2. **There is no single consolidated document that contains all applicable French rules for a given
   broadcast.** The applicable set is: statute (art. 15) + recommendation 2005-5 as amended + (for -18)
   recommendation 2004-7 + **that channel's convention**.
3. **Consequence for the rule table:** a `channel_specific_override` concept is required. For Task 1 the
   table covers the general regime and flags that convention-level rules exist and are not included.
   For Task 2, conventions are a per-country, per-channel data source that **cannot be scraped generically** —
   it is a strong example of where a local expert / licensee-level data feed is needed.

---

## FR-C1 — CNC and the Commission de classification des œuvres cinématographiques

- **Source type:** classification_body (authority rank 6) — **not a television regulator**
- **URL:** https://www.cnc.fr/cinema/actualites/proteger-sans-censurer--la-classification-des-oeuvres-cinematographiques_1924881
- **Activity page:** https://www.cnc.fr/professionnels/visas-et-classification/activite-de-la-commission-de-classification

### Scope — explicitly limited
The CNC states that the Commission's role is **limited to the classification of films exploited in cinemas**.
It is **competent neither for television, DVD, VOD, video games nor the internet.**

### The classification measures (cinema *visa d'exploitation*)
Granted by the Minister of Culture on the Commission's opinion:
- visa authorising representation **for all audiences**;
- visa with **prohibition for under-12s**;
- visa with **prohibition for under-16s**;
- visa with **prohibition for under-18s**, without listing as pornographic/inciting violence;
- visa with **prohibition for under-18s with listing** on the pornographic / incitement-to-violence
  ("X") list (art. 12 of the law of 30 December 1975).
A film may also be classified with a **reasoned warning** (*avertissement*) where particular scenes are
sensitive.

Films may also be **refused a visa** entirely, though the CNC notes the last refusal was in 1979.

### How it actually enters the TV decision
- It does **not** supply the TV category.
- It is an **input** to FR-R1 art. 2: the cinema classification *may serve as an indication*, the editor must
  check it transfers safely, and **may strengthen it**.
- FR-R1 art. 2 categories III, IV and V each explicitly include *"œuvres cinématographiques interdites aux
  mineurs de 12 / 16 / 18 ans"* — so a cinema interdiction **pulls a film into at least that category**.
- A film carrying a CNC **avertissement** is, per CSA practice, classified **-12** for television.
- The 20-year reclassification route (FR-R1 art. 2) is the only channel by which the Commission revisits a
  classification *for television purposes*, and only on joint editor/producer request via Arcom.

### Scope ruling for this project
**Out of scope as a rule source. In scope as an optional input field.**
The prompt should accept an optional `existing_theatrical_classification` (BBFC rating / CNC visa).
If the content is a **theatrical film** and that field is **empty**, the correct output is a
**missing-information flag**, because both countries' frameworks refer to it.
If the content is not a film (music video, short, trailer, studio programme), the field is irrelevant and
must not be requested.

### Also out of scope: streaming / on-demand
A film on a streaming app (e.g. a Paramount-branded app) is a **non-linear** service. It is governed in
France by **Délibération n° 2011-64 du 20 décembre 2011** (SMAD), **not** by FR-R1, and not by the CNC.
The 2011 text reuses the same five categories but with **different conditions** — e.g. category IV content
that is not behind payment is accessible only **22:30–05:00**. This is a useful contrast for Task 2 and a
further demonstration that **the same category maps to different hours on different service types.**
