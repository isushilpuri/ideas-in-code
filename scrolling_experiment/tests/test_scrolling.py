import numpy as np

from experiment import N_USERS, run_experiment, still_scrolling
from feeds import (FEEDS, JACKPOT_CHANCE, JACKPOT_REWARD, STEADY_REWARD,
                   empty_feed, predictable_feed, unpredictable_feed)
from scroller import BOREDOM, MAX_SWIPES, continue_probability, scroll_session


def test_same_average_reward():
    assert JACKPOT_CHANCE * JACKPOT_REWARD == STEADY_REWARD
    rng = np.random.default_rng(0)
    draws = [unpredictable_feed(rng) for _ in range(40_000)]
    assert abs(np.mean(draws) - STEADY_REWARD) < 0.05
    assert np.mean(np.array(draws) == 0.0) > 0.75   # most posts are forgettable


def test_predictable_and_empty_never_vary():
    rng = np.random.default_rng(1)
    assert {predictable_feed(rng) for _ in range(100)} == {STEADY_REWARD}
    assert {empty_feed(rng) for _ in range(100)} == {0.0}


def test_reward_makes_another_swipe_more_tempting():
    assert continue_probability(5.0) > continue_probability(3.0) > continue_probability(0.0)
    assert 0 < continue_probability(-10) < continue_probability(10) < 1
    assert STEADY_REWARD - BOREDOM < 0 < JACKPOT_REWARD - BOREDOM


def test_sessions_are_bounded():
    rng = np.random.default_rng(2)
    for feed in FEEDS.values():
        assert 1 <= scroll_session(feed, rng) <= MAX_SWIPES


def test_story_holds():
    s = run_experiment()
    assert all(v.shape == (N_USERS,) for v in s.values())
    assert s["unpredictable"].mean() > 1.5 * s["predictable"].mean()
    assert s["predictable"].mean() > 2 * s["empty"].mean()
    assert np.percentile(s["unpredictable"], 90) > 2 * np.percentile(s["predictable"], 90)


def test_still_scrolling_curve():
    x, y = still_scrolling(np.array([1, 2, 2, 5]))
    assert x[0] == 1 and len(x) == MAX_SWIPES
    assert list(y[:6]) == [1.0, 0.75, 0.25, 0.25, 0.25, 0.0]


def test_reproducible():
    a, b = run_experiment(), run_experiment()
    assert all((a[k] == b[k]).all() for k in a)
