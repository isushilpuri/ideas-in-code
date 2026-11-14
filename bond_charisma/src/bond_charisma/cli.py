from __future__ import annotations

import argparse
from pathlib import Path

from .model import BOND, COPY, INTERACTIONS, SEEKER, averages, partners, run, table

TRACKED = ("engagement", "warmth", "confidence", "continue")


def main() -> None:
    p = argparse.ArgumentParser(description="Can you code James Bond's charisma?")
    p.add_argument("--seed", type=int, default=23)
    p.add_argument("--output", type=Path, default=Path("output"))
    p.add_argument("--no-charts", action="store_true")
    a = p.parse_args()

    people = partners(a.seed)
    results = {}
    for style in (SEEKER, BOND, COPY):
        results[style.name] = averages(table(style, run(style, people), people))

    print(f"{INTERACTIONS} conversations each, same partners")
    print(f"{'':10}" + "".join(f"{k:>12}" for k in TRACKED))
    for name, avg in results.items():
        print(f"{name:10}" + "".join(f"{avg[k]:>12}" for k in TRACKED))
    print("Illustrative model scores, not real measurements of charisma.")

    if not a.no_charts:
        from .visuals import save_charts

        a.output.mkdir(parents=True, exist_ok=True)
        save_charts(results, a.output)
        print(f"Charts saved to: {a.output.resolve()}")


if __name__ == "__main__":
    main()
