# UK-S2 — Ofcom Broadcasting Code, Section Two: Harm and Offence

- **Regulator:** Ofcom
- **Source type:** regulator_binding (authority rank 2)
- **URL:** https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence
- **Authoritative form:** the HTML above (last updated 19 Feb 2024). ⚠ The PDF edition is
  **January 2019** and predates it by five years.
- **Published:** 3 March 2021 · **Last updated:** 19 February 2024
- **Legal basis:** Communications Act 2003 ss. 3(4)(g), 319(2)(a), (f) & (l)
- **Retrieval status:** STRUCTURED EXTRACT, not official full text.

> **Why this section is in scope.** Section One repeatedly defers to "the context", and the binding
> definition of "context" lives here. The time of broadcast is one of its components. This is the
> mechanism by which the *same scene* can be compliant at one hour and a breach at another, even though
> no age rating has changed. Section One states it must be read in conjunction with Section Two.

---

## Principle

To apply generally accepted standards to the content of television and radio services so as to provide
adequate protection for members of the public from harmful and/or offensive material.

---

## Meaning of "context" — the operative definition

Context includes (but is not limited to):

1. the **editorial content** of the programme, programmes or series;
2. the **service** on which the material is broadcast;
3. the **time of broadcast**;
4. **what other programmes are scheduled** before and after the programme or programmes concerned;
5. the **degree of harm or offence likely to be caused** by the inclusion of any particular sort of
   material in programmes generally or programmes of a particular description;
6. the **likely size and composition** of the potential audience and **likely expectation** of the audience;
7. the **extent to which the nature of the content can be brought to the attention of the potential
   audience**, for example by giving information;
8. the **effect of the material on viewers or listeners who may come across it unawares**.

For BBC ODPS, scheduling and time of broadcast do not apply; context instead covers the manner in which
the content is accessed, including any measures intended to prevent children viewing or listening.

---

## Relevant rules

- **2.1** Generally accepted standards must be applied to the contents of television and radio services and
  BBC ODPS so as to provide adequate protection for members of the public from the inclusion of harmful
  and/or offensive material.
- **2.3** In applying generally accepted standards broadcasters must ensure that material which may cause
  offence is **justified by the context**. Such material may include, but is not limited to, offensive
  language, violence, sex, sexual violence, humiliation, distress, violation of human dignity, and
  discriminatory treatment or language. Appropriate information should also be broadcast where it would
  assist in avoiding or minimising offence.
- **2.4** Programmes must not include material (whether in individual programmes or in programmes taken
  together) which, taking into account the context, condones or glamorises violent, dangerous or seriously
  antisocial behaviour and is likely to encourage others to copy such behaviour.
- **2.5** Methods of suicide and self-harm must not be included in programmes except where they are
  **editorially justified and are also justified by the context**.

---

## Design implications

1. **"Context" is the engine of the UK time rule.** Because `time of broadcast` and
   `what is scheduled before and after` are formal components of context, the UK decision function is
   genuinely time-dependent: `verdict = f(content, time, service, audience expectation)`.
   This is the concrete reason an age rating cannot be mapped to hours.
2. The Section Two list gives a usable **set of contextual factors** for the prompt's reasoning field.
   A good UK output should name which of these eight factors it relied on.
3. **Cumulative assessment is explicit** in Rule 2.4 ("in individual programmes or in programmes taken
   together") and in Rule 1.16 ("frequent use"). The content-extraction stage must therefore record
   *counts and density* of events with timecodes, not just presence/absence.
4. Rule 2.5 (suicide/self-harm) requires a **double test** — editorially justified *and* justified by
   context. A single-condition check would under-rate.
