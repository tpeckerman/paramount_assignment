# Test cases

The system's input is a **written description with timecodes**, not a video. So a test case is
a description, and running one needs no media file. These are all built on real, identifiable
content rather than invented titles.

Eight cases. Two have **known real-world outcomes**, so the right answer is not my opinion:
TC-01 is a decided regulator case, and TC-08 is content that has aired in UK daytime for
decades.

| # | Content | Category | What it tests | A naive system fails by |
|---|---|---|---|---|
| TC-01 | *Toofan*, NTV, 11:30 | `violence`, `audience_information` | **Does it match a real regulator decision?** | Clearing it, or citing the wrong rule |
| TC-02 | *Mad Max: Fury Road*, free-to-air | `violence`, `film_carryover` | An age rating does not tell you the hours | Answering "15" when the UK issues no rating |
| TC-03 | The same film, premium service | `violence`, `access_control` | A PIN can replace a time restriction | Saying "any time" and dropping the PIN |
| TC-04 | *Thriller* and its trailer | `fear_distress`, `occult_paranormal`, `trailers`, `music_videos` | A trailer is its own decision | Letting the trailer inherit the video's slot |
| TC-05 | Documentary, summary contradicts it | `fear_distress`, `imitable_behaviour` | The supplied summary can be wrong | Believing it, or settling the clash silently |
| TC-06 | *Step Brothers*, comic sex scene | `sexual_content` | Comedy does not excuse every rule | Clearing it for being funny with no nudity |
| TC-07 | *The 40-Year-Old Virgin* | `sexual_content`, `nudity` | ...and sometimes it does | Answering it the same way as TC-06 |
| TC-08 | *Friends*, after-sex scene at 14:30 | `sexual_content` | **Being too strict, which nobody reports** | Pushing it to 21:00 and nobody noticing |
| TC-09 | Cookery show, plaster on a cut finger | `serious_harm`, `imitable_behaviour`, `drugs_alcohol_smoking` | **A benign control: does anything ever come back clear?** | Escalating it, which the first run did |

The category column uses the rules table's controlled vocabulary, not free text, so it can be
checked against the rules the engine actually selects.

**TC-06 to TC-08 were added because the first five all fail the same way.** Every one catches
a system being too permissive. Train on those alone and you get a system that is always
cautious, which scores well and quietly costs daytime slots. TC-08 is the only case that
catches it.

### What these cases do not test

Seven of eleven content categories are exercised. Not tested:

- `strong_language` (4 rules)
- `hatred_discrimination` (2 rules)
- `suicide_self_harm` (2 rules)
- `religion` (1 rule)

A pass rate here is a pass rate on the seven.

---|---|---|
| `strong_language` | 4 | A common real breach type, and the clearest case of something **audible and not visible**, which a picture-only description would miss |
| `suicide_self_harm` | 2 | Has its own rules on method and imitation |
| `hatred_discrimination` | 2 | Judged on treatment, not on whether the words were said |
| `drugs_alcohol_smoking` | 1 | Turns on glamorisation, not depiction |
| `religion` | 1 | Section Four exists; nothing here goes near it |

Four of the five are judgment calls, so the gap sits on top of the table's known weak spot.

A pass rate over six of eleven categories is a pass rate **on the six**. Same shape as the
quote-coverage defect in `RESULTS.md`. `out_of_scope/pipeline/verify_cases.py` prints this denominator on
every run so it cannot go stale.

---

## TC-01: Back-test against a real Ofcom decision

Everything here is taken from Ofcom's published finding (Broadcast and On Demand Bulletin
issue 553, 7 September 2026), including the clock times. **The outcome is known**, so this
measures the system rather than my judgment of it.

```
TITLE: Toofan (feature film, Bengali-language action)
CERTIFICATE: BBFC 15
SERVICE: NTV, free-to-air satellite
TRANSMISSION: 29 May 2026, 11:30
DATE CONTEXT: during the three-day Eid-ul-Adha celebrations
COUNTRIES: UK

EVENTS (clock times during transmission, as recorded by the regulator)
11:33  A mass shooting. A character uses a large machine gun to kill multiple people.
       This scene is repeated at 13:41.
12:24  A man is stabbed to death. Another is beheaded with a machete, followed by a shot
       of the decapitated head being carried by the killer.
13:28  A man is choked to death during a wrestling match.
13:44  Multiple people are assassinated.
NO WARNING OR SIGNPOSTING was given before or during the broadcast.
```

