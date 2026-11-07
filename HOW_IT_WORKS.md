# How it works

How a content description becomes a decision, and where the rules come in.

## The flow

Three kinds of step, and the distinction matters more than it looks:

| | |
|---|---|
| 🟩 **Code** | Deterministic. Same input, same output, every time. Costs nothing, cannot be argued with. |
| 🟪 **Model** | Needs reading, weighing or judgement. Used only where code genuinely cannot do the job. |
| 🟧 **Person** | A judgement with consequences, or a decision nobody should automate. |
| ⬜ **Dotted** | Outside the scope of this project. Shown because the flow does not make sense without it, not because it is built. |

```mermaid
flowchart TB
    A1["1. Fetch the document<br/>store it, record a hash"]:::det
    A2{"2. Is this really the document?<br/>check for a phrase only it contains"}:::det
    A3{"3. Has it been amended since?"}:::det
    A4["4. Read it and write down its rules"]:::ai
    A5{"5. Is every quote really in the document?"}:::det
    A6{"6. Valid fields and vocabulary?"}:::det
    A7{"7. Expert signs the rule off"}:::human
    A8[("The rules table")]:::store

    A1 --> A2
    A2 -- "no: we saved the website's<br/>menus and headings,<br/>not the law" --> A1
    A2 -- yes --> A3
    A3 -- "superseded" --> A1
    A3 -- current --> A4 --> A5
    A5 -- "quote not found" --> A4
    A5 -- yes --> A6
    A6 -- "no: bad field or<br/>unknown vocabulary" --> A4
    A6 -- yes --> A7
    A7 -- "yes" --> A8
    A7 -- "not yet looked at" --> A8

    B0["0. Someone watches the content<br/>and writes down what happens,<br/>with timecodes"]:::scope
    C1["0b. Turn the description<br/>into an embedding"]:::scope
    C2{"0c. Have we answered this before?<br/>same country, service, slot<br/>AND similar enough text"}:::scope
    C3[["Serve the stored answer"]]:::scope
    C4["0d. A source was amended:<br/>drop every stored answer<br/>that cites a rule from it"]:::scope
    C5[("Stored answers")]:::scope

    B1["8. Read the content description"]:::ai
    B2{"9. Categories in the controlled list?"}:::det
    B2a["9b. A person adds the new<br/>category, or rejects it"]:::human
    B3{"10. Does an existing age rating<br/>ban this outright?<br/>(BBFC R18, or refused a rating)"}:::det
    B4["11. Pick the rules that could apply"]:::det
    B5["12. Decide: rating, hours, conditions"]:::ai
    B6{"13. Does every claim cite a real rule?"}:::det
    B7{"14. Clear-cut, and nothing missing?"}:::det
    B8[["Answer, with its rules"]]:::out
    B9[["A person decides,<br/>rule and quote attached"]]:::human

    B0 -.-> C1
    C1 -.-> C2
    C5 -.-> C2
    C2 -. "hit" .-> C3
    C2 -. "miss, or judgement<br/>was involved" .-> B1
    A3 -. "superseded" .-> C4
    C4 -.-> C5
    B8 -. "only if every rule it cited<br/>was a bright line" .-> C5

    B1 --> B2
    B2 -- "a word for a<br/>category we have" --> B1
    B2 -- "a kind of content<br/>the list lacks" --> B2a
    B2a -- "added" --> A4
    B2 -- yes --> B3
    B3 -- "yes" --> B8
    B3 -- no --> B4 --> B5 --> B6
    A8 -- "approved rows only" --> B4
    B6 -- "invented a rule" --> B5
    B6 -- yes --> B7
    B7 -- yes --> B8
    B7 -- no --> B9

    classDef det fill:#e9f5ec,stroke:#2f7d55,stroke-width:2px,color:#143
    classDef ai fill:#efeaf7,stroke:#5e42a6,stroke-width:2px,color:#231
    classDef human fill:#fdf0e3,stroke:#b4690e,stroke-width:2px,color:#331
    classDef store fill:#f1efea,stroke:#6b6b6b,stroke-width:1px,color:#222
    classDef out fill:#fff,stroke:#2f7d55,stroke-width:2px,color:#143
    classDef scope fill:#fafafa,stroke:#9a9a9a,stroke-width:2px,stroke-dasharray:5 4,color:#555
```

