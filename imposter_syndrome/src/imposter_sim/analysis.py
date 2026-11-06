from __future__ import annotations

import numpy as np

from .model import BALANCED, DISCOUNTING, Results, Style, Twins


def settles_at(success_rate, style: Style):
    """Where self-belief levels off when you succeed this often.

    Credit gained on wins balances blame taken on losses.
    """
    gain = success_rate * style.credit
    loss = (1 - success_rate) * style.blame
    return gain / (gain + loss)


def the_gap(results: Results, doubting: float = 0.5) -> dict:
    performance = results.outcomes.mean(axis=1)
    feeling = results.confidence[:, -1]
    top = performance >= np.quantile(performance, 0.75)
    hidden = top & (feeling < doubting)
    return {
        "top_performers": int(top.sum()),
        "top_but_doubting": int(hidden.sum()),
        "doubting_below": doubting,
    }


def promotion_story(results: Results) -> dict:
    c = results.config
    up = results.promoted
    doubt = results.staff.self_doubt
    groups = {
        "balanced": up & (doubt < 1 / 3),
        "discounting": up & (doubt > 2 / 3),
    }
    out: dict = {"promoted": int(up.sum())}
    for name, mask in groups.items():
        conf = results.confidence[mask]
        out[name] = {
            "count": int(mask.sum()),
            "at_promotion": float(conf[:, c.promotion_at].mean()),
            "low_point": float(conf[:, c.promotion_at :].mean(axis=0).min()),
            "final": float(conf[:, -1].mean()),
        }
    return out


def summarize(results: Results, twins: Twins) -> dict:
    perf = results.outcomes.mean(axis=1)
    return {
        "note": "Illustrative model; weights are assumptions, not clinical values.",
        "employees": results.config.employees,
        "tasks": results.config.tasks,
        "seed": results.config.seed,
        "mean_success_rate": float(perf.mean()),
        "mean_final_confidence": float(results.confidence[:, -1].mean()),
        "twins": {
            "successes": int(twins.succeeded.sum()),
            "failures": int((~twins.succeeded).sum()),
            "a_final": float(twins.a[-1]),
            "b_final": float(twins.b[-1]),
        },
        "promotion": promotion_story(results),
        "gap": the_gap(results),
        "settles_at_80pct": {
            "balanced": float(settles_at(0.8, BALANCED)),
            "discounting": float(settles_at(0.8, DISCOUNTING)),
        },
    }
