from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import summarize
from .model import Config, converse, signals


def main() -> None:
    p = argparse.ArgumentParser(description="The liking gap, simulated")
    p.add_argument("--pairs", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", type=Path, default=Path("output"))
    p.add_argument("--no-charts", action="store_true")
    a = p.parse_args()

    config = Config(pairs=a.pairs, seed=a.seed)
    c = converse(config)
    s = signals(c)
    out = summarize(c, s, config)

    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "summary.json").write_text(json.dumps(out, indent=2))
    if not a.no_charts:
        from .visuals import save_charts

        save_charts(c, s, config, a.output)

    g, pr, sg, m, v = out["gap"], out["pair"], out["signals"], out["memory"], out["views"]
    print(f"Conversations: {config.pairs:,} | people: {g['people']:,}")
    print(f"Actual liking:    {g['actual']:.2f} / 7")
    print(f"Perceived liking: {g['perceived']:.2f} / 7")
    print(f"Liking gap:       {g['gap']:.2f}")
    print(f"Below the line:   {g['below_line']:.0%}")
    print(f"Pair #{pr['pair']}: A likes B {pr['a_likes_b']:.1f}, B likes A {pr['b_likes_a']:.1f}")
    print(f"  A thinks {pr['a_thinks']:.1f}, B thinks {pr['b_thinks']:.1f}")
    print(f"Signals shown {sg['shown']:.1f}, noticed {sg['noticed']:.1f}")
    print(f"Memory: balanced {m['balanced']:.1f}, inner critic {m['inner_critic']:.1f}")
    for d in out["durations"]:
        print(f"  {d['minutes']:>2} min  gap {d['gap']:.2f}  spread {d['spread']:.2f}")
    print(f"Views: actual {v['actual']:.1f}, self-critical {v['self_critical']:.1f}, observer {v['observer']:.1f}")
    print("Illustrative model only; not a reanalysis of the original data.")


if __name__ == "__main__":
    main()
