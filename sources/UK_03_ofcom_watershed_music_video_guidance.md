# UK-G1 — Ofcom Guidance: Observing the watershed on television and music videos

- **Regulator:** Ofcom
- **Source type:** regulator_guidance (authority rank 3)
- **URL:** https://www.ofcom.org.uk/__data/assets/pdf_file/0030/86781/watershed-on-tv.pdf
- **Scope:** Television. Pre-watershed and immediately-post-watershed content; **music videos**.
- **Status:** Guidance — not itself binding, but it is how Ofcom reasons when applying Rules 1.3–1.6 and 2.3.
- **Retrieval status:** STRUCTURED EXTRACT.

> **Why this document matters disproportionately for this assignment.** It is the only UK source that gives
> operational detail on **music videos**, which is one of the content types the assignment explicitly suggests
> for test cases. It also gives the only guidance on the **post-watershed ramp**.

---

## 1. Material before and soon after the 21:00 watershed

- The watershed is **21:00**; unsuitable material should not in general be shown before 21:00 or after 05:30.
  The watershed applies to television only.
- Rule 1.3 (appropriate scheduling) is judged on the nature of the content, the likely number and age of
  child viewers, and the nature of the channel and programme. **"Television broadcasters must observe the
  watershed."**

### What Ofcom expects immediately after 21:00 (the "ramp")
- A programme that **starts before 21:00 and continues past it must not suddenly become unsuitable.**
- A programme **starting after the watershed** should make a **smooth transition** to more adult material
  and **should not open with its strongest material**.
- **No fixed interval is specified.** There is no "X minutes after 21:00" rule. Whether a transition is
  smooth is judged case by case.
  → *For the rule table this is a `judgment_based` rule, not a bright line. Flag for human review when a
  test case places strong material in the first minutes after 21:00.*

### Areas Ofcom singles out for particular care
- **Family viewing shows** — attract large child audiences; content should suit family viewing throughout.
  Extra caution if the show runs past 21:00. Daytime repeats need separate thought.
- **Trailers** — viewers do not choose to watch them, so trailers shown before the watershed for
  post-watershed programmes must contain only pre-watershed-appropriate material. May need restricting
  around children's programming, family shows and sports coverage.
- **Soaps** — a frequent source of parental concern. Each episode must be scheduled appropriately in its own
  right, with viewer information where needed; a long-running storyline does not by itself supply context.
- **Post-watershed content edited for daytime** — may be shown earlier if properly edited, but some content
  remains unsuitable regardless of editing because of adult themes or frequent offensive language.
  **Frequent bleeping has a cumulative effect.** Violence should be limited. **+1 (timeshift) services need
  specific attention** — a 21:00 broadcast becomes a 22:00 broadcast on +1, but a 20:00 broadcast becomes 21:00.

---

## 2. Music videos broadcast before the watershed

Ofcom acknowledges artistic freedom but has statutory duties to protect under-eighteens and to apply
generally accepted standards.

### Scheduling factors applied to music videos
Nature of the content; likely child audience (**including school time, weekends and holidays**);
start and finish times; channel type; audience expectations.
**Niche music channels still carry responsibility toward possible child viewers** — a small or
genre-specific audience does not remove the duty.

### Genre and editing
- Urban and R&B videos often include mild sexual content and innuendo. Broadcasters must still consider
  the **strength of the imagery**, the genre, the time of broadcast, and whether the video was
  **edited for a child audience** (e.g. supplied marked "pre 9pm").

### Specific content thresholds given
| Element | Guidance |
|---|---|
| **Sexual images** | Sexualised images are not banned but must be **editorially justified and appropriately limited**. Explicit sexual behaviour should be avoided. **Intrusive or prolonged shots of body parts increase sexual impact.** |
| **BDSM / fetish imagery** | Not prohibited, but **explicit** imagery should be avoided. Ofcom considers **shot length, repetition, and the video's overall theme**. |
| **Clothing** | Underwear and bikinis are not prohibited; context matters, especially whether the clothing is **presented sexually**. Pre-watershed videos should not show performers **inadequately covered, particularly the breasts, genitals or buttocks**. Fetish clothing combined with sexual behaviour needs care. |
| **Lyrics** | Pre-watershed videos should **avoid lyrics clearly focused on sex**. Lyrics that seem mild on audio alone **can become highly sexualised when paired with sexual imagery.** |
| **Dancing** | Provocative or sexualised dancing should be **limited**. Cultural or traditional links can justify it, but the justification must be sufficient for the images actually shown. |
| **Violence / dangerous behaviour** | Violence should be **limited and justified by context**, and not explicit, gratuitous or easily imitable. **Images of suicide are not banned but must be very carefully limited so that no details could prompt imitation.** |

---

## Design implications

1. **Audio–visual interaction is explicit.** The lyrics guidance says mild audio + sexual imagery =
   highly sexualised. A content-extraction stage that tags audio and video independently and never
   combines them will systematically **under-rate** music videos. The extraction schema needs a
   combined/aggravating-factor field.
2. **Duration and repetition are rated, not just presence.** "Prolonged", "shot length", "repetition",
   "frequent", "cumulative" all appear. This is a direct argument for requiring **timecodes with durations**
   in the input, which the assignment already asks for.
3. **Niche channel ≠ relaxation.** A plausible model failure is reasoning "this is a niche music channel so
   the child audience is negligible". The guidance explicitly closes that off. Worth a negative test case.
4. **"Edited for pre-9pm" is a real input signal.** If a test case says the supplied version is a
   pre-watershed edit, that changes the analysis. The prompt should accept a `version/edit` input field.