Steps 1 to 7 run **once per legal document**, and again when the law changes. Steps 8 to 14
run **once per showing**.

### What happens when a rule does not pass

Step 7 is not pass-or-bin. A rule that fails a check gets a **status**, and the status decides
whether a decision may use it. Only `approved` rules are ever handed to step 12.

```mermaid
flowchart LR
    N["A rule is written<br/>from a source document"]:::ai
    Q{"Is the quote really<br/>in the document?"}:::det
    V{"Is the source current,<br/>and is it the primary text?"}:::det
    E{"Expert agrees?"}:::human

    N --> Q
    Q -- no --> FIXQ["Fix the quote<br/>or the source"]:::ai
    FIXQ --> Q
    Q -- yes --> V
    V -- "source not collected" --> D["DRAFT<br/>we know the rule exists,<br/>not what it says"]:::bad
    V -- "source is out of date" --> U["UNVERIFIED<br/>quote is real,<br/>vintage is wrong"]:::bad
    V -- ok --> E
    E -- no --> U
    E -- yes --> A["APPROVED<br/>usable for decisions"]:::good

    A -- "the law changes" --> S["SUPERSEDED<br/>true about the past,<br/>end-dated, kept"]:::old
    S -.-> A2["A new APPROVED row<br/>replaces it"]:::good

    D -. "source finally collected" .-> Q
    U -. "re-checked against<br/>the current text" .-> Q

    classDef det fill:#e9f5ec,stroke:#2f7d55,stroke-width:2px,color:#143
    classDef ai fill:#efeaf7,stroke:#5e42a6,stroke-width:2px,color:#231
    classDef human fill:#fdf0e3,stroke:#b4690e,stroke-width:2px,color:#331
    classDef good fill:#d6eade,stroke:#2f7d55,stroke-width:2px,color:#143
    classDef bad fill:#f6dada,stroke:#9e2b2b,stroke-width:2px,color:#411
    classDef old fill:#f1efea,stroke:#6b6b6b,stroke-width:2px,color:#333
```

**How a rule actually ends up in each state.** Every one of these has happened here.

| Status | How it happens | The real case |
|---|---|---|
| `draft` | You learn a rule exists from a source that **is not the rule**. You can write down that it binds, but not what it demands. | French channels each sign an individual agreement with the regulator. An enforcement decision cited those agreements, which proved they exist and bind, but the agreements themselves are not published centrally. |
| `unverified` | Either the source could not be read yet, or it was read and something is off. The quote can be real and the document real while the **vintage** is wrong. | Two rules cited guidance from 2015 that a 2018 statement had restructured. Correct quote, correct document, superseded edition. |
| `superseded` | The law changed. The old row is not wrong; it was correct until a date. | A 2014 amendment broadened a French category. The old wording stays, end-dated, because explaining a decision made in 2013 needs the rule as it stood in 2013. |
| `approved` | Quote verified against the stored document, fields valid, source current, expert agreed. | 103 of 103 rules. |

Two things follow from this that are easy to miss.

**A rule can be correct and still unusable.** `draft` is not a complaint about quality. It is the
table being honest that a whole layer of binding obligation exists which it cannot describe,
so a decision for a French channel should say "check the channel's own agreement" rather than
implying the general law is the whole answer.

**Deleting a superseded rule breaks the past.** The question a regulator asks is "why did you
clear that programme in 2013?", and answering it needs the rule as it was then, not as it is
now.

### Why only three steps use a model

The rule applied here is: **if a step can be done by comparing strings, it must not be done by
a model.** A model asked a question code can answer is slower, costs more, and can be talked
out of the right answer. Code cannot be talked out of anything.

So every model step had to justify itself:

| Step | Could code do it? | Why not |
|---|---|---|
| 4. Read a document, write down its rules | **No** | Turning prose law into structured rules needs reading comprehension. There is no pattern to match. |
| 8. Describe the content | **No** | "Two teenagers share a cigarette, played for laughs" has to become a category, a treatment and a timecode. Nothing mechanical does that. |
| 12. Decide | **Partly, and the part that can is not done here** | Applying a fixed time to a known category is a lookup. Weighing whether violence is "presented repeatedly" is not. Step 11 hands over only the rules that could apply, so the model is asked the narrow question and not the broad one. |