**Known outcome:** breach of Rule 1.3. Ofcom also opened the case under Rule 2.3 (offence)
and **dropped that limb**, finding the violence contextually justified within the film.

> **Source.** `UK-P1_ofcom_decision_toofan.pdf` in `sources/originals/`, Ofcom bulletin issue
> 553, 7 September 2026
> ([original](https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins/broadcast-bulletins/2026/553/toofan-ntv-29-may-2026-11.30.pdf)).
> Verbatim: `"Breach of Rule 1.3 of the Code."` and, on the dropped limb, Ofcom
> `"did not pursue the investigation further under Rule 2.3"` having found the material
> `"sufficiently contextualised within the film"`.
> `out_of_scope/pipeline/verify_cases.py` checks all three against the PDF, so the claim fails the build
> if it drifts.

**What the system must get right.** The breach, on Rule 1.3. The absence of a warning as an
aggravating factor. The festival date as raising the likely child audience. And critically,
that the content *was* contextually justified while the **scheduling** was not. A system that
resolves "justified by context?" once and reuses the answer for both questions reaches the
wrong result here.

---

## TC-02: *Mad Max: Fury Road* (2015), free-to-air

BBFC 15. Timecodes are indicative rather than frame-accurate; the content is as classified.

```
TITLE: Mad Max: Fury Road (feature film, 120 min)
CERTIFICATE: BBFC 15 (cinema and home video)
SERVICE: free-to-air general entertainment channel
SLOT: not stated
COUNTRIES: UK, FR

EVENTS (indicative)
00:08  Sustained vehicular pursuit; a character is dragged behind a moving vehicle.
00:23  A character is branded with a hot iron. Pain is shown; no graphic wound detail.
00:41  Repeated depictions of human beings used as blood donors, restrained and bled.
01:06  Prolonged combat with improvised weapons. Multiple deaths, limited blood detail.
01:34  A character falls under the wheels of a moving vehicle. Impact implied, not shown.
THEMES: captivity, forced reproduction, references to sexual slavery. No sexual content
        is depicted.
```

**Right answer.** UK: **no age rating exists**; the output is a scheduling verdict. France:
a category, but the *hours depend on service type*, so a single French answer is wrong. The
themes matter independently of what is depicted, and nothing here is sexual content despite
the subject matter, which is a distinction a keyword-driven read gets wrong.

---

## TC-03: The same film, premium service, PIN

```
As TC-02, identical content and certificate.
SERVICE: premium subscription film service
ACCESS CONTROL: mandatory PIN, enabled by default, cannot be disabled by the subscriber
SLOT: 14:30, Wednesday
COUNTRIES: UK, FR
```

**Right answer.** Same film, **opposite answer**. In the UK the watershed is *disapplied*
while mandatory daytime protection is in place, so 14:30 is permissible, but only because of
the PIN, and only because it is on by default. Reporting "any time" without that condition is
the most dangerous output this system can produce. In France, Wednesday is specifically
restricted for some categories.

TC-02 and TC-03 differ in **no content whatsoever**. Any system deriving hours from the rating
must answer both identically and must therefore be wrong about one.

---

## TC-04: *Thriller* (Michael Jackson, 1983) and its trailer

```
TITLE: Thriller (music video, 13 min 42 s)
CERTIFICATE: none
SERVICE: music channel
SLOT: video at 22:15; 30-second trailer in a 15:00 break
COUNTRIES: UK, FR

EVENTS, music video (indicative)
00:02  A character transforms into a werewolf. Prosthetic effects, sustained close-up.
00:05  Corpses rise from graves. Decayed faces shown in detail over an extended sequence.
00:09  A woman is pursued and cornered by the risen figures inside a derelict house.
00:13  A final shot of the lead's eyes in a non-human form.
NOTE: the work opens with an on-screen disclaimer stating it does not endorse belief in
      the occult.

EVENTS, trailer (30 s)
00:05  The graveyard sequence, decayed faces included.
00:18  The pursuit, cut faster than in the full video.
```

