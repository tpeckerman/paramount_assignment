# Test cases

## On what "test case" means here

The prompt's input is **a content description with events and timecodes**, not a video file.
So a test case is a description, and no media file is needed to run one. What a test case
*can* be is about real, identifiable content rather than invented titles, which is what these
are.

Eight cases. Each attacks a specific way this system fails. Two have **known real-world
outcomes**, so the right answer is not my opinion: TC-01 is a decided regulator case, and
TC-08 is content that has demonstrably aired in UK daytime for decades.

| # | Content | Attacks | A naive system fails by |
|---|---|---|---|
| TC-01 | *Toofan*, NTV, 29 May 2026, 11:30 | **back-test against a decided case** | Clearing it, or citing the wrong rule |
| TC-02 | *Mad Max: Fury Road*, free-to-air | rating does not give hours | Emitting "15" as the UK answer |
| TC-03 | *The same film*, premium + PIN | the third axis | Saying "any time" and dropping the PIN |
| TC-04 | *Thriller*, music channel, plus its trailer | derived assets | Judging the trailer by the video's slot |
| TC-05 | Documentary with contradictory metadata | missing information | Resolving the contradiction silently |
| TC-06 | *Step Brothers*, comic sex scene, no nudity | comedy is not an escape from every rule | Clearing it because it is funny and has no nudity |
| TC-07 | *The 40-Year-Old Virgin*, explicit talk | where comedy **is** a live argument | Answering it the same way as TC-06 |
| TC-08 | *Friends*, an after-sex scene at 14:30 | **over-rating**, the failure nobody reports | Pushing it to 21:00 and nobody noticing |

TC-06 to TC-08 were added because the first five all fail in the same direction. Every one of
them catches a system being **too permissive**. A test set made only of those trains a system
to be cautious, and a system that is always cautious scores well on that set and quietly costs
the business daytime inventory. TC-08 is the only case here that can catch that.

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

**Known outcome:** breach of Rule 1.3. Ofcom also considered Rule 2.3 (offence) and
**dropped it**, finding the violence sufficiently contextualised within the film.

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

## TC-05: Documentary with contradictory metadata

Modelled on the true-crime and emergency-services documentaries that fill UK daytime
schedules.

```
TITLE: Coastal Rescue (documentary, 48 min)
DISTRIBUTOR SUMMARY: "Suitable for all audiences. No content of concern."
SERVICE: not stated
SLOT: not stated
COUNTRIES: UK, FR

EVENTS
00:14:02  Footage of a real fatal accident. A body is visible at a distance.
00:32:18  A bereaved relative describes the death in detail, visibly distressed.
00:41:05  A presenter demonstrates a climbing technique, described on screen as
          "easy to copy at home".
```

**Right answer.** The summary **contradicts** the event list; the system must surface that
rather than believe either side. Service type is absent, and in France that single gap makes
the hours unanswerable. Real footage of death engages rules that dramatised violence does not.
And "easy to copy at home" is an imitable-behaviour trigger that reads as harmless.

**A confident answer here is a failure, even if the rating happens to be right.**

---

## TC-06, TC-07, TC-08: where comedy saves you, and where it does not

These three exist because of a distinction in the UK Code that is easy to state and easy to
get wrong, and that no amount of general reasoning about "is this suitable" will find.

Three rules sit next to each other and they do **not** have the same escape clause:

| rule | covers | escape clause |
|---|---|---|
| Rule 1.19 | strong or explicit sexual images **or language** | unless **justified by the context** |
| Rule 1.21 | **nudity** before the watershed | unless **justified by the context** |
| Rule 1.20 | **representations of sexual intercourse** | only a **serious educational purpose** |

Comedy is part of context. So comedy can rescue content under 1.19 and under 1.21. It cannot
rescue it under 1.20, because 1.20's only door is a serious educational purpose, and a comedy
does not have one.

That produces a result most people get backwards: **a sex scene with no nudity at all can be
more restricted than a nude scene**, because the nudity rule bends to context and the
intercourse rule does not.

These cases also test something the extraction stage has fields for but that nothing has
exercised yet: whether an act is **shown**, **implied**, or only **referred to afterwards**.

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

**Right answer.** Not before 21:00, on **Rule 1.20**, and the comedy is irrelevant to that
rule. Rule 1.21 does **not** fire, because there is no nudity to justify.

**How a naive system fails.** It reasons "comedy, unrealistic, no nudity" and concludes the
scene is mild enough for an afternoon. Every one of those observations is true and none of
them reaches Rule 1.20. A system that has learned "nudity is the thing that matters" will
clear this.

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

**Right answer.** This one is **genuinely arguable**, which is the point of including it.
Rule 1.19 is engaged by the explicit sexual language, and unlike TC-06 the comedy **is** a
live argument here, because 1.19 bends to context. Rule 1.20 does not fire: nothing is
depicted. The waxing scene is not sexual nudity.

**What the system must do** is route this to a person, cite Rule 1.19, and set out the
context argument rather than settling it. `determinacy` for that rule is `judgment_based`,
and the post-decision check now fails any answer that relies on a judgment rule without
flagging it.

**The pair TC-06 and TC-07 is the real test.** Two comedies, both BBFC 15, both with explicit
sexual content and no sexual nudity. One is a hard 21:00 with comedy counting for nothing;
the other is a judgement call where comedy counts for a lot. A system that treats "comedic
treatment" as a single modifier applied to all sexual content answers both the same way and
is therefore wrong about one of them.

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

**Right answer.** Schedulable at 14:30. Rule 1.20 does **not** fire, because the aftermath of
sex is not a representation of sexual intercourse. Rule 1.21 does not fire, no nudity. Rule
1.19 is unlikely to be engaged by implication alone.

**This one has a known real-world outcome, which is why it is here.** *Friends* has run in
UK daytime for decades. It aired on E4, a free-to-air channel, at around 23 hours a week
before 2011, and has been a daytime staple of Comedy Central ever since, at times filling
most of the schedule between late morning and early evening. No Ofcom finding has followed.
So if the system pushes this episode to 21:00, it is **over-rating**, and we know that
without needing anyone's opinion.

Two details worth keeping in the case rather than tidying away:

- The channel is **pay TV**, not free-to-air, which is a different `service_type`. The real
  broadcast history spans both, which is useful: it means the daytime answer does not depend
  on which of the two you pick.
- It has a **+1 channel**, so the identical episode goes out again an hour later. That is
  rule `UK-SCH-009`, and a decision that answers for 14:30 without noticing 15:30 exists has
  answered half the question.

Over-rating is the failure nobody reports. It costs daytime inventory quietly and generates no
complaint, which is why section 5 of `TASK2_SCALING.md` gives it its own metric. **TC-08 is
the only case in this set that can catch it.** Every other case here fails by being too
permissive. A test set made only of those trains a system to be cautious, and a system that is
always cautious scores well and is expensive to run.