And every model step is **gated by cheaper checks first**:

- Step 4 never runs on a file that failed step 2. Asking a model to extract rules from a
  file that turned out to hold the website's menus, not the law, costs a model call and
  produces confident nonsense.
- Step 12 never runs when step 10 has already settled it. A BBFC R18 certificate is an
  outright ban: nothing in any context lifts it, so asking a model can only introduce a chance
  of it being argued away.
- Step 12 is not asked about rules step 11 already excluded.

### What each check catches

| Check | Catches | Already caught, for real |
|---|---|---|
| 2. Is this the document? | A saved file that holds the website around the document rather than the document | A French source saved as 12,493 characters of menus, headings and links with none of the law in it. It passed a length test, because it was long |
| 3. Amended since? | A rule whose wording a later instrument replaced | Twice. Both times the old version was internally consistent and agreed with other sources of the same age |
| 5. Quote really present? | Paraphrase passed off as a quotation, wrong source cited | Four quotes, including one with a full stop added that cut off the words making the rule enforceable |
| 6. Valid vocabulary? | A value outside the list, which matches nothing and errors nowhere | Two spellings of one service type, which silently dropped a rule from every decision using the other |
| 9. Known category? | An observation that would match no rule | Enforced before the decision step rather than discovered after |
| 13. Claims cite real rules? | A decision citing a rule that does not exist | |
| 14. Clear-cut? | Automating a judgement call | 38 of 103 rules are judgement calls and route to a person |

Every defect in that right-hand column **looked completely fine**. None was found by rereading.
Each was found by something mechanical comparing the work against a source outside it.

## Which steps belong to which task

All fourteen numbered steps are **Task 1**. Task 2 adds no steps: it asks what breaks when
the same flow runs for thirty countries instead of two. The dotted boxes are in neither, and
are drawn only because the flow does not make sense without them.

| Steps | Task 1 | What Task 2 asks about them |
|---|---|---|
| 0, someone watches the content | Out of scope. The assignment starts from a description | Out of scope, and the weakest link in the chain |
| 0b, 0c, 0d, answer from stored answers | Out of scope | Cost per decision, and what an amendment has to invalidate |
| 1, 2, 3, fetch and validate the document | Deliverable: *sources, with links and scope* | Source collection at scale: who finds them, how you know a document is current, what happens on amendment |
| 4, write down the rules | Deliverable: *the table of rules* | Rule representation. One schema for every country; which differences are data rather than code |
| 5, 6, quote and vocabulary checks | **Not asked for** | **Testing for correctness.** Task 2 asks this directly, and these are the answer |
| 7, expert sign-off | Not asked for | **Automate versus local expert.** The one step that cannot scale by engineering |
| 8, describe the content | Deliverable: *the prompt* | Shared. Same everywhere |
| 9, 10, vocabulary and prohibition gates | Not asked for | Shared logic, country data |
| 11, pick the rules | Deliverable: *the prompt* | Where "what looks shared and is not" bites |
| 12, decide | Deliverable: *the prompt*, plus *reasoning with rule references* | Shared. The three passes do not change per country |
| 13, 14, citation and clear-cut checks | Deliverable: *missing information or need for human review* | **Measurement.** The escalation rate is the metric that says whether this is working |

Two things worth drawing out.

**The checks were not asked for by Task 1.** Nothing in the brief requires quotes to be
verified. They exist because Task 2 asks how you know the rules are right, and that needs a
mechanical answer rather than an assurance. They then earned their place in Task 1 by catching
four defective quotes, two rules citing the wrong document, a reversed rule and two silently
dropped vocabularies.

**Steps 1 to 7 run per document; 8 to 14 run per showing.** That split is the architecture.
Merge them and nothing separates "what the rule says" from "what I decided", so a misreading
cannot be caught and the quote check has nothing to check against.

## One rule, followed all the way through

A real example. The same film, on two different channels.

```mermaid
flowchart LR
    A["Ofcom rulebook<br/>Section One, rule 1.24"] --> B["Stored as one row<br/>'any time, IF a PIN<br/>gate is in place'"]
    B --> C["A film is checked<br/>for a paid film channel"]
    C --> D["Rating<br/>the UK gives none"]
    C --> E["Hours<br/>any time"]
    C --> F["Other conditions<br/>PIN, on by default"]
    E --> G{"Do the conditions<br/>change the hours?"}
    F --> G
    G --> H["Yes. With the PIN in place<br/>the 9pm watershed<br/>does not apply at all"]
    H --> I["Answer: it may run at 2:30pm,<br/>but ONLY because of the PIN"]
```

