#!/usr/bin/env python3
"""Every value the pipeline would otherwise hardcode, in one place.

WHY THIS FILE EXISTS

A literal written into a script is fine until it is written into eleven scripts, and then it
is not a value any more, it is eleven values that happen to agree today. This project has
already been bitten by exactly that: `premium_subscription` in one row and
`premium_subscription_film` in another silently dropped a rule from every decision that used
the other spelling. Nothing errored. A rule was just missing.

So: paths, vocabularies, patterns and limits live here, and the scripts import them. Changing
where a file sits, or adding a status, is a one-line edit in one file rather than a search.

WHAT BELONGS HERE AND WHAT DOES NOT

Here: anything two scripts both need to agree on, and anything a person might reasonably want
to change without reading code.

Not here: the rules themselves. Those live in the table with a quote from the law behind each
one, which is the entire point of the project. A constant that encodes a legal threshold
would be a rule hiding in a config file, so `21:00` must never appear in this file.
"""
from __future__ import annotations

import pathlib
import re

# --------------------------------------------------------------------------------------
# Where things live. Everything is derived from ROOT so the checkout can sit anywhere.
# --------------------------------------------------------------------------------------
ROOT = pathlib.Path(__file__).resolve().parent.parent

RULES_DIR = ROOT / "rules"
RULES_XLSX = RULES_DIR / "RULES_TABLE_v1.xlsx"
RULES_CSV = RULES_DIR / "csv" / "Rules.csv"
SOURCES_CSV = RULES_DIR / "csv" / "Sources.csv"
OPEN_QUESTIONS_CSV = RULES_DIR / "csv" / "Open_Questions.csv"

SOURCES_DIR = ROOT / "sources"
ORIGINALS_DIR = SOURCES_DIR / "originals"
INCOMING_DIR = ORIGINALS_DIR / "incoming"
MANIFEST_CSV = ORIGINALS_DIR / "MANIFEST.csv"
EXPECT_JSON = ORIGINALS_DIR / "expect.json"
LOCKFILE = ORIGINALS_DIR / "originals.lock.json"
SOURCE_INVENTORY_MD = SOURCES_DIR / "00_SOURCE_INVENTORY.md"

DOCS_DIR = ROOT / "docs"
TIMELINE_HTML = DOCS_DIR / "timeline.html"
DIAGRAMS_HTML = DOCS_DIR / "diagrams.html"

PROMPTS_DIR = ROOT / "prompts"
DECISION_PROMPT = PROMPTS_DIR / "RUN_2_decide.md"

TESTS_DIR = ROOT / "tests"
CASES_MD = TESTS_DIR / "CASES.md"

HOW_IT_WORKS_MD = ROOT / "HOW_IT_WORKS.md"
TASK2_MD = ROOT / "TASK2_SCALING.md"

# --------------------------------------------------------------------------------------
# Controlled vocabularies. A value outside these does not error, it silently matches
# nothing, which is why they are enforced rather than documented.
# --------------------------------------------------------------------------------------
COUNTRIES = ("UK", "FR", "EU")

STATUSES = ("approved", "draft", "unverified", "superseded")

#: The only status the decision engine may read. Everything else is in the table on purpose
#: and must never reach a decision.
USABLE_STATUS = "approved"

#: A rule that is closed but kept, because a past decision still has to be explainable.
SUPERSEDED_STATUS = "superseded"

#: Describes THE RULE: is the line bright, or is it a judgement?
DETERMINACY = ("bright_line", "conditional", "judgment_based")

#: The determinacy that must always route to a person.
JUDGMENT_DETERMINACY = "judgment_based"

#: Describes THE EXTRACTION: am I sure I read it right? Not the same axis as determinacy,
#: and merging the two loses the ability to say "this rule is clear and I am not confident
#: I captured it".
AMBIGUITY_FLAGS = ("clear", "conflicting_sources", "translation_uncertain", "unverified",
                   "out_of_scope_for_asset_decision")

#: Ambiguity values that are incompatible with an approved rule.
BLOCKING_AMBIGUITY = ("conflicting_sources", "unverified")

#: Marker for a rule that has not been closed out.
OPEN_VALID_TO = "open"

# --------------------------------------------------------------------------------------
# Identifiers
# --------------------------------------------------------------------------------------
RULE_ID_PATTERN = re.compile(r"^(?:UK|FR|EU)-[A-Z]{2,4}-\d{3}$")

#: Loose form, for finding ids mentioned inside free text such as `source_doc`.
RULE_ID_IN_TEXT = re.compile(r"\b(?:UK|FR|EU)-[A-Za-z0-9]{1,4}\b")

# --------------------------------------------------------------------------------------
# Limits and thresholds. These are engineering choices, not legal ones.
# --------------------------------------------------------------------------------------
#: Longest quote to carry in a rule row. Past this, the row wants splitting.
MAX_QUOTE_WORDS = 15

#: A saved page smaller than this is almost certainly an error page rather than a document.
#: Size alone is not sufficient, which is why `expect.json` also checks for a phrase only
#: the real document contains: one French source arrived as 12,493 characters of website
#: menus and passed a length test.
MIN_PLAUSIBLE_DOCUMENT_BYTES = 20_000

HTTP_TIMEOUT_SECONDS = 120
RENDER_TIMEOUT_SECONDS = 300

# --------------------------------------------------------------------------------------
# Presentation. Shared so the generated pages look like one system.
# --------------------------------------------------------------------------------------
#: (background, foreground) per verdict, reused by the answer table and the timeline.
VERDICT_COLOURS = {
    "answered": ("#e9f5ec", "#2f7d55"),
    "human": ("#fdf0e3", "#b4690e"),
    "prohibited": ("#fbeaea", "#a8323b"),
    "neutral": ("#f1efea", "#555555"),
}

#: Matches the step kinds in the HOW_IT_WORKS diagrams.
STEP_COLOURS = {
    "deterministic": ("#e9f5ec", "#2f7d55"),
    "model": ("#efeaf7", "#5e42a6"),
    "person": ("#fdf0e3", "#b4690e"),
    "out_of_scope": ("#fafafa", "#9a9a9a"),
}

UI_FONT_STACK = ('-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
                 "Helvetica, Arial, sans-serif")
MONO_FONT_STACK = "ui-monospace, Menlo, Consolas, monospace"


def relative(path: pathlib.Path) -> str:
    """A path as written in output, so messages do not leak the machine's directory layout."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)
