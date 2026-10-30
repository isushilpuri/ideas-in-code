"""Thousands of simulated scrolling sessions, for every feed."""

import numpy as np

from feeds import FEEDS
from scroller import MAX_SWIPES, scroll_session

SEED = 42
N_USERS = 5000


def simulate(feed, rng):
    return np.array([scroll_session(feed, rng) for _ in range(N_USERS)])


def run_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    return {name: simulate(feed, rng) for name, feed in FEEDS.items()}


def still_scrolling(sessions):
    """Share of users still scrolling at every swipe number."""
    swipes = np.arange(1, MAX_SWIPES + 1)
    return swipes, np.array([(sessions >= n).mean() for n in swipes])
