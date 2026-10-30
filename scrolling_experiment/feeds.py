"""
Three toy social-media feeds. Each one returns the reward of the next post.

An illustrative model, NOT a measurement of real feeds or real people.
Every number below is an assumption we chose.
"""

# The first two feeds pay the same on average: 1.0 per post.
STEADY_REWARD = 1.0      # every post is equally interesting


def predictable_feed(rng):
    return STEADY_REWARD


JACKPOT_CHANCE = 0.2     # 1 post in 5 is genuinely entertaining...
JACKPOT_REWARD = 5.0     # ...and the other 4 are completely forgettable


def unpredictable_feed(rng):
    if rng.random() < JACKPOT_CHANCE:
        return JACKPOT_REWARD
    return 0.0


def empty_feed(rng):
    return 0.0  # just disappointment with a Wi-Fi connection


FEEDS = {
    "predictable": predictable_feed,
    "unpredictable": unpredictable_feed,
    "empty": empty_feed,
}
