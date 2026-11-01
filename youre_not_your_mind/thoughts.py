"""One stream of thoughts, shared by both minds.

An illustrative model inspired by cognitive defusion. It does NOT model real
brain activity or prove a clinical outcome. Every number is an assumption we chose.
"""

import numpy as np

SEED = 42
N_THOUGHTS = 60

THOUGHT_BANK = [
    ("What if I fail?", "negative"),
    ("Everyone is judging me.", "negative"),
    ("I should have said something different three years ago.", "negative"),
    ("They probably hate me.", "negative"),
    ("I made a mistake.", "negative"),
    ("I'm going to fail.", "negative"),
    ("Maybe things will work out.", "positive"),
    ("That was actually a good day.", "positive"),
    ("I wonder what's for dinner.", "neutral"),
    ("I need to remember that appointment.", "neutral"),
]


def generate_thoughts():
    rng = np.random.default_rng(SEED)
    picks = rng.integers(0, len(THOUGHT_BANK), N_THOUGHTS)
    intensities = rng.uniform(0.2, 1.0, N_THOUGHTS)
    return [(*THOUGHT_BANK[p], float(i)) for p, i in zip(picks, intensities)]
