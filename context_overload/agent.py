"""
Two tiny toy agents with one job: answer a question from the notes they hold.

This is an illustrative model, NOT a real LLM. The distraction is written
by hand below — every irrelevant note costs the stuffing agent a fixed slice
of accuracy because we say so.
"""

import re

import numpy as np

QUESTION = "When does the customer's contract renew?"
FACT = "Customer contract renews on 14 June."

NOISE = [
    "Meeting notes from last Tuesday: offsite moved to 9 May.",
    "Old log: retry attempt 47 scheduled for 1 March.",
    "Outdated plan (do not use): launch on 2 April.",
    "Coffee machine descaling due on 3 October.",
    "Email thread: 'Quick question' (47 replies).",
    "An old summary of an old summary.",
    "A note saying 'check the previous note'.",
    "Unrelated deployment warning on 12 August.",
    "Someone's lunch preference: no olives.",
    "Fridge inventory: 17 sauces, 0 reasons.",
    "Conflicting instruction from last month: reply in haiku.",
    "The 2019 printer troubleshooting guide.",
]

# Toy-model assumptions: we are programming the failure ourselves.
BASE_SUCCESS = 0.96
DISTRACTION = 0.0045    # accuracy lost per irrelevant note
FILTER_MISS = 0.03      # the filter sometimes throws the fact away too

DATE = re.compile(r"\b\d{1,2} (?:January|February|March|April|May|June|July|"
                  r"August|September|October|November|December)\b")


def find_date(note):
    match = DATE.search(note)
    return match.group(0) if match else None


def stuffing_agent(context, rng):
    """Reads every note it is given, then answers the question."""
    clutter = len(context) - context.count(FACT)
    p_correct = max(0.0, BASE_SUCCESS - DISTRACTION * clutter)
    if FACT in context and rng.random() < p_correct:
        return find_date(FACT)
    decoys = [find_date(n) for n in context if n != FACT and find_date(n)]
    return str(rng.choice(decoys)) if decoys else "I don't know"


def is_relevant(note):
    return "contract" in note.lower()


def filtering_agent(context, rng):
    """Keeps the relevant facts, throws away the clutter, then answers."""
    kept = [note for note in context if is_relevant(note)]
    if rng.random() < FILTER_MISS:
        kept = []
    return stuffing_agent(kept, rng)


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    context = [FACT]
    print("Q:", QUESTION)
    print("A:", stuffing_agent(context, rng))
