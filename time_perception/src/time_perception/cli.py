from __future__ import annotations

import argparse
from pathlib import Path

from .model import (
    AGES, DAYS, ROUTINE, VARIED, landmarks, live, small_changes, year_share,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Why time speeds up, simulated")
    p.add_argument("--seed", type=int, default=27)
    p.add_argument("--output", type=Path, default=Path("output"))
    p.add_argument("--no-charts", action="store_true")
    a = p.parse_args()

    a_days = live(ROUTINE, a.seed)
    b_days = live(VARIED, a.seed)
    tweaked = small_changes(a_days)

    print("One year as a share of your life")
    for age in AGES:
        print(f"  age {age:>2}  {year_share(age):>5g}%")
    for life, days in ((ROUTINE, a_days), (VARIED, b_days)):
        print(f"{life.name}: {DAYS} days, {len(landmarks(days))} landmarks")
    print(f"Person A + one small change a week: {len(landmarks(tweaked))} landmarks")
    print("Illustrative model, not a measurement of real brains.")

    if not a.no_charts:
        from .visuals import save_charts

        a.output.mkdir(parents=True, exist_ok=True)
        save_charts(a_days, b_days, tweaked, a.output)
        print(f"Charts saved to: {a.output.resolve()}")


if __name__ == "__main__":
    main()
