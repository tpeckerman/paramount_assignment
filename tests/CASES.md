# Test cases

Five cases. Each one is built to **break** the system in a specific way, not to show it
working. A test suite of plausible-looking content tells you nothing: every case here has a
known right answer that a naive pipeline gets wrong, and I say in advance what the failure
would look like.

| # | Case | What it attacks | A naive system fails by |
|---|---|---|---|
| TC-01 | BBFC 15 action film, free-to-air | rating ≠ hours | Emitting "15" as the UK answer. There is no such thing for UK linear TV. |
| TC-02 | The *same film*, premium service with PIN | the third axis | Saying "any time" and dropping the PIN condition that earned it. |
| TC-03 | Comedy sketch mocking a religion | negative space | Finding no violence/sex/drugs and returning "no restrictions". |
| TC-04 | Music video, daytime slot, plus its trailer | derived assets | Judging the trailer by the parent's permission. |
| TC-05 | Self-contradicting description, no service type | missing information | Resolving the contradiction silently and answering confidently. |

---

## TC-01 — Cinema film carried over to television

```
TITLE: "Harbour Line" (feature film, 104 min)
CERTIFICATE: BBFC 15 (cinema release)
INTENDED SERVICE: free-to-air general entertainment channel
INTENDED SLOT: not stated
COUNTRIES: UK, FR

EVENTS
00:06:12  Two men fight in a stairwell. One is struck with a bottle; blood is visible.
00:21:40  Sustained use of strong language during an argument (approx. 8 instances).
00:48:03  A character prepares and injects heroin. The process is shown in close-up.
01:12:55  A consensual sex scene. Partial nudity, no explicit detail. Approx. 90 seconds.
01:31:20  A character is shown contemplating suicide on a bridge. No method is depicted.
```

**Right answer.** UK: **no age rating exists** — the correct output is a scheduling answer
(post-watershed), not a number. France: a category, but the *hours depend on service type*,
so a single French answer is wrong. The drug-injection scene is two observations, not one —
the technique being shown triggers an imitable-behaviour rule independent of the drug rule.
The suicide scene must not be over-read: no method is depicted.

---

## TC-02 — The identical film, different service

```
As TC-01, identical content and certificate.
INTENDED SERVICE: premium subscription film service
ACCESS CONTROL: mandatory PIN, enabled by default, cannot be disabled by the subscriber
INTENDED SLOT: 14:30 on a Wednesday
COUNTRIES: UK, FR
```

**Right answer.** Same content, same certificate, **completely different answer**. In the UK
the watershed is *disapplied* while mandatory daytime protection is in place, so a 14:30
transmission is permissible — but only because of the PIN, and the PIN must be on by default,
which this one is. Reporting "any time" without the condition is the most dangerous possible
output. In France, Wednesday is a specifically restricted day for some categories.

This case exists because TC-01 and TC-02 differ in **no content whatsoever**. Any system that
derives hours from the rating must give them the same answer, and must therefore be wrong
about one of them.

---

## TC-03 — Negative space

```
TITLE: "The Sunday Panel" (comedy sketch, 6 min)
CERTIFICATE: none
INTENDED SERVICE: free-to-air entertainment channel
INTENDED SLOT: 19:30
COUNTRIES: UK, FR

EVENTS
00:00:30  A panel host introduces a recurring sketch that mocks the dress, accent and
          dietary rules of a named religious community. The audience laughs throughout.
00:03:10  A performer impersonates a figure from that community as foolish and dishonest.
00:05:40  The host repeats a stereotype about the community's attitude to money.
```

**Right answer.** No violence, no sex, no drugs, no strong language — a category-driven
pipeline scores this clean and returns "no restrictions". That is a serious failure. The
trigger here is **treatment**, not depicted subject matter, and it engages the
abusive-or-derogatory rule, which is context-justified. This is a human-review case, not an
automatic refusal: comedy and satire have real protection, and the answer is "escalate", not
"ban". A system that either clears it *or* refuses it outright is wrong both ways.

---

## TC-04 — Derived asset

```
TITLE: "Night Drive" (music video, 4 min) and its 30-second on-air trailer
CERTIFICATE: none
INTENDED SERVICE: music channel
INTENDED SLOT: video at 22:15; trailer in a 15:00 break
COUNTRIES: UK, FR

EVENTS — MUSIC VIDEO
00:00:45  Repeated strong language in the chorus (unedited).
00:02:10  Dancers in minimal clothing; camera emphasises bodies.
00:03:30  A performer brandishes a replica handgun toward the camera.

EVENTS — TRAILER (30s)
00:00:05  The chorus plays, strong language audible, unedited.
00:00:18  The handgun shot is included.
```

**Right answer.** Two separate decisions. The video at 22:15 is post-watershed. The trailer
at 15:00 is **not**, and does not inherit the video's permission — it is judged in its own
slot. A pipeline that reasons about "the asset" produces one answer and misses the breach
entirely. Also tests adjacency: French rules restrict placement near children's programming.

---

## TC-05 — Missing information and self-contradiction

```
TITLE: "Coastal Rescue" (documentary, 48 min)
SUMMARY SUPPLIED BY DISTRIBUTOR: "Suitable for all audiences. No content of concern."
INTENDED SERVICE: not stated
INTENDED SLOT: not stated
COUNTRIES: UK, FR

EVENTS
00:14:02  Footage of a real fatal accident; a body is visible at a distance.
00:32:18  A bereaved relative describes the death in detail, visibly distressed.
00:41:05  A presenter demonstrates a climbing technique described as "easy to copy at home".
```

**Right answer.** The distributor's summary **contradicts** the event list. The correct
behaviour is to surface the contradiction, not to silently believe either side. Service type
is absent, and in France that single gap makes the hours unanswerable — the system must
branch, not assume. Real footage of death engages rules that dramatised violence does not.
The "easy to copy at home" line is an imitable-behaviour trigger that reads as harmless.

A confident answer here is a **failure**, even if the rating happens to be right.
