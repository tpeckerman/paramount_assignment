# Task 1, Design choices, and the tools used

Everything the assignment asks for, with the reasoning. Where a choice was wrong and got
changed, the original is stated rather than quietly replaced, the corrections are the most
informative part of this.

| Deliverable | Where |
|---|---|
| Sources and rule table | `sources/originals/MANIFEST.csv`, `rules/RULES_TABLE_v1.xlsx`, `rules/csv/` |
| The prompt | `prompts/STAGE1_extract.md`, `prompts/STAGE2_apply.md` |
| The prompt that *builds* the table | `prompts/STAGE0_build_rules_table.md` |
| Test cases and results | `tests/CASES.md`, `tests/RESULTS.md` |
| Scope reasoning | `SCOPE_DECISION.md` |
| Design choices and tools | this file |

**Current state:** 90 rules, 87 approved, 12 of 20 sources collected, 32 quotes verified
against stored sources, 0 failing.

---

## Design choice 1, Two stages, not one

**Chosen:** Stage 1 turns the description into timecoded observations. Stage 2 applies rules.
Stage 1 **does not know the rules exist.**

A single prompt doing both is smaller and cheaper. It is also unauditable: there is nothing
separating "what the rule says" from "what I decided", so a misreading cannot be caught. And
an extractor that knows the thresholds will shade its descriptions toward the rating it
expects, write "graphic violence" rather than "a man is struck with a bottle; blood is
visible" and the decision is already made, invisibly, by an adjective.

**Cost:** two calls, and Stage 1 sometimes produces observations no rule uses. That turned
out to be a feature. An observation matching no rule is a **coverage gap**, which is how you
discover a missing rule.

## Design choice 2, Compile the rules once, query them many times

**Chosen:** source documents → rules table → decisions read the table.

The alternative is feeding regulatory text to the model per decision. That re-reads the law
thousands of times, re-derives it slightly differently each time, and leaves no citation that
resolves to anything. Here a rule is read once, checked once, signed off once. Updating a rule
is a row edit with a provenance trail. The decision context is roughly 5× smaller than the
source corpus, and that corpus is still only 12 of 20 documents, so the real ratio is far
higher.

**Cost:** the table can go stale. That is why the currency gate and the amendment tracking
exist, and they exist because this failure happened twice.

## Design choice 3, Three output axes, not two

The assignment warns against assuming age rating implies broadcast hours. The warning
understates it. There are **three** outputs and they are **substitutes**:

```
UK-FLM-003   Rule 1.24   any_time; requires=mandatory_daytime_protection
UK-SCH-007   Rule 1.4    the watershed does not apply while that gate is in place
```

Permitted at any hour, weekday afternoons included, *provided* a PIN gate is on by default.
Report "any time" and you dropped the condition that earned it. Report "barred before 21:00"
and you missed that a technical measure lifts it. **Wrong in both directions.**

This is not a quirk. The EU framework requires an *outcome* and permits scheduling **or**
technical measures as alternatives, so any country implementing it will show the same shape.

## Design choice 4, Determinacy and ambiguity are separate fields

`determinacy` describes the rule: bright line, conditional, or judgment. `ambiguity_flag`
describes my extraction: clear, conflicting, translation-uncertain, unverified.

Merging them loses the most useful state: *this rule is perfectly crisp and I am not confident
I captured it correctly.* Scoring uses the first; usability uses the second.

## Design choice 5, Every claim carries a verbatim quote

The single highest-value decision. Each rule stores a quote that must appear
character-for-character in the stored source, checked mechanically.

The moment real sources landed, it failed four rules. Two were paraphrases I had written as
quotes. One cited the wrong document. The fourth is the one worth remembering: it ended
`"...post-0530."` with a full stop **I had added**, cutting the sentence before the words
"which cannot be removed by the user", the exact words that make the rule enforceable. A
truncated clause dressed as a complete sentence.

I could not have found any of these by re-reading my own work.

## Design choice 6, Scope by escape clause, not by keyword

I first scoped the Broadcasting Code by searching for one phrase and concluded seven of ten
sections were irrelevant. That was wrong. Section Three enters through a different door: its
rules are permitted "except where it is justified by the context", and *context* is a defined
term whose third factor is **the time of broadcast**.

