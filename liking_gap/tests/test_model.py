import numpy as np
import pytest

from liking_gap.analysis import the_durations, the_gap, the_pair, the_signals, the_views
from liking_gap.model import (
    BALANCED,
    INNER_CRITIC,
    MOMENTS,
    Config,
    attention,
    converse,
    guess,
    replay,
    signals,
)


def test_reproducible():
    a, b = converse(), converse()
    assert np.array_equal(a.a_thinks, b.a_thinks)
    assert a.a_likes_b.shape == (1000,)


def test_scores_stay_on_the_scale():
    c = converse()
    for x in (c.a_likes_b, c.b_likes_a, c.a_thinks, c.b_thinks):
        assert x.min() >= 1 and x.max() <= 7


def test_the_gap_leans_one_way():
    g = the_gap(converse())
    assert g["actual"] > g["perceived"]
    assert 0.5 < g["gap"] < 0.75
    assert g["below_line"] > 0.8


def test_no_bias_no_gap():
    g = the_gap(converse(Config(bias=0.0, bias_spread=0.0)))
    assert abs(g["gap"]) < 0.08


def test_the_pair_both_underestimate():
    p = the_pair(converse())
    assert p["a_thinks"] < p["b_likes_a"]
    assert p["b_thinks"] < p["a_likes_b"]


def test_guess_sharpens_with_time():
    rng = np.random.default_rng(0)
    short = guess(np.full(20000, 4.0), 2, 0.0, rng)
    long = guess(np.full(20000, 4.0), 20, 0.0, rng)
    assert long.std() < short.std()


def test_attention_filter():
    assert attention(0.0) == 1.0
    assert attention(1.0) == pytest.approx(0.4)
    s = the_signals(signals(converse()))
    assert s["noticed"] < s["shown"]


def test_memory_systems():
    assert replay(MOMENTS, BALANCED)[-1] > 6
    assert replay(MOMENTS, INNER_CRITIC)[-1] < 3


def test_longer_conversations_keep_the_gap():
    d = the_durations()
    assert [r["minutes"] for r in d] == [2, 5, 10, 20]
    assert all(r["gap"] > 0.5 for r in d)
    assert d[-1]["spread"] < d[0]["spread"]


def test_observer_reads_closer_than_the_pair():
    v = the_views(converse())
    assert abs(v["observer"] - v["actual"]) < abs(v["self_critical"] - v["actual"])
