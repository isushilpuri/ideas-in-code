from __future__ import annotations

import argparse
from pathlib import Path
import json

from .simulation import SimulationConfig, run_simulation
from .analysis import build_summary, save_summary, save_player_csv
from .visualization import save_static_charts, render_animation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate a positive-expectation multiplicative bet."
    )
    parser.add_argument("--players", type=int, default=10_000)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--no-video", action="store_true",
                        help="Create charts and data, but skip animation rendering.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = SimulationConfig(
        players=args.players,
        rounds=args.rounds,
        seed=args.seed,
    )
    config.validate()
    args.output.mkdir(parents=True, exist_ok=True)

    print(f"Running {config.players:,} players for {config.rounds} rounds...")
    result = run_simulation(config)

    summary = build_summary(result)
    save_summary(summary, args.output / "simulation_summary.json")
    save_player_csv(result, args.output / "player_results.csv")
    save_static_charts(result, args.output)

    if not args.no_video:
        print("Rendering animation...")
        animation_path = render_animation(result, args.output, fps=args.fps)
        print(f"Animation saved: {animation_path}")

    sample = summary["sample_results"]
    theory = summary["theoretical_results"]

    print("\n=== SIMULATION RESULTS ===")
    print(f"Players below starting wealth: {sample['fraction_below_start']:.2%}")
    print(f"Sample mean final wealth:      ${sample['final_mean_wealth']:,.2f}")
    print(f"Sample median final wealth:    ${sample['final_median_wealth']:,.4f}")
    print(f"Theoretical expected wealth:   ${theory['expected_final_wealth']:,.2f}")
    print(f"Typical log-growth wealth:     ${theory['typical_wealth_from_mean_log_growth']:,.4f}")
    if theory["theoretical_probability_below_start"] is not None:
        print(f"Theoretical chance below $100: {theory['theoretical_probability_below_start']:.2%}")
    print(f"\nAll outputs saved in: {args.output.resolve()}")
