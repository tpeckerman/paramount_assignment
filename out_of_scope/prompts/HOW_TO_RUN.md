# How to run these prompts

Two prompts, run in order. Everything here is doable by hand with a model you can paste into;
no code is required, and the code in the repository only automates the middle step.

## Step 1: describe the content

Paste `RUN_1_describe_content.md`, then the content description between the delimiters it
declares:

```
<content_description>
TITLE: ...
CERTIFICATE: ...
SERVICE: ...
TRANSMISSION: ...
COUNTRIES: UK, FR

EVENTS
00:14:02  what happens
</content_description>
```

Out comes a JSON object: the asset, the transmissions, the observations with timecodes, and
what it was not told.

**This step does not see the rules, on purpose.** An extractor that knows the thresholds
shades its descriptions toward the rating it expects, and then the decision is already made,
invisibly, by an adjective.

## Step 2: pick the rules that could apply

This is the only step that is not just pasting. Take the rules table and keep a row if **all**
of these hold:

1. `valid_to` is `open`. A closed rule may not reach a decision.
2. `country` matches a country you want an answer for. The table holds UK and French rules
   together. You decide which countries you are asking about and you write them into the
   `<request>` block in step 3. Keep the rows for those countries and drop the rest: if you
   only want a UK answer, the French rows do not belong in the slice. Most content
   descriptions name the countries at the top, as the test cases do with `COUNTRIES: UK, FR`,
   so that line is usually what you copy.
3. `service_type` names the service, **or** is service-agnostic (`all_linear_tv`,
   `all_avms`), **or** the service was not stated. When the service is unknown, keep
   everything: the decision step branches, and withholding rows narrows the branches it can
   see without saying so.
4. `content_category` is one that step 1 observed, **or** is in the always-keep list below.

**The always-keep list, and why it exists.** Some rules describe how a program is
*delivered* or what it *is*, not what is in it, so no content description ever mentions them
and a category filter drops them every time:

- `scheduling_general`, `definition`, `classification_scheme`, `legal_basis`, `scope`,
  `signage`, `film_carryover`, `access_control`, `audience_information`, `trailers`,
  `human_dignity`, `serious_harm`, `commercial_conditions`, `channel_override`,
  `data_protection`
- plus every absolute prohibition, always, whatever the categories
- plus categories implied by the asset itself: a `music_video` pulls in `music_videos`, a
  `trailer` pulls in `trailers`

Each of those entries is there because a real run lost a rule without it. A PIN is not
content, so access-control rules vanished. A music video is not an observation, so every
music-video rule vanished from a music video.

**The lesson, which this project learned five separate times.** A filter built from what is
IN the content cannot retrieve rules about what the content IS or how it is DELIVERED. When
adding a category to the rules table, ask which of the two kinds it is. If a content
description would never mention it, it belongs on this list from the day it is created.

**One more trap.** Countries name their service types in their own words and the names do not
line up: the UK has `premium_subscription_film`, France regulates `cinema_channels`. Asking
for the UK token matched nothing French and silently dropped eight rules, which made a French
answer look unanswerable when it was merely unasked. If a service has no equivalent term in
the other country, keep that country's rows and let the decision step weigh them.

## Step 3: decide

Paste `RUN_2_decide.md`, then three blocks:

```
<rules>
[ the rows you kept in step 2, as JSON ]
</rules>

<observations>
[ step 1's output, unedited ]
</observations>

<request>
{"countries": ["UK","FR"], "service_type": "...", "intended_slot": "...", "intended_date": "..."}
</request>
```

Take `service_type`, `intended_slot` and `intended_date` from step 1's output when it
recorded them. Writing `not_stated` over a slot the description actually gave throws away the
fact the decision turns on.

Out comes a decision per country per transmission: classification, hours, other restrictions,
the reasoning with a `rule_id` behind every claim, what is missing, and whether a person must
look at it.

## Reading the answer

- **Three outputs, not two.** The classification, the hours, and any other restriction. They
  can substitute for each other and they can stack, and one country here issues no
  per-program rating at all, so `no_per_programme_rating` is a real answer rather than a
  gap.
- **Every claim carries a `rule_id`.** Follow it into the table to find the clause and the
  quote from the law. A time with no rule beside it cannot be defended by whoever has to
  defend it.
- **"A person must decide" is an answer.** So is "I was not told X". Neither is a failure.
