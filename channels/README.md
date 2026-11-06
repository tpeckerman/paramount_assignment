# Channel-level data

The level the first scaling draft missed. Some facts that change a decision are not shared
logic and not country law. They belong to a single channel, and two channels in the same
country under identical law need different answers.

The Toofan decision turned partly on the broadcast falling during Eid-ul-Adha, because that
channel serves a Muslim audience. The same date on a different channel carries no such
weight. **A public-holiday calendar cannot produce this**, and a system that tries will be
wrong in both directions: flagging dates that do not matter to that audience, and missing
ones that do.

## What goes in a channel file

- `high_child_audience_dates`, festivals, holidays and local events when families gather
  around that channel. Ten to twenty entries is normal.
- `has_timeshift`, whether a `+1` service carries the same schedule an hour later. This
  changes the answer with no edit to the content: material placed while children are at
  school lands after they are home.
- `service_type`, how the channel is classified under local rules. In France this decides
  the permitted hours outright.
- `regulator_agreement`, any channel-specific undertaking stricter than the general law. In
  France these are formal conventions; elsewhere they may be licence conditions.

## Who maintains it

The channel's own compliance contact, not a lawyer and not the platform team. Nobody else
knows it, and no amount of research reproduces it.

**This changes the staffing model.** "One lawyer per country" does not cover this level. You
also need a named contact per channel, but what you need from them is about an hour a year,
not a retainer.

## How it is used

`high_child_audience_dates` never changes the permitted hours. It raises the expected child
audience within those hours, which makes a borderline slot a review item rather than an
automatic pass. When the transmission date is unknown, the decision is marked provisional
rather than assumed to fall on an ordinary day.

See `example_channel.json` for the shape.
