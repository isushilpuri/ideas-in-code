"""A toy model of imposter syndrome: same evidence, different stories.

Illustrative only. The credit/blame weights are assumptions chosen to
isolate one mechanism (how results are interpreted), not clinical values.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Config:
    employees: int = 1000
    tasks: int = 100
    promotion_at: int = 60
    harder_by: float = 0.16
    learning: float = 0.003
    seed: int = 42


@dataclass(frozen=True)
class Style:
    """How a brain turns a result into self-belief."""

    credit: float  # how far a success moves you up
    blame: float  # how far a failure knocks you down


BALANCED = Style(credit=0.22, blame=0.22)
DISCOUNTING = Style(credit=0.075, blame=0.30)


@dataclass
class Workforce:
    ability: np.ndarray  # how good they actually are
    confidence: np.ndarray  # how good they think they are
    self_doubt: np.ndarray  # their relationship with compliments


def hire(config: Config, rng: np.random.Generator) -> Workforce:
    n = config.employees
    return Workforce(
        ability=rng.beta(5, 3, n).clip(0.15, 0.95),
        confidence=np.full(n, 0.5),
        self_doubt=rng.random(n),
    )


def attempt(ability, difficulty, rng):
    """Better than the task means likely, never certain."""
    p_success = 1 / (1 + np.exp(-7 * (ability - difficulty)))
    return rng.random(np.shape(p_success)) < p_success


def interpret(confidence, succeeded, style: Style):
    """One result in, one updated self-belief out."""
    up = confidence + style.credit * (1 - confidence)
    down = confidence - style.blame * confidence
    return np.clip(np.where(succeeded, up, down), 0.01, 0.99)


def blend(self_doubt) -> Style:
    """0 = balanced, 1 = discounting, anything between."""
    d = self_doubt
    return Style(
        credit=(1 - d) * BALANCED.credit + d * DISCOUNTING.credit,
        blame=(1 - d) * BALANCED.blame + d * DISCOUNTING.blame,
    )


@dataclass
class Twins:
    succeeded: np.ndarray
    a: np.ndarray
    b: np.ndarray


def identical_lives(tasks=30, ability=0.70, seed=148) -> Twins:
    """Two employees, one shared life. Only the story differs."""
    rng = np.random.default_rng(seed)
    succeeded = attempt(np.full(tasks, ability), 0.5, rng)

    a, b = [0.5], [0.5]
    for result in succeeded:
        a.append(interpret(a[-1], result, BALANCED))
        b.append(interpret(b[-1], result, DISCOUNTING))
    return Twins(succeeded, np.array(a), np.array(b))


def promote(outcomes, config: Config):
    """The top quarter by results so far get the bigger job."""
    record = outcomes[:, : config.promotion_at].mean(axis=1)
    return record >= np.quantile(record, 0.75)


@dataclass
class Results:
    config: Config
    staff: Workforce
    outcomes: np.ndarray
    confidence: np.ndarray
    promoted: np.ndarray


def run(config: Config = Config()) -> Results:
    rng = np.random.default_rng(config.seed)
    staff = hire(config, rng)
    style = blend(staff.self_doubt)
    n, tasks = config.employees, config.tasks

    ability = staff.ability.copy()
    belief = staff.confidence.copy()
    outcomes = np.zeros((n, tasks), dtype=bool)
    confidence = [belief]
    promoted = np.zeros(n, dtype=bool)

    for t in range(tasks):
        if t == config.promotion_at:
            promoted = promote(outcomes, config)
        if t >= config.promotion_at:
            # Harder work, and slowly getting better at it.
            ability = np.where(promoted, ability + config.learning, ability)
        difficulty = 0.5 + config.harder_by * promoted
        outcomes[:, t] = attempt(ability, difficulty, rng)
        belief = interpret(belief, outcomes[:, t], style)
        confidence.append(belief)

    return Results(config, staff, outcomes, np.array(confidence).T, promoted)
