import numpy as np
import pytest

from imposter_sim.analysis import promotion_story, settles_at, the_gap
from imposter_sim.model import (
    BALANCED,
    DISCOUNTING,
    Config,
    identical_lives,
    interpret,
    run,
)


def test_interpret_moves_toward_the_evidence():
    assert interpret(0.5, True, BALANCED) == pytest.approx(0.61)
    assert interpret(0.5, False, BALANCED) == pytest.approx(0.39)
    assert interpret(0.5, True, DISCOUNTING) == pytest.approx(0.5375)
    assert interpret(0.5, False, DISCOUNTING) == pytest.approx(0.35)


def test_twins_share_one_life_and_diverge():
    t = identical_lives()
    assert len(t.a) == len(t.b) == len(t.succeeded) + 1 == 31
    assert int(t.succeeded.sum()) == 21
    assert t.a[-1] == pytest.approx(0.82, abs=0.01)
    assert t.b[-1] == pytest.approx(0.43, abs=0.01)


def test_run_is_reproducible():
    a, b = run(Config(employees=50, tasks=20)), run(Config(employees=50, tasks=20))
    assert np.array_equal(a.confidence, b.confidence)
    assert a.confidence.shape == (50, 21)


def test_settles_at():
    assert settles_at(0.8, BALANCED) == pytest.approx(0.8)
    assert settles_at(0.8, DISCOUNTING) == pytest.approx(0.5)


def test_the_numbers_the_video_quotes():
    r = run()
    story = promotion_story(r)
    assert story["promoted"] == 261
    assert story["discounting"]["final"] < story["balanced"]["final"]
    gap = the_gap(r)
    assert gap["top_but_doubting"] == 12
