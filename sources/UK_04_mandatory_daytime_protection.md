# UK-M1 — Ofcom: Mandatory Daytime Protection (MDP) regime

- **Regulator:** Ofcom
- **Source type:** regulator_binding (authority rank 2) — statement amending the Code
- **URL:** https://www.ofcom.org.uk/__data/assets/pdf_file/0025/125359/statement-mandatory-daytime-protection-rules.pdf
- **Publication date:** 5 November 2018 · **Code changes effective:** 1 January 2019
- **Related call for inputs:** https://www.ofcom.org.uk/siteassets/resources/documents/consultations/uncategorised/7803-mandatory-daytime-pin-protections/summary/pin_call_for_inputs.pdf
- **Retrieval status:** STRUCTURED EXTRACT.

> **Why this is decisive for the assignment.** MDP is the clearest proof in the UK framework that
> *a content rating does not determine broadcast hours.* The **same BBFC 18 film** may be barred before
> 21:00 on one service and permitted **at any hour** on another, purely because of a technical access
> measure. Any solution that maps rating → hours will fail on this.

---

## Definition

**"Mandatory daytime protection" means there is a PIN protection system in place pre-2100 and post-0530.**

Characteristics:
- The PIN **cannot be removed or disabled by the user**.
- It restricts access to authorised viewers only.
- The PIN must be **required each time** the viewer enters protected content.
- Broadcasters must supply **accurate metadata** for the system to work.
- **Adult sex material is excluded** from MDP and remains confined to 22:00–05:30 behind
  *mandatory restricted access* (Rule 1.18).

---

## Which services may use it

| Service | MDP available? |
|---|---|
| Premium subscription film services | Yes (originally the only category, with pay-per-view) |
| Pay-per-view services | Yes |
| Scheduled TV channels showing programmes and films | **Yes, from 1 January 2019** (this was the 2018 extension) |
| Free-to-air DTT (e.g. Freeview) | **No** — cannot currently implement it |
| Channels not on a vertically integrated pay-TV platform | **No** — only channels on vertically integrated pay-TV platforms can currently implement it |

Platforms must rule out unprotected unsuitable content **on all devices, including legacy and
unconnected ones**.

---

## What may be shown, and when

| Content | Without MDP | With MDP |
|---|---|---|
| BBFC **18**-rated films (or equivalent) | Not before **21:00** on any service (Rule 1.23) | **Any time of day** |
| Programmes unsuitable for children normally scheduled post-watershed | Watershed rules apply (21:00–05:30) | **Any time of day** |
| Films up to BBFC **15** on premium subscription film services | From **20:00** (carve-out retained — Ofcom had proposed removing it and did not) | Any time of day |
| Films up to BBFC 18 on **pay-per-view** | — | **Any time** (Rule 1.25) |
| Films **refused** BBFC classification (Rule 1.22) | Prohibited | **Prohibited — unchanged** |
| BBFC **R18** films (Rule 1.26) | Prohibited | **Prohibited — unchanged** |
| **Adult sex material** (Rule 1.18) | 22:00–05:30 + mandatory restricted access | **Unchanged — MDP does not extend this** |

Additional obligations where MDP is relied on:
- **Clear information** must be provided about the content, **and** an explanation of the MDP in place,
  to all viewers.
- **Pay-per-view** additionally: content information, a **detailed itemised billing system**, and a clear
  explanation of security systems to subscribers.

---

## Resulting amended Code rules

- **Rule 1.23** — BBFC 18 films must not be broadcast before 21:00 on any service, **except where there is
  MDP**. (The previous pay-per-view-specific reference was replaced by the MDP concept.)
- **Rule 1.24** — the general MDP route: unsuitable programmes and films up to BBFC 18 may air at any time
  with MDP; films up to BBFC 15 on premium subscription film channels may start from 20:00 without it;
  information duties apply.
- **Rule 1.25** — pay-per-view route with MDP, plus billing and security-explanation duties.

---

## Design implications

1. **`service_type` and `access_control` are mandatory inputs, not optional.** Without them the UK answer
   is indeterminate. If a content description does not state the service type and whether MDP/mandatory
   restricted access is in place, the correct behaviour is to **return a missing-information flag**, not to
   assume free-to-air. This is a prime candidate for the prompt's "missing information" path and for a
   dedicated test case.
2. **Three distinct access concepts must not be conflated:**
   - *mandatory daytime protection* (PIN, pre-2100/post-0530) → unlocks films up to 18 at any hour;
   - *mandatory restricted access* (Rule 1.18) → gates adult sex material in the 22:00–05:30 window;
   - no protection → ordinary watershed.
   A model that treats "PIN protected" as a single concept will wrongly allow adult sex material in daytime.
3. **Absolute prohibitions survive every access measure** (R18, refused classification). These should be
   hard-coded as a pre-check in code rather than left to the prompt, since no amount of contextual
   reasoning should be able to override them.
