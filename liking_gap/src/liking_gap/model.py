"""A toy model of the liking gap.

Two strangers talk. Each one ends up liking the other some amount, and each one
guesses how much the other liked them. The model is inspired by Boothby et al.
(2018), "The Liking Gap in Conversations"; it is an illustration, not a
reanalysis of their data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

LOW, HIGH = 1.0, 7.0  # the research's 1-7 liking scale


def clip(x):
    return np.clip(x, LOW, HIGH)


@dataclass(frozen=True)
class Config:
    pairs: int = 1000
    minutes: float = 5  # a short first conversation
    pleasant: float = 5.8  # most chats are pleasant
    spread: float = 0.75
    bias: float = 0.6  # how much less we think they liked us
    bias_spread: float = 0.45  # relaxed ... detective
    seed: int = 42


@dataclass
class Conversations:
    a_likes_b: np.ndarray
    b_likes_a: np.ndarray
    a_thinks: np.ndarray  # how much A thinks B liked A
    b_thinks: np.ndarray  # how much B thinks A liked B
    bias: np.ndarray  # each person's self-criticism


READ_NOISE = 0.9  # blur of a one-minute read


def guess(liking, minutes, self_critical, rng):
    """What you think they felt, from what you saw."""
    blur = READ_NOISE / np.sqrt(minutes)  # sharper with time
    seen = liking + rng.normal(0, blur, np.shape(liking))
    return clip(seen - self_critical)


def converse(config: Config = Config()) -> Conversations:
    rng = np.random.default_rng(config.seed)
    n, m = config.pairs, config.minutes
    a_likes_b = clip(rng.normal(config.pleasant, config.spread, n))
    b_likes_a = clip(rng.normal(config.pleasant, config.spread, n))
    bias = rng.normal(config.bias, config.bias_spread, (2, n))
    bias = np.maximum(0, bias)
    a_thinks = guess(b_likes_a, m, bias[0], rng)
    b_thinks = guess(a_likes_b, m, bias[1], rng)
    return Conversations(
        a_likes_b, b_likes_a, a_thinks, b_thinks, bias
    )


def actual_and_perceived(c: Conversations):
    """One row per person: how liked they were, and their guess."""
    actual = np.concatenate([c.b_likes_a, c.a_likes_b])
    perceived = np.concatenate([c.a_thinks, c.b_thinks])
    return actual, perceived


def one_pair(c: Conversations) -> int:
    """A typical pair: both underestimate, by the usual amount."""
    gap_a = c.b_likes_a - c.a_thinks
    gap_b = c.a_likes_b - c.b_thinks
    both = (gap_a > 0) & (gap_b > 0)
    for liked in (c.a_likes_b, c.b_likes_a):
        both &= (liked > 5.6) & (liked < 6.5)  # warm, not maxed
    off = abs(gap_a - np.median(gap_a))
    off += abs(gap_b - np.median(gap_b))
    return int(np.argmin(np.where(both, off, np.inf)))


# ---- what you notice ----

SIGNALS = ("smile", "follow-up question", "laugh", "attentive listening")
CHANCES = 8  # moments in a conversation to show interest


def show_interest(liking, rng):
    """Warmer people send more positive signals."""
    p = (liking - LOW) / (HIGH - LOW)
    return rng.binomial(CHANCES, 0.95 * p)


def attention(self_focus):
    """Busy judging yourself, you miss more of them."""
    return 1.0 - 0.6 * self_focus


def notice(shown, self_focus, rng):
    return rng.binomial(shown, attention(self_focus))


@dataclass
class Signals:
    shown: np.ndarray  # positive signals each person received
    noticed: np.ndarray  # the ones they actually took in
    self_focus: np.ndarray


def signals(c: Conversations, seed: int = 7) -> Signals:
    rng = np.random.default_rng(seed)
    liked_by_partner, _ = actual_and_perceived(c)
    shown = show_interest(liked_by_partner, rng)
    self_focus = rng.beta(2, 2, shown.shape)
    noticed = notice(shown, self_focus, rng)
    return Signals(shown, noticed, self_focus)


# ---- what you remember ----

# (minute, what happened, how it felt: +1 good, -1 awkward)
MOMENTS = [
    (0.3, "smile", 1.0),
    (0.8, "question about work", 1.0),
    (1.3, "laugh", 1.0),
    (1.8, "forgot their name", -1.0),
    (2.3, "follow-up question", 1.0),
    (2.8, "friendly disagreement", 0.5),
    (3.2, "laugh", 1.0),
    (3.7, "said it wrong", -1.0),
    (4.2, "shared a story", 1.0),
    (4.7, "laugh", 1.0),
]


@dataclass(frozen=True)
class Memory:
    good: float  # weight on the positive moments
    bad: float  # weight on the awkward ones


BALANCED = Memory(good=1.0, bad=1.0)
INNER_CRITIC = Memory(good=0.4, bad=3.0)


def replay(moments, memory: Memory) -> list[float]:
    """How it feels in memory, moment by moment, on 1-7."""
    total, felt = 0.0, []
    for _, _, feel in moments:
        weight = memory.good if feel > 0 else memory.bad
        total += feel * weight
        felt.append(4 + 3 * np.tanh(total / 4))
    return felt


# ---- longer conversations ----

DURATIONS = (2, 5, 10, 20)


def by_duration(config: Config = Config(), seed: int = 11):
    """Same bias. Only the length of the conversation changes."""
    rng = np.random.default_rng(seed)
    n = config.pairs * 2
    rows = []
    for minutes in DURATIONS:
        liking = clip(rng.normal(config.pleasant, config.spread, n))
        bias = rng.normal(config.bias, config.bias_spread, n)
        bias = np.maximum(0, bias)
        guessed = guess(liking, minutes, bias, rng)
        rows.append((minutes, liking, guessed))
    return rows


# ---- one conversation, three readings ----


def three_views(c: Conversations, pair: int, seed: int = 3):
    """The same conversation, read three ways."""
    rng = np.random.default_rng(seed)
    liked = np.array([c.b_likes_a[pair], c.a_likes_b[pair]])
    actual = liked.mean()
    self_critical = np.mean([c.a_thinks[pair], c.b_thinks[pair]])
    # An observer sees the same five minutes, with no inner critic.
    observer = guess(liked, 5, 0.0, rng).mean()
    return actual, self_critical, observer
