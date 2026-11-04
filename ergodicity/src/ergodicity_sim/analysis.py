from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np

from .simulation import SimulationResult


def theoretical_metrics(result: SimulationResult) -> dict:
    c = result.config
    expected_multiplier = (
        c.win_probability * c.win_multiplier
        + (1 - c.win_probability) * c.loss_multiplier
    )
    expected_final = c.starting_wealth * expected_multiplier ** c.rounds

    expected_log_growth = (
        c.win_probability * math.log(c.win_multiplier)
        + (1 - c.win_probability) * math.log(c.loss_multiplier)
    )
    typical_final = c.starting_wealth * math.exp(expected_log_growth * c.rounds)

    # Probability of ending below initial wealth, calculated exactly for this
    # symmetric 50/50 setup using the binomial distribution.
    below_start_probability = None
    if (
        c.win_probability == 0.5
        and c.win_multiplier == 1.5
        and c.loss_multiplier == 0.6
    ):
        threshold = (
            -c.rounds * math.log(c.loss_multiplier)
            / (math.log(c.win_multiplier) - math.log(c.loss_multiplier))
        )
        max_wins_below = math.ceil(threshold) - 1
        if max_wins_below < 0:
            below_start_probability = 0.0
        elif max_wins_below >= c.rounds:
            below_start_probability = 1.0
        else:
            # Stable recurrence for Binomial(n, 0.5).
            probs = [math.comb(c.rounds, k) / (2 ** c.rounds)
                     for k in range(max_wins_below + 1)]
            below_start_probability = float(sum(probs))

    return {
        "expected_multiplier_per_round": expected_multiplier,
        "expected_arithmetic_return_per_round": expected_multiplier - 1,
        "expected_final_wealth": expected_final,
        "expected_log_growth_per_round": expected_log_growth,
        "typical_wealth_from_mean_log_growth": typical_final,
        "theoretical_probability_below_start": below_start_probability,
    }


def build_summary(result: SimulationResult) -> dict:
    c = result.config
    final = result.final_wealth
    mean_by_round = result.wealth_paths.mean(axis=0)
    median_by_round = np.median(result.wealth_paths, axis=0)
    theory = theoretical_metrics(result)

    return {
        "experiment": "50/50 multiplicative bet",
        "configuration": {
            "players": c.players,
            "rounds": c.rounds,
            "starting_wealth": c.starting_wealth,
            "win_probability": c.win_probability,
            "win_multiplier": c.win_multiplier,
            "loss_multiplier": c.loss_multiplier,
            "seed": c.seed,
        },
        "sample_results": {
            "final_mean_wealth": float(np.mean(final)),
            "final_median_wealth": float(np.median(final)),
            "final_min_wealth": float(np.min(final)),
            "final_max_wealth": float(np.max(final)),
            "players_below_start": int(np.sum(final < c.starting_wealth)),
            "fraction_below_start": float(np.mean(final < c.starting_wealth)),
            "mean_wealth_by_round": mean_by_round.tolist(),
            "median_wealth_by_round": median_by_round.tolist(),
        },
        "theoretical_results": theory,
        "interpretation": (
            "The arithmetic ensemble mean and typical individual growth differ "
            "because wealth changes multiplicatively. Rare high-wealth outcomes "
            "can pull the mean upward while the median declines."
        ),
    }


def save_summary(summary: dict, path: Path) -> None:
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def save_player_csv(result: SimulationResult, path: Path) -> None:
    import csv

    c = result.config
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["player_id", "wins", "losses", "final_wealth", "below_start"])
        wins_per_player = result.wins.sum(axis=1)
        for i, wealth in enumerate(result.final_wealth):
            writer.writerow([
                i + 1,
                int(wins_per_player[i]),
                c.rounds - int(wins_per_player[i]),
                f"{wealth:.10g}",
                bool(wealth < c.starting_wealth),
            ])
