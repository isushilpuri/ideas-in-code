"""Why time seems to speed up: years, novelty and memory landmarks.

The proportions are plain arithmetic. The novelty scores and the landmark
threshold are illustrative storytelling devices, not measurements of brains.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

AGES = (10, 20, 40, 80)
DAYS = 365


def year_share(age: int) -> float:
    """One more year, as a percentage of the life already lived."""
    return 100 / age


@dataclass(frozen=True)
class Life:
    name: str
    usual: float  # novelty of an ordinary day, 0 to 1
    variety: float  # how much one day differs from the next
    surprises: int  # unusually new days in the year


ROUTINE = Life("Person A", usual=0.18, variety=0.07, surprises=3)
VARIED = Life("Person B", usual=0.46, variety=0.18, surprises=15)


def live(life: Life, seed: int = 27) -> np.ndarray:
    """One novelty score per day: 0 = same as ever, 1 = brand new."""
    rng = np.random.default_rng(seed)
    days = rng.normal(life.usual, life.variety, DAYS)
    big = rng.choice(DAYS, size=life.surprises, replace=False)
    days[big] += rng.uniform(0.3, 0.5, life.surprises)
    return np.clip(days, 0, 1)


LANDMARK = 0.62  # new enough to stand out when you look back


def landmarks(novelty: np.ndarray) -> np.ndarray:
    """The days distinctive enough to remember."""
    return np.flatnonzero(novelty >= LANDMARK)


def per_week(novelty: np.ndarray) -> np.ndarray:
    """Landmarks in each of the 52 full weeks."""
    weeks = novelty[: 52 * 7].reshape(52, 7)
    return (weeks >= LANDMARK).sum(axis=1)


MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MONTH_EDGES = np.cumsum((0,) + MONTH_DAYS)


def looking_back(novelty: np.ndarray) -> np.ndarray:
    """Landmarks per month: what memory rebuilds each month from."""
    found, _ = np.histogram(landmarks(novelty), bins=MONTH_EDGES)
    return found


def small_changes(novelty: np.ndarray, seed: int = 5) -> np.ndarray:
    """One small new thing a week: a new route, a new skill, a new face."""
    rng = np.random.default_rng(seed)
    days = np.arange(52) * 7 + rng.integers(0, 7, 52)
    changed = novelty.copy()
    changed[days] = np.clip(changed[days] + 0.5, 0, 1)
    return changed
