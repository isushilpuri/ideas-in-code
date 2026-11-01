from agents import DECAY, SETTLE, WEIGHTS, respond, simulate
from thoughts import N_THOUGHTS, generate_thoughts

NEGATIVE = ("What if I fail?", "negative", 0.5)
NEUTRAL = ("I wonder what's for dinner.", "neutral", 0.5)


def test_stream_is_reproducible_and_sixty_long():
    assert generate_thoughts() == generate_thoughts()
    assert len(generate_thoughts()) == N_THOUGHTS == 60


def test_intensities_stay_in_range():
    assert all(0.2 <= t[2] <= 1.0 for t in generate_thoughts())


def test_a_reacts_more_than_b_to_the_same_thought():
    assert respond(0.0, NEGATIVE, "A") == 0.5 * WEIGHTS["A"]
    assert respond(0.0, NEGATIVE, "B") == 0.5 * WEIGHTS["B"]
    assert WEIGHTS["A"] > WEIGHTS["B"]


def test_observing_still_feels_the_thought():
    assert respond(0.0, NEGATIVE, "B") > 0


def test_neutral_thought_settles_and_never_goes_negative():
    assert respond(1.0, NEUTRAL, "A") == DECAY - SETTLE
    assert respond(0.0, NEUTRAL, "B") == 0.0


def test_histories_cover_every_thought_and_a_stays_above_b():
    stream = generate_thoughts()
    a, b = simulate(stream, "A"), simulate(stream, "B")
    assert len(a) == len(b) == N_THOUGHTS + 1
    assert all(x >= y for x, y in zip(a, b))
    assert max(a) > max(b) > 0
