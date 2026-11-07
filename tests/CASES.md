# Test cases

## On what "test case" means here

The prompt's input is **a content description with events and timecodes**, not a video file.
So a test case is a description, and no media file is needed to run one. What a test case
*can* be is about real, identifiable content rather than invented titles, which is what these
are.

Five cases. Each attacks a specific way this system fails, and the first is the strongest kind
of test available: a **real broadcast with a real regulator finding**, so the right answer is
not my opinion.

| # | Content | Attacks | A naive system fails by |
|---|---|---|---|
| TC-01 | *Toofan*, NTV, 29 May 2026, 11:30 | **back-test against a decided case** | Clearing it, or citing the wrong rule |
| TC-02 | *Mad Max: Fury Road*, free-to-air | rating does not give hours | Emitting "15" as the UK answer |
| TC-03 | *The same film*, premium + PIN | the third axis | Saying "any time" and dropping the PIN |
| TC-04 | *Thriller*, music channel, plus its trailer | derived assets | Judging the trailer by the video's slot |
| TC-05 | Documentary with contradictory metadata | missing information | Resolving the contradiction silently |

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
