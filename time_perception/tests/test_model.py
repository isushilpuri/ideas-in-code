import numpy as np

from time_perception.model import (
    AGES, DAYS, LANDMARK, ROUTINE, VARIED, landmarks, live, looking_back, per_week, small_changes, year_share,
)


def test_year_shares_match_the_narration():
    assert [year_share(age) for age in AGES] == [10, 5, 2.5, 1.25]


def test_both_people_get_the_same_365_days():
    assert live(ROUTINE).shape == live(VARIED).shape == (DAYS,)


def test_reproducible_and_bounded():
    a, b = live(ROUTINE), live(ROUTINE)
    assert np.array_equal(a, b)
    assert a.min() >= 0 and a.max() <= 1


def test_variety_leaves_more_landmarks():
    a, b = live(ROUTINE), live(VARIED)
    assert 0 < len(landmarks(a)) < len(landmarks(b))
    assert (a[landmarks(a)] >= LANDMARK).all()


def test_weeks_and_months_count_the_same_days():
    a = live(VARIED)
    assert looking_back(a).sum() == len(landmarks(a))
    assert per_week(a).sum() == len(landmarks(a[: 52 * 7]))


def test_small_changes_add_landmarks_without_touching_the_rest():
    a = live(ROUTINE)
    t = small_changes(a)
    assert len(landmarks(a)) < len(landmarks(t)) < len(landmarks(live(VARIED)))
    assert (t >= a).all() and (t != a).sum() <= 52