**Right answer.** Two decisions. The video at 22:15 is post-watershed. The trailer at 15:00 is
**not**, and does not inherit the video's permission. Horror imagery and fear or distress are
the live categories, not violence. France treats music videos more softly than the UK, so the
same asset should yield a harder UK answer than French one, and rendering the French
preference as a prohibition is an over-rating defect. The occult disclaimer is a real
contextual factor, not decoration.

---

## TC-05: a documentary where the paperwork disagrees with the program

A program arrives from a distributor with a short written summary of what is in it. The
scheduler reads the summary, not the program. It is the cheapest thing in the process and
usually right. This case is what happens when it is not.

```
TITLE: Coastal Rescue (documentary, 48 min)
SUPPLIED SUMMARY: "Suitable for all audiences. No content of concern."
SERVICE: not stated
SLOT: not stated
COUNTRIES: UK, FR

EVENTS
00:14:02  Footage of a real fatal accident. A body is visible at a distance.
00:32:18  A bereaved relative describes the death in detail, visibly distressed.
00:41:05  A presenter demonstrates a climbing technique, described on screen as
          "easy to copy at home".
```

The summary says there is nothing to worry about. The event list has a real death, a grieving
relative, and an instruction to copy something dangerous at home. Both arrived in the same
package and they cannot both be true.

**Why the summary exists, and why believing it is dangerous.** Whoever wrote it wanted the
program scheduled. Not dishonesty, just a description written for a buyer rather than an
audit against a regulator's rules. The trap is that it is far easier to read than the event
list, because it already contains a conclusion. So the right move is not to pick the more
trustworthy source but to **record that they disagree and stop**: a program whose
description does not match its contents needs a person, whatever the content answer is.

**Four things it tests:**

1. **The contradiction.** Surface it, do not settle it silently.
2. **A missing fact that blocks the answer.** No service type is given, and French hours
   depend on it, so the correct French output is a question rather than a time.
3. **Real death is not dramatised death.** The French rule is the sharper one: `FR-VIO-003`
   covers `"images difficilement soutenables ou des témoignages"`, hard-to-watch images **or
   testimony**. The grieving relative is the testimony limb, which a UK-trained reading would
   treat as a harmless talking head.
4. **The most dangerous line reads as the friendliest.** `"easy to copy at home"` is the
   trigger for `UK-IMI-001` and `UK-IMI-010`, where the test is imitability **plus setting**:
   a kitchen counts, a mountaineering expedition does not. A system scanning for violence,
   sex, drugs and language finds nothing wrong with that sentence.

**A confident answer here is a failure, even if the rating happens to be right.**

---

## TC-06, TC-07, TC-08: where comedy saves you, and where it does not

Three UK rules sit next to each other and do **not** share an escape clause:

| rule | covers | escape |
|---|---|---|
| Rule 1.19 | strong or explicit sexual images **or language** | justified by **context** |
| Rule 1.21 | **nudity** before the watershed | justified by **context** |
| Rule 1.20 | **representations of sexual intercourse** | **serious educational purpose** only |

Comedy is context, so it rescues content under 1.19 and 1.21 and cannot rescue it under 1.20,
which has no door a comedy fits through. Hence a result most people get backwards: **a sex
scene with no nudity can be more restricted than a nude scene.**

These also exercise a distinction the extraction stage has fields for and nothing has tested:
whether an act is **shown**, **implied**, or **referred to afterwards**.

### TC-06: *Step Brothers* (2008)

```
TITLE: Step Brothers (comedy feature)
CERTIFICATE: BBFC 15
SERVICE: free-to-air
TRANSMISSION: not stated
COUNTRIES: UK, FR

EVENTS
00:48:10  A sex scene played for comedy. Sexual intercourse is clearly depicted.
          No nudity is shown. The staging is broad and unrealistic, scored for laughs,
          and the scene is intercut with reaction shots.
```

**Right answer.** Not before 21:00 on **Rule 1.20**, with the comedy irrelevant to it. Rule
1.21 does not fire: no nudity to justify.

**How it fails.** The system reasons "comedy, unrealistic, no nudity" and clears it for the
afternoon. All three observations are true and none of them reaches Rule 1.20.

### TC-07: *The 40-Year-Old Virgin* (2005)

