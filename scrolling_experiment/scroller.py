"""One simulated user, and the one rule they follow."""

import numpy as np

START_TEMPTATION = 3.0   # you opened the app for a reason
BOREDOM = 1.1            # every swipe costs a little patience
MAX_SWIPES = 300         # the feed never ends; our simulation does


def continue_probability(temptation):
    """More temptation, more likely to swipe again."""
    return 1 / (1 + np.exp(-temptation))


def scroll_session(feed, rng):
    """Swipe until the user gives up. Returns the number of swipes."""
    temptation = START_TEMPTATION
    swipes = 0
    while swipes < MAX_SWIPES:
        reward = feed(rng)
        swipes += 1
        temptation += reward - BOREDOM
        if rng.random() > continue_probability(temptation):
            break
    return swipes
