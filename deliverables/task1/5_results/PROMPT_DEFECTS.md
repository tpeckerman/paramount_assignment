# Defects found by actually running the prompts

These came out of running the prompts against all eight test cases, by agents that had never
seen the expected answers. Reading a prompt does not find these. Nothing here was visible to
the person who wrote it.

The runs are in `runs/`. The ones that affect a decision are listed first.

## 1. There is no field for access control, and it decides the answer

**The worst one.** TC-03 states `ACCESS CONTROL: mandatory PIN, enabled by default, cannot be
disabled by the subscriber`. The RUN 1 output schema has nowhere to put that. Not on the
asset, not on the transmission.

So the PIN survived only as prose, folded into `intended_service` and `extractor_notes`. Look
in `tests/runs/TC-03_run1.json`: the words are there, but no structured field holds them.

That matters because a PIN is exactly what turns `not before 21:00` into `any time` under
`UK-FLM-003`. The fact the whole case turns on reaches the decision step as free text, and a
decision engine that filters on structured fields can never see it. The schema is missing the
field that unlocks the most permissive answer in the system.

## 2. `treatment` carries two different questions at once

The field holds both *whether something was shown* (`reported_not_shown`) and *how it was
framed* (`comedic`, `stylised`, `realistic`, `documentary`). TC-07's dialogue is both comic
**and** only spoken about, and only one value fits. Information has to be dropped, and which
piece gets dropped is left to the extractor.

The prompt's own rules collide here: rule 2 says the field is for marking spoken-only events,
rule 3 says it is for framing. Both cannot be satisfied.

## 3. Wall-clock and elapsed timecodes are indistinguishable

TC-01's timecodes are wall-clock, because they came from a regulator's finding about a
broadcast. The schema's `timecode: HH:MM:SS` implies elapsed time from the start of the
programme. Nothing in the output says which.

In TC-01 that distinction is the entire case. The decision turns on material airing at 11:33
and 13:41 on a particular morning, not 11 and 13 hours into a film.

## 4. `content_type` has no value for a documentary, but `treatment` does

`content_type` offers `film | series_episode | trailer | music_video | live | other |
not_stated`. TC-05 is a documentary, so it became `other`. Meanwhile `treatment` *does* have
`documentary`. The two vocabularies disagree about whether documentary is a kind of thing.

The escape hatch the prompt provides for an unknown value covers `category` only, so the
extractor had to invent what to do.

## 5. An observation cannot say which transmission it belongs to

TC-04 is a music video at 22:15 and a trailer cut from it at 15:00: two assets, two slots,
two different answers. `observations` have no transmission id, so the join exists only in
prose. The prompt insists decisions are per transmission; the schema cannot express which
transmission an observation came from.

The trailer's timecodes also collide numerically with the video's, since both start at 00:00.

## 6. Rule 9 and rule 7 contradict each other on a `+1` service

Rule 9 says a `+1` service re-broadcasts an hour later, which invites computing 15:30 from
14:30 in TC-08. Rule 7 says never normalise or estimate a timecode. Both apply, and they
point opposite ways on the exact case rule 9 exists for.

## 7. "Asserted absent" and "not stated" are the same value

`CERTIFICATE: none` is a claim. `SERVICE: not stated` is a gap. The schema records both as
absence, so a positively asserted "there is no certificate" is indistinguishable from "nobody
mentioned a certificate". Rule 4 says every `not_stated` entry is a question for a human,
which is wrong for the first case and right for the second.

## 8. Rule 11 contradicts itself on genre

It says do not infer `is_news_or_current_affairs` from genre, then says a documentary is not
automatically news, which treats genre as evidence. Both runs hit this and resolved it
differently. For "comedy feature" one agent answered `no` and flagged that it may have broken
the rule by doing so.

## 9. Smaller ones, recorded because they cost real accuracy

- `existing_certificates.scope` is single-valued, but "BBFC 15 (cinema and home video)" is one
  certificate with two scopes. The extractor emitted two entries, which would double-count
  under any rule that counts certificates.
- `runtime_minutes` is an integer, but TC-04 is 13 min 42 s. Rounding is forced by the schema
  and forbidden by rule 7.
- `COUNTRIES: UK, FR` could mean transmission territory, production origin or rights. Nothing
  says which, and `production_origin` is a routing field.
- TC-01's `NO WARNING OR SIGNPOSTING was given` is an asserted absence that is not an
  observation and not a gap. It has no home, so it went in `extractor_notes`, which is doing
  a lot of load-bearing work across every case.
- The inputs themselves contain severity words ("sustained", "prolonged", "graphic"). Rule 1
  bans the extractor's own severity adjectives; rule 5 demands verbatim evidence. Stripping
  them would have destroyed the only duration signal in the input.
- Pain played for comedy (TC-07's waxing) matches no category. It became `offence_general`.

## What this says about the prompts

The prompts are careful about the *reasoning* and loose about the *schema*. Almost every
defect above is a container problem: a field that cannot hold what the content says, or two
facts sharing one slot. None of it was visible from reading, and all of it surfaced in the
first run.

Defect 1 is the one to fix before anything else, because it is the only one that silently
produces a **more permissive** answer than the law allows.
