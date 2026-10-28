import numpy as np

from agent import FACT, NOISE, filtering_agent, find_date, is_relevant, stuffing_agent
from experiment import ANSWER, N_TRIALS, NOISE_LEVELS, build_context, run_experiment


def test_fact_carries_the_answer():
    assert find_date(FACT) == ANSWER


def test_no_noise_note_is_relevant():
    assert is_relevant(FACT)
    assert not any(is_relevant(n) for n in NOISE)


def test_clean_context_is_answered():
    rng = np.random.default_rng(0)
    hits = sum(stuffing_agent([FACT], rng) == ANSWER for _ in range(2000))
    assert 0.93 < hits / 2000 < 0.99


def test_build_context_keeps_exactly_one_fact():
    rng = np.random.default_rng(1)
    ctx = build_context(40, rng)
    assert len(ctx) == 41 and ctx.count(FACT) == 1


def test_filter_strips_clutter():
    rng = np.random.default_rng(2)
    ctx = build_context(100, rng)
    assert [n for n in ctx if is_relevant(n)] == [FACT]
    hits = sum(filtering_agent(ctx, rng) == ANSWER for _ in range(2000))
    assert hits / 2000 > 0.9


def test_experiment_shape_and_story():
    r = run_experiment()
    assert r["stuffing"].shape == (len(NOISE_LEVELS), N_TRIALS)
    s, f = r["stuffing"].mean(axis=1), r["filtering"].mean(axis=1)
    assert s[-1] < s[0] - 0.3          # stuffing drowns
    assert abs(f[-1] - f[0]) < 0.05    # filtering holds
    assert f[-1] > s[-1]


def test_experiment_is_reproducible():
    a, b = run_experiment(), run_experiment()
    assert (a["stuffing"] == b["stuffing"]).all()