The thing to notice is the question in the middle. The hours and the PIN are worked out
**separately** and then checked against each other, because the PIN changes the hours.

Say only "any time" and you have dropped the condition that earned it, and a channel without
a PIN would act on it. Say only "not before 9pm" and you have missed that a PIN would lift
that, which costs the channel a slot it was entitled to. Both are wrong, in opposite
directions.

Put the same film on an ordinary free-to-air channel with no PIN and the answer is 9pm. Same
film, same certificate, nothing re-edited.

## The steps in more detail

### Steps 1 to 7: turning documents into a table

Prompt: `prompts/BUILD_rules_from_sources.md`

This takes **one legal document** and produces **rows**. Its
job is reading law. It runs 20 times, once per source, and again whenever a regulator amends
something.

Each row carries a `verbatim_quote` that appears character for character in the stored file.
**All 103 approved rules do**, and a rule without one fails the build.
`pipeline/verify_rules.py --with-quotes` checks every one mechanically. A row that fails
does not ship.

**Step 2 is asking whether the file we saved is the law or just the website around it.** When
you save a page, you can end up with the menus, the headings, the cookie banner and the links
down the side, and none of the actual text, because some sites draw the text with JavaScript
after the page arrives. That happened here: one French source saved as 12,493 characters of
menus and links with not a word of the law in it. It passed a length check, because it was
long. So the test is not "is this file big enough", it is "does this file contain a phrase
that could only appear in this particular document". If not, it goes back to step 1 to be
fetched a different way.

**If step 6 says no**, the row goes back to step 4 to be written again. Step 6 is checking
two different things. One is a field that is empty or impossible, a `service_type` left
blank, an `authority_rank` of 11. The other is a value outside the controlled list, which is
the dangerous one, because nothing errors: the row sits in the table looking fine and matches
no lookup. Two real bugs in this project were exactly that.

**Step 7 is a gate on being used, not a gate on being stored.** A rule can reach the table
without anyone signing it off. It arrives as `draft` or `unverified` instead of `approved`,
and the decision engine only ever reads `approved` rows, which is the `approved rows only`
arrow on the diagram. So the honest answer to "can a rule get into the table without an
expert?" is yes, and it will be ignored until one looks at it. That is deliberate. The
alternative is that a rule nobody has reviewed yet has nowhere to live, so it gets held
outside the system in someone's notes, and then it is not quoted, not checked and not
counted. Better in the table and visibly unusable.

### Step 0: someone watches the content

**This is outside the project and is drawn with a dotted border for that reason.** The
assignment starts from a content description that includes events and timecodes. Something
has to produce that description, and in a real system it is either a person watching the
programme or a vision model doing it, but neither is built here and neither is specified.

It is worth being blunt about this, because it is the weakest link in the whole chain. Every
careful thing downstream rests on the description being accurate and complete. If the
description misses a stabbing, no rule fires on a stabbing, and the system will answer
confidently and be wrong, with a full citation trail behind the wrong answer. Nothing in the
pipeline can detect that, because the pipeline never sees the video.

### Steps 0b to 0d: answering from stored answers

**Also dotted, also not built.** This is a cost idea, so it belongs to the scaling question
rather than to Task 1. The same content gets asked about repeatedly: a film goes out, goes out
again on the timeshift service, goes out again next quarter, goes out on a sister channel.
Running the whole chain each time pays for an answer that has not changed.

The shape is: embed the description, look for a stored answer that is close enough, and serve
it instead of deciding again. What follows is what would have to be true for that to be safe,
because a wrong cached answer is worse than a slow one. It arrives with the same confident
citations as a fresh answer and nothing downstream re-examines it.

**The key cannot be the content alone.** This system decides about a *transmission*, not
about an asset. Country is necessary and nowhere near sufficient. Test cases TC-01 and TC-02
in this repo are the same film with identical content on different services and they get
different answers, so a cache keyed on content and country would serve one of them the other's
answer. The key has to carry everything the decision actually turned on: country, service
type, intended slot, the date, and the version of the rules in force. Anything the decision
depended on and the key omits is a wrong answer waiting to be served.

