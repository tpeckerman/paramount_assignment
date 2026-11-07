# How it works

How a content description becomes a decision, and where the rules come in.

## The flow

**The process diagram lives in [`TASK2_SCALING.md`](TASK2_SCALING.md#process)**, where it is a
required deliverable. Task 1 asks for sources, rules, a prompt, test cases and results, and
not for a diagram, so there is only one in this repo rather than two that have to be kept in
step with each other. `out_of_scope/docs/diagrams.html` renders it large and scrollable.

This file is the written walkthrough of the same process: what each step does, what it
catches, and why it sits where it does.

Three kinds of step, and the distinction matters more than it looks:

| | |
|---|---|
| 🟩 **Code** | Deterministic. Same input, same output, every time. Costs nothing, cannot be argued with. |
| 🟪 **Model** | Needs reading, weighing or judgment. Used only where code genuinely cannot do the job. |
| 🟧 **Person** | A judgment with consequences, or a decision nobody should automate. |
| ⬜ **Dashed** | Not built in this project. |

Steps 1 to 7 run **once per legal document**, and again when the law changes. Steps 8 to 14
run **once per showing**.

### What happens when a rule does not pass

Step 7 is not pass-or-bin. A rule that fails a check gets a **status**, and the status decides
whether a decision may use it. Only `approved` rules are ever handed to step 12.

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
clear that program in 2013?", and answering it needs the rule as it was then, not as it is
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
| 14. Clear-cut? | Automating a judgment call | 43 of 103 rules are judgment calls and route to a person |

Every defect in that right-hand column **looked completely fine**. None was found by rereading.
Each was found by something mechanical comparing the work against a source outside it.

## Which steps belong to which task

Task 1 asks for four things: **locate official sources and present the rules, with links and
scope**; **a prompt**; **test cases**; **results**. Everything else in this diagram is either
Task 2's territory or out of scope, and is dashed.

**Steps 1 to 3 are dashed, and that is a correction.** Locating the sources is Task 1 and it
was done: twenty documents, collected, with links and scope recorded. But an *automated
system that re-fetches them and watches for amendments* is not a Task 1 deliverable. It is the
answer to Task 2's first question. For Task 1 these steps happened **once**, by hand and with
one-off scripts; the diagram dashes them because what is drawn is the repeating automated
version, which belongs to Task 2.

| Steps | Task 1 | What Task 2 asks about them |
|---|---|---|
| 0, someone watches the content | Out of scope. The assignment starts from a description | Out of scope, and the weakest link in the chain |
| 0b, 0c, 0d, answer from stored answers | Out of scope | Cost per decision, and what an amendment has to invalidate |
| 1, 2, 3, fetch and re-check the document | Collecting them, yes. **Automating it, no** | **Task 2's first question.** Who finds them, how you know a document is current, what happens on amendment |
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

Prompt: `out_of_scope/BUILD_rules_from_sources.md`

**None of this is a deliverable for either task.** Task 1 asks for the sources and a table of
rules, not for a method of producing one. Task 2 asks for a design, meaning a diagram, a
worked rule, a validation plan and metrics; it wants a plan for doing this at scale, not a
working prompt that does it.

So this prompt is apparatus, in the same category as everything in `out_of_scope/pipeline/`. It is
described here because it is how this table was actually built, and a reader who wants to
judge the rules deserves to know what produced them.

This takes **one legal document** and produces **rows**. Its
job is reading law. It runs 20 times, once per source, and again whenever a regulator amends
something.

Each row carries a `verbatim_quote` that appears character for character in the stored file.
**All 103 approved rules do**, and a rule without one fails the build.
`out_of_scope/pipeline/verify_rules.py --with-quotes` checks every one mechanically. A row that fails
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
arrow in the process diagram. So the honest answer to "can a rule get into the table without an
expert?" is yes, and it will be ignored until one looks at it. That is deliberate. The
alternative is that a rule nobody has reviewed yet has nowhere to live, so it gets held
outside the system in someone's notes, and then it is not quoted, not checked and not
counted. Better in the table and visibly unusable.

### Step 0: someone watches the content

**This is outside the project and is drawn with a dotted border for that reason.** The
assignment starts from a content description that includes events and timecodes. Something
has to produce that description, and in a real system it is either a person watching the
program or a vision model doing it, but neither is built here and neither is specified.

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

**Do not store judgment.** On the diagram the arrow into storage is conditional: an answer is
only kept if every rule it cited was a bright line. A `judgment_based` rule routes to a person
precisely because the answer depends on weighing this material in this context, and that
weighing is not transferable to the next piece of content that happens to be worded similarly.
Caching a human's judgment and replaying it automatically converts a careful decision into an
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

Code, not a prompt: `out_of_scope/pipeline/precheck.py` then `out_of_scope/pipeline/run_decision.py`

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
that is the loop back to step 8 in the process diagram.

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
grow it is a judgment about what the regulator would consider a distinct kind of harm, which
is exactly the sort of judgment that should not be automated.

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

That last part exists because of a real bug. Access-control rules describe how a program is
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

**Steps 13 and 14 are code, not the model grading itself:** `out_of_scope/pipeline/postcheck.py`.

Step 13 asks whether every cited `rule_id` actually resolves. The worst failure a tool like
this can have is not a wrong answer, it is **a wrong answer wearing a citation**. "Prohibited
before 22:30 (UK-SCH-012)" reads exactly like a correct answer unless somebody looks
UK-SCH-012 up, and looking it up is a dictionary lookup. It also rejects a citation to a row
that exists but is `draft`, `unverified` or `superseded`, which is worse than citing nothing
because the id resolves and the citation looks sound, and a citation to a rule belonging to
the other country.

Step 14 asks whether the decision routed itself to a person when it had to. Part of that is a
judgment, but a large part is not, and the part that is not belongs here:

- if any rule relied on is `judgment_based`, a person has to see it. That is a property of
  the rule recorded in the table, not a matter of how confident the answer sounds
- if the output claims `confidence: high` while listing missing information, one of the two
  is wrong. Either the missing field would not change the answer, in which case it does not
  belong in `missing_information`, or it would, in which case the confidence is not high
- if observations matched no rule, that is a gap in the table, and a gap is not permission

Exit `0` passes, `1` means it must go to a person and did not say so, `2` means malformed or
badly cited.

What `postcheck.py` deliberately does not check is **whether the answer is right**. Nothing in
it reads the content or weighs a threshold. A decision can pass every check in the file and
still be wrong. These checks establish that it is well-formed, honestly sourced and correctly
routed, which is a floor and not a verdict.

### What is designed but not built

Most of this process is a prompt or a script in this repo that you can run. These parts are
not, and the difference between "designed" and "done" is where this sort of project usually
oversells itself.

| Dashed | Why |
|---|---|
| Automated re-fetching and amendment watching | **Built, but it answers Task 2.** Task 1 asked for the sources to be located and presented, which was done once. A system that keeps re-checking them is Task 2's first question |
| 0, someone watches the content | The assignment starts from a description, so producing one is outside it. Also the weakest link in the chain |
| 0b, 0c, 0d, the answer cache | A cost idea for scale, belonging to Task 2. Nothing is built |
| 7, a country expert signs the rule off | **The one that matters.** No expert signed anything off here. Every row is `approved` because the author approved it, which is conflict C-08 |
| 9b, a person adds a new category | There is a branch for it and a message telling you to take it, but no process behind it |
| A person decides, after escalation | Producing the escalation **is** in scope and is a required deliverable. What the person then does with it is not |

## Why the rules live in a table rather than in the prompt

Three reasons, all learned the hard way.

**Auditability.** Every decision cites a `rule_id` resolving to a row with a clause reference
and a quote checked against the source. A reviewer can verify any claim without reading the
prompt or trusting its author. The verifier reports how many rows carry a quote, not only how
many passed, because a count of the rows that opted in will always report success.

**Reliability.** Feeding whole legal codes into a decision means re-deriving the law on every
request, slightly differently each time. Here a rule is read once and checked once, and is
meant to be signed off once, though see step 7 above for what actually happened.

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

python out_of_scope/pipeline/verify_rules.py --with-quotes        # does the table hold up?
python out_of_scope/pipeline/run_decision.py --countries UK FR \
    --service free_to_air --categories violence      # assemble a decision context
python out_of_scope/pipeline/precheck.py run1_output.json         # gates BEFORE the deciding model runs
python out_of_scope/pipeline/postcheck.py run2_output.json        # citation and escalation checks AFTER
python out_of_scope/pipeline/verify_cases.py                      # do the test cases' claimed outcomes hold up?
python out_of_scope/pipeline/render_answer.py decision.json        # the country-by-country answer table
python out_of_scope/pipeline/build_timeline.py                    # regenerate out_of_scope/docs/timeline.html
python out_of_scope/pipeline/build_diagrams.py                    # redraw the diagrams into docs/
python out_of_scope/pipeline/supersede.py <source_doc>            # close out rules from a replaced document
```

Every path, vocabulary and limit the scripts use lives in `out_of_scope/pipeline/constants.py`, so moving
a file or adding a status is a one-line change in one place. Legal thresholds deliberately
do **not** live there: a constant holding `21:00` would be a rule hiding in a config file,
and rules belong in the table with a quote from the law behind them.

```bash
```

`out_of_scope/docs/timeline.html` shows, for a chosen country and service, which rules bite at which hour
across a 24-hour day. It is built from the table, so a rule appears only if its token encodes
a real clock time. Rules whose restriction is not a time are listed separately rather than
drawn at an invented hour.
