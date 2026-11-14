import numpy as np

from bond_charisma.model import (
    BOND, COPY, INTERACTIONS, SEEKER, TURNS, averages, converse, partners, run, table,
)


def avg(style):
    people = partners()
    return averages(table(style, run(style, people), people))


def test_same_partners_for_everyone():
    assert np.array_equal(partners(), partners())
    assert partners().shape == (INTERACTIONS,)


def test_every_turn_gets_one_reply():
    t = converse(BOND, 0.5, np.random.default_rng(1))
    assert t.redirects + t.questions + t.waits == TURNS
    assert t.fillers <= t.pauses and t.landed <= t.jokes


def test_scores_stay_in_range():
    for style in (SEEKER, BOND, COPY):
        for v in avg(style).values():
            assert 0 <= v <= 100


def test_bond_style_wins_all_four_tracked_scores():
    a, b = avg(SEEKER), avg(BOND)
    for k in ("engagement", "warmth", "confidence", "continue"):
        assert b[k] > a[k]


def test_talking_less_is_not_listening():
    b, c = avg(BOND), avg(COPY)
    assert c["talk_share"] < b["talk_share"]
    assert c["felt_heard"] < b["felt_heard"] - 20


def test_copying_the_surface_is_not_enough():
    a, b, c = avg(SEEKER), avg(BOND), avg(COPY)
    assert c["composure"] > b["composure"]  # he copied the silence
    assert a["warmth"] < c["warmth"] < b["warmth"] - 15  # but not the interest