**Similarity thresholds fail in the dangerous direction.** Cosine similarity and ROUGE-L both
reward overlapping wording. Two descriptions that overlap almost entirely can have opposite
legal outcomes, and the differences that flip an outcome are short. "A man is stabbed" and
"a man is stabbed, blood is visible" score very close together and sit on opposite sides of a
real threshold. Negation is worse still: embeddings are famously weak at it, so "no drug use
is shown" and "drug use is shown" can land nearer each other than either lands to an unrelated
description. The expensive error here is not a missed hit, it is a near-miss served as a hit.

Which means the threshold is not something to set by eye and tune later. The question to
answer with data is not "how similar are these two descriptions", it is **"of all the pairs
this threshold would call a match, what fraction had a different answer?"** That number has to
be zero on a labelled set before anything is served, and the set has to be built from pairs
chosen to be adversarial, differing by one clause, by a negation, by a timecode. A threshold
validated on randomly drawn pairs will look excellent and tell you nothing, because random
pairs are easy.

**Do not store judgement.** On the diagram the arrow into storage is conditional: an answer is
only kept if every rule it cited was a bright line. A `judgment_based` rule routes to a person
precisely because the answer depends on weighing this material in this context, and that
weighing is not transferable to the next piece of content that happens to be worded similarly.
Caching a human's judgement and replaying it automatically converts a careful decision into an
unreviewed one, which defeats the reason it went to a human.

**Invalidation is the part this repo is already set up for.** Step 3 asks whether a source has
been amended; that check is the trigger. The useful version is not a blanket flush. Every
stored answer records the `rule_id`s it relied on, so an amendment only has to drop the
answers that cite a rule from the amended document. A French amendment leaves the UK answers
alone, and an amendment to one Code section leaves answers that never touched it alone. That
matters at thirty countries, where a blanket flush on any amendment anywhere means the cache
is almost always cold and was never worth building.

One more thing an amendment should do: keep a sample of what it dropped and re-decide those
from scratch, then compare. If the answers come back identical, the amendment did not touch
anything that mattered, and that is worth knowing. If they differ, the cache was serving stale
law, and you now know for exactly how long and to whom.

### Step 8: describing the content

Prompt: `prompts/RUN_1_describe_content.md`

This takes a **content description** and produces **timecoded
observations**. Its job is reading content.

It **does not know the rules exist**, and that is the point. An extractor that knows the
thresholds shades its descriptions toward the rating it expects. Write "graphic violence"
instead of "a man is struck with a bottle, blood is visible" and the decision has already been
made, invisibly, by an adjective.

It also records what it was **not** told. `not_stated` is a deliverable, not an apology.

### Steps 9 to 11: gates, then picking the rules

Code, not a prompt: `pipeline/precheck.py` then `pipeline/run_decision.py`

`precheck.py` stops the run rather than warning about it, and says which of the two gates
stopped it:

| exit | meaning |
|---|---|
| `0` | both gates clear, continue to the decision prompt |
| `1` | a certificate triggers an absolute prohibition. The answer is already known, so no model is asked |
| `2` | the extraction is unusable: a category outside the controlled list, or output that is not valid JSON. Fix and re-run |

Exit `2` matters more than it looks. An out-of-vocabulary category does not cause an error. It
causes the observation to match no rule, so the answer comes back looking complete with that
observation silently absent, which is the failure mode this whole pipeline is built against.

**Why would an unknown category come out at all?** Step 8 is a model writing words. The list
of categories is closed, but nothing physically stops the model from writing a word that is
not on it. Almost always this is a wording problem rather than a real one: `self-harm` for
`self_harm`, `drugs` for `drug_use`, a plural, a synonym. The fix is to run step 8 again, and
that is the loop on the diagram.

**But sometimes the list really is missing something**, and that is the case the old diagram
got wrong. If a description contains a kind of content the vocabulary has no slot for, running
step 8 again cannot help. The model would be asked to describe the same thing with the same
closed list and would fail the same way forever. So there is a second branch now: a person
decides whether this is genuinely new, and if it is, they add it to the vocabulary and the
affected rules are rewritten at step 4. That is not a loop, it is an exit.

