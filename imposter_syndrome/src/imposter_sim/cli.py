from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import summarize
from .model import Config, identical_lives, run


def main() -> None:
    p = argparse.ArgumentParser(description="Imposter syndrome toy model")
    p.add_argument("--employees", type=int, default=1000)
    p.add_argument("--tasks", type=int, default=100)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", type=Path, default=Path("output"))
    p.add_argument("--no-charts", action="store_true")
    a = p.parse_args()

    config = Config(employees=a.employees, tasks=a.tasks, seed=a.seed)
    results = run(config)
    twins = identical_lives()
    s = summarize(results, twins)

    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "summary.json").write_text(json.dumps(s, indent=2))
    if not a.no_charts:
        from .visuals import save_charts

        save_charts(results, twins, a.output)

    t, pr, g = s["twins"], s["promotion"], s["gap"]
    print(f"Employees: {config.employees:,} | tasks: {config.tasks}")
    print(f"Twins: {t['successes']} wins, {t['failures']} losses, same for both")
    print(f"  A (balanced) final confidence:    {t['a_final']:.0%}")
    print(f"  B (discounting) final confidence: {t['b_final']:.0%}")
    print(f"Promoted: {pr['promoted']}")
    for k in ("balanced", "discounting"):
        v = pr[k]
        print(f"  {k:<11} {v['at_promotion']:.0%} -> low {v['low_point']:.0%} -> {v['final']:.0%}")
    print(
        f"Top performers: {g['top_performers']} | believe they're below "
        f"{g['doubting_below']:.0%}: {g['top_but_doubting']}"
    )
    print("Illustrative model only; not clinical evidence.")


if __name__ == "__main__":
    main()
