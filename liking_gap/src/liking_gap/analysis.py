from __future__ import annotations

from .model import (
    BALANCED,
    INNER_CRITIC,
    MOMENTS,
    Config,
    Conversations,
    Signals,
    actual_and_perceived,
    by_duration,
    one_pair,
    replay,
    three_views,
)


def the_gap(c: Conversations) -> dict:
    actual, perceived = actual_and_perceived(c)
    return {
        "people": int(actual.size),
        "actual": float(actual.mean()),
        "perceived": float(perceived.mean()),
        "gap": float((actual - perceived).mean()),
        "below_line": float((perceived < actual).mean()),
    }


def the_pair(c: Conversations) -> dict:
    i = one_pair(c)
    return {
        "pair": i,
        "a_likes_b": float(c.a_likes_b[i]),
        "b_likes_a": float(c.b_likes_a[i]),
        "a_thinks": float(c.a_thinks[i]),
        "b_thinks": float(c.b_thinks[i]),
    }


def the_signals(s: Signals) -> dict:
    return {
        "shown": float(s.shown.mean()),
        "noticed": float(s.noticed.mean()),
        "missed": float(1 - s.noticed.sum() / s.shown.sum()),
    }


def the_memory() -> dict:
    return {
        "balanced": replay(MOMENTS, BALANCED)[-1],
        "inner_critic": replay(MOMENTS, INNER_CRITIC)[-1],
    }


def the_durations(config: Config = Config()) -> list[dict]:
    return [
        {
            "minutes": m,
            "actual": float(liking.mean()),
            "perceived": float(guessed.mean()),
            "gap": float((liking - guessed).mean()),
            "spread": float((liking - guessed).std()),
        }
        for m, liking, guessed in by_duration(config)
    ]


def the_views(c: Conversations) -> dict:
    actual, critical, observer = three_views(c, one_pair(c))
    return {"actual": float(actual), "self_critical": float(critical), "observer": float(observer)}


def summarize(c: Conversations, s: Signals, config: Config = Config()) -> dict:
    return {
        "gap": the_gap(c),
        "pair": the_pair(c),
        "signals": the_signals(s),
        "memory": the_memory(),
        "durations": the_durations(config),
        "views": the_views(c),
    }