This is rarer than the wording case, but it is not hypothetical. The categories were derived
from the content two regulators thought worth writing rules about by a particular date.
Deepfakes, AI-generated likenesses and self-harm challenge content all arrived after rules
elsewhere already existed for them. A closed list has to be able to grow, and the decision to
grow it is a judgement about what the regulator would consider a distinct kind of harm, which
is exactly the sort of judgement that should not be automated.

**Step 10, "does an existing age rating ban this outright?"** This means a rating the content
already carries from somewhere else, before any broadcast question is asked. A film released
in UK cinemas or on DVD has been rated by the BBFC, and that rating travels with it. Two of
those ratings end the question immediately: **R18**, which is the category for material sold
only in licensed sex shops, and **refused classification**, meaning the BBFC would not give
it a rating at all. Neither may be broadcast, at any hour, on any service, under any
condition. So if the description says the film carries one of those, the answer is known
before any rule is weighed and no model is asked. That is why it is a green code box and not
a purple one, and it is a string comparison, nothing more.

Note what it is **not**. It is not the broadcast decision, and a cinema rating of 18 does not
by itself prohibit anything on television, it just makes the scheduling question harder. Only
those two specific outcomes are absolute.

Then `run_decision.py` picks the rules that could apply: matching country, matching service
type, matching content category, plus a set that is **always** included.

That last part exists because of a real bug. Access-control rules describe how a programme is
*delivered*, not what is in it, so no content description ever mentions them, so a
category-based filter dropped them every single time. The rule defining what a PIN gate must
be never reached the decision engine, while the rule granting an any-hour permission
*conditional on that gate* did.

### Steps 12 to 14: deciding

Prompt: `prompts/RUN_2_decide.md`

This applies only the rules it was handed. It never recalls regulation,
and it cites a `rule_id` for every claim.

It runs three passes that are deliberately independent: classification, hours, other
restrictions. Then it compares them, because in these two countries they come apart in both
directions.

## Why the rules live in a table rather than in the prompt

Three reasons, all learned the hard way.

**Auditability.** Every decision cites a `rule_id` resolving to a row with a clause reference
and a quote checked against the source. A reviewer can verify any claim without reading the
prompt or trusting its author. The verifier reports how many rows carry a quote, not only how
many passed, because a count of the rows that opted in will always report success.

**Reliability.** Feeding whole legal codes into a decision means re-deriving the law on every
request, slightly differently each time. Here a rule is read once, checked once, signed off
once.

**Maintainability.** When a regulator amends something, you edit a row and version the old
one. You do not re-read everything. This matters more than it sounds: two of the worst errors
in this project were rules carrying wording that an amendment had replaced, and both survived
review because the superseded version was internally coherent and corroborated by other
sources of the same vintage.

## Reading a rule row

```
rule_id             UK-SCH-007
authority_rank      1                 lower wins when rules conflict
service_type        all_linear_tv     controlled vocabulary, enforced in CI
content_category    scheduling_general
classification      exempt
time_rule_machine   any_time;override=watershed_disapplied_when_mdp_in_place
determinacy         bright_line       how to score it
ambiguity_flag      clear             how confident the extraction is
verbatim_quote      "does not apply to channels when mandatory daytime protection"
source_doc          UK-S1
clause_ref          Rule 1.4 (meaning of the watershed)
```

Two fields are easy to confuse and must not be merged. **`determinacy`** describes the rule:
is the line bright, conditional, or a judgment? **`ambiguity_flag`** describes the extraction:
are we sure we read it right? A crisp rule nobody is sure was transcribed correctly is
`bright_line` + `unverified`, and merging the two loses exactly that state.

## Running it

```bash
pip install openpyxl pypdf

python pipeline/verify_rules.py --with-quotes        # does the table hold up?
python pipeline/run_decision.py --countries UK FR \
    --service free_to_air --categories violence      # assemble a decision context
python pipeline/precheck.py run1_output.json          # deterministic gates, before any model
python pipeline/build_timeline.py                    # regenerate docs/timeline.html
```

`docs/timeline.html` shows, for a chosen country and service, which rules bite at which hour
across a 24-hour day. It is built from the table, so a rule appears only if its token encodes
a real clock time. Rules whose restriction is not a time are listed separately rather than
drawn at an invented hour.