A single lexical test is not a scoping method. The corrected test enumerates the escape
clauses. Sections Five to Eight use "editorially justified", which does **not** import the
context definition and so never turns on the hour, verified against the live text, not
assumed.

**Scope boundary:** this tool covers the age/time decision and anything that conditions or
substitutes for it. It stays silent on impartiality, fairness, privacy and commercial
compliance. The news section still binds this broadcaster, it is excluded because it yields
no rating and no hour, not because it does not apply, and it is retained as a *router*, since
news is regulated elsewhere and applying a harm rule to it would be wrong.

## Design choice 7, "Not stated" is an output, not a failure

The worst outcome is a confident decision on absent information. `not_stated` is a
first-class value and Stage 2 is forbidden from resolving it by assumption, it branches and
labels instead. Service type is the critical one: French hours depend on it, so a single
unqualified French answer is almost always wrong.

---

## Failure analysis, and the improvement I can demonstrate

Five test cases. One failed, and finding **two** bugs from one case is the result I would
most want a reviewer to look at.

TC-01 and TC-02 are the same film with **identical content** on different services. Any
system deriving hours from the rating must answer both alike, and must therefore be wrong
about one.

**Bug 1. The rule defining the condition never reached the engine.** `UK-ACC-001` defines
"mandatory restricted access" as a gate that *cannot be removed by the user*. The engine
selects rules by the content categories present in the description. `access_control` is not a
content category, because **a PIN is not content**. So it was filtered out every time. The
engine would read `requires=mandatory_daytime_protection` with no row saying what that meant,
and would have accepted a parental control the viewer can switch off, a breach from the
first frame.

*Fix:* `access_control`, `audience_information` and `trailers` are force-included regardless
of content. The lesson is larger than the fix: **filtering rules by content categories
silently removes every rule about delivery.**

**Bug 2, two spellings of one service.** After that fix the rule still did not arrive.
`premium_subscription` in one row, `premium_subscription_film` in another, no controlled
vocabulary, rule silently dropped.

*Fix:* vocabulary normalised, and the verifier now **fails** on any unknown `service_type`.

**Why this matters more than a passing test:** neither bug errored. Neither produced a
visibly wrong answer. Both produced complete-looking output with a rule missing, which is
indistinguishable from correct output until someone is in front of a regulator.

---

## Known weaknesses

- **28 of 90 rules are judgment-based and uncalibrated.** One enforcement precedent collected.
  The table can say "a human must decide"; it cannot say where the line sits. The regulator's
  guidance notes contain worked examples that would fix this, they are among the 8
  uncollected sources.
- **Author equals grader.** I wrote the rules, prompts, tests and checker, and executed them.
  The failures are the trustworthy part. Bright-line rules need independent re-derivation by
  someone who has not seen the table.
- **Two rules sit at `unverified`** (C-14) because they cite guidance predating a 2018
  restructure. Flagged, not used.
- **French rules are quoted from an official English translation** that states only the French
  is authentic.
- **Channel-level agreements not collected.** In France these can be stricter than the law.
- **Tested only on cases I wrote**, never on a real asset.

---

## Models and tools

**Claude Opus 5**, research, source analysis, rule extraction, pipeline code, and executing
the test cases. One sub-agent run for independent verification of 22 downloaded files, used
specifically because my own substring matching had already produced two false positives.

**Python 3**, `openpyxl` (table), `pypdf` (PDF extraction), `csv`/`json`, `unicodedata` for
the accent and ligature folding the French quote checks need.

**Pipeline** (`pipeline/`): `build_rules_table.py`, `verify_rules.py` (integrity + quote
check + vocabulary), `fetch_originals.py`, `fetch_with_browser.py` (Playwright),
`import_saved.py`, `build_worklist.py`, `run_decision.py`.

**GitHub Actions**, CI runs the verifier, the quote check and a regenerate-and-diff of the
CSV mirrors so the binary table cannot drift unnoticed. A second workflow fetches sources.

**Google Workspace / Colab**, `pipeline/COLAB_rule_pipeline_starter.ipynb` converts the table
to a Sheet with change detection and versioning, for the non-engineers who maintain rules.

**Not used, deliberately:** no attempt to defeat Cloudflare or AWS WAF challenges. Blocked
documents were listed for manual retrieval instead, with a console snippet that verifies each
save contains the phrase identifying the real document.
