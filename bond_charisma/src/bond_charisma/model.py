"""Can you code James Bond's charisma? A toy model of conversation styles.

Every coefficient is an invented assumption. The scores are illustrative
indices from 0 to 100, not measurements of real human charisma.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

INTERACTIONS = 1000
TURNS = 12  # things the partner says in one conversation
PAUSE = 0.25  # chance a turn ends in three seconds of silence


@dataclass(frozen=True)
class Style:
    name: str
    self_focus: float  # a reply turns the talk back to himself
    curiosity: float  # he actually wants to hear the answer
    approval: float  # he needs them to like him
    pause_panic: float  # a silence must be filled, now
    joke_rate: float  # he tries to be funny
    joke_fit: float  # the joke suits the moment


SEEKER = Style("Agent A", self_focus=0.65, curiosity=0.30, approval=0.90,
               pause_panic=0.85, joke_rate=0.55, joke_fit=0.25)
BOND = Style("Agent B", self_focus=0.15, curiosity=0.85, approval=0.20,
             pause_panic=0.15, joke_rate=0.15, joke_fit=0.80)
COPY = Style("The copy", self_focus=0.15, curiosity=0.10, approval=0.60,
             pause_panic=0.05, joke_rate=0.35, joke_fit=0.30)


@dataclass
class Talk:
    him: float = 0  # how much he says
    them: float = 0  # how much the partner says
    redirects: int = 0  # "that happened to me too"
    questions: int = 0  # a real follow-up question
    waits: int = 0  # quiet, rehearsing his next line
    depth: int = 0  # how far their topic has grown
    deepest: int = 0
    pauses: int = 0
    fillers: int = 0  # "nice weather today"
    jokes: int = 0
    landed: int = 0
    log: list[str] = field(default_factory=list)


def converse(style: Style, openness: float, rng) -> Talk:
    """One conversation, turn by turn."""
    t = Talk()
    for _ in range(TURNS):
        t.them += 1 + openness
        if rng.random() < style.self_focus:
            t.redirects += 1
            t.him += 3
            t.depth = 0
            t.log.append("redirect")
        elif rng.random() < style.curiosity:
            t.questions += 1
            t.him += 1
            t.them += openness  # a good question opens them up
            t.depth += 1
            t.log.append("question")
        else:
            t.waits += 1
            t.him += 0.5  # "mm", then quiet
            t.log.append("wait")
        t.deepest = max(t.deepest, t.depth)
        if rng.random() < PAUSE:
            t.pauses += 1
            if rng.random() < style.pause_panic:
                t.fillers += 1
                t.him += 1
                t.log.append("filler")
            else:
                t.log.append("calm")
        if rng.random() < style.joke_rate:
            t.jokes += 1
            hit = rng.random() < style.joke_fit
            t.landed += hit
            t.log.append("laugh" if hit else "cringe")
    return t


def scores(t: Talk, style: Style, openness: float) -> dict[str, float]:
    """How the partner felt afterwards, as 0-100 indices."""
    heard = (t.questions - t.redirects) / TURNS
    calm = 1 - t.fillers / max(t.pauses, 1)
    wit = (2 * t.landed - t.jokes) / TURNS
    s = {
        "engagement": 45 + 35 * heard + 25 * wit + 15 * openness,
        "warmth": 50 + 32 * heard + 10 * wit,
        "confidence": 50 + 30 * calm - 25 * style.approval,
        "felt_heard": 50 + 50 * heard,
        "flow": 100 * t.deepest / TURNS,
        "talk_share": 100 * t.him / (t.him + t.them),
        "composure": 100 * calm,
        "humour": 50 + 50 * (2 * t.landed - t.jokes) / max(t.jokes, 1),
    }
    s["continue"] = (0.4 * s["engagement"] + 0.4 * s["warmth"]
                     + 0.2 * s["confidence"])
    return {k: float(np.clip(v, 0, 100)) for k, v in s.items()}


def partners(seed: int = 23) -> np.ndarray:
    """The same 1,000 fictional partners for every style: openness 0-1."""
    return np.random.default_rng(seed).beta(4, 3, INTERACTIONS)


def run(style: Style, people: np.ndarray, seed: int = 7) -> list[Talk]:
    rng = np.random.default_rng(seed)
    return [converse(style, o, rng) for o in people]


def table(style: Style, talks: list[Talk], people: np.ndarray):
    rows = [scores(t, style, o) for t, o in zip(talks, people)]
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}


def averages(cols: dict[str, np.ndarray]) -> dict[str, float]:
    return {k: round(float(v.mean()), 1) for k, v in cols.items()}