```
TITLE: The 40-Year-Old Virgin (comedy feature)
CERTIFICATE: BBFC 15
SERVICE: free-to-air
TRANSMISSION: not stated
COUNTRIES: UK, FR

EVENTS
00:09:30  Sustained comic dialogue between friends describing sexual acts in explicit
          terms. No sexual activity is shown.
00:21:15  A chest-waxing scene. A man's bare chest is shown; he shouts in pain.
          Played entirely for comedy.
```

**Right answer.** Genuinely arguable, which is why it is here. Rule 1.19 is engaged by the
explicit language, and here the comedy **is** a live argument because 1.19 bends to context.
Rule 1.20 does not fire: nothing is depicted. The waxing is not sexual nudity.

The system should escalate, cite Rule 1.19, and set the context argument out rather than
settle it. That rule is `judgment_based`, and `out_of_scope/pipeline/postcheck.py` fails any answer
leaning on a judgment rule without flagging it.

**The pair is the real test.** Two comedies, both BBFC 15, both explicit, neither with sexual
nudity. One is a hard 21:00 where comedy counts for nothing; the other a judgment call where
it counts for a lot. A system treating "comedic" as one modifier applied to all sexual content
answers both alike, and is wrong about one.

### TC-08: *Friends*, an after-sex scene

```
TITLE: Friends (sitcom, 22 min episode)
CERTIFICATE: none
SERVICE: general entertainment, pay TV, with a +1 timeshift channel
TRANSMISSION: 14:30 weekday
COUNTRIES: UK

EVENTS
00:11:40  Two characters are shown in bed together after sex, covered by a duvet,
          talking. No sexual activity is shown and no nudity is visible.
          The fact that they have had sex is clear from the dialogue.
```

**Right answer.** Fine at 14:30. Rule 1.20 does not fire, because the aftermath of sex is not
a representation of intercourse. No nudity, so not 1.21. Implication alone is unlikely to
engage 1.19.

**The outcome is known.** *Friends* has run in UK daytime for decades: around 23 hours a week
on free-to-air E4 before 2011, a Comedy Central daytime staple since. No Ofcom finding. So a
system that pushes this to 21:00 is **over-rating**, provably.

Two details kept rather than tidied away:

- The channel is **pay TV**, a different `service_type` from E4. The real history spans both,
  so the daytime answer does not depend on which you pick.
- There is a **+1 channel**, so the same episode airs again at 15:30. That is `UK-SCH-009`,
  and answering for 14:30 alone answers half the question.

---

## TC-09: a benign control, which the set was missing

Every other case here is content with something in it. That is a test set that can only ever
measure one thing: whether the system restricts enough. It cannot notice a system that
restricts everything, because nothing in it should come back clear.

An external reviewer ran exactly this gap and found it: a cookery program with a plaster on
a cut finger escalated in both countries, alongside four deliberately hostile inputs. Five out
of five. At that point the escalation rate stops being a number about content and becomes a
number about the system.

```
TITLE: Market Kitchen (cookery series, 30 min episode)
CERTIFICATE: none
SERVICE: free-to-air general entertainment
TRANSMISSION: 11:00 weekday
COUNTRIES: UK, FR

EVENTS
00:06:20  A presenter slices a vegetable and nicks a finger. A plaster is applied.
          No blood is shown. The moment is brief and treated lightly.
00:18:40  A knife-skills demonstration, filmed close up, in a domestic kitchen.
00:24:05  A glass of wine is poured alongside the finished dish and tasted.
```

**Right answer.** Permitted at 11:00 in both countries, with no condition and no escalation.

**What it tests, which nothing else here does.** The system has rules about injury, about
imitable behavior in a setting a viewer could reproduce, and about alcohol. All three are in
the slice. **None should apply**, and the answer should not escalate just because a
judgment rule was present.

**Why the first run failed it.** The reviewer found that the description step forced the cut
finger into `serious_harm`, because the closed category list has no value for a minor injury.
Then the decision step saw a judgment rule in its slice and escalated, as it was built to do.
Neither step did anything wrong on its own terms.

**This is the case that would catch the escalation fix going too far.** If a later change
relaxes escalation until TC-09 passes, TC-01 and the hostile inputs must still escalate. A
benign control is only useful next to cases that must not come back clear.
