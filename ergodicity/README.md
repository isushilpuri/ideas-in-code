# Noetic Room — Ergodicity: The Winning Bet That Ruins You

A coin flip pays +50% on heads and costs 40% on tails, so the average return is
+5% a round. What happens to the people who keep playing?

A reproducible Monte Carlo simulation of 10,000 players, each starting with $100
and betting everything they have, 100 times.

- **`SimulationConfig`** holds the experiment: `players`, `rounds`, `starting_wealth`,
  `win_probability`, `win_multiplier = 1.5`, `loss_multiplier = 0.6`, `seed`.
- **`run_simulation`** draws each player's wins and losses with NumPy, then compounds
  them with `np.cumprod`, because each bet is on whatever is left.
- **`theoretical_metrics`** works out the exact answers: the expected wealth, the wealth
  implied by the average log growth, and the binomial chance of ending below $100.

```bash
uv run pytest -q               # 3 tests
uv run ergodicity-sim --no-video   # numbers and charts, written to output/
uv run ergodicity-sim          # also renders the animation (slower)
```

Output (seed 42):

```
Running 10,000 players for 100 rounds...

=== SIMULATION RESULTS ===
Players below starting wealth: 86.53%
Sample mean final wealth:      $4,205.99
Sample median final wealth:    $0.5154
Theoretical expected wealth:   $13,150.13
Typical log-growth wealth:     $0.5154
Theoretical chance below $100: 86.44%
```

The sample mean falls well short of the $13,150.13 expectation, and that is part of
the point. The expectation is held up by winners so rare that 10,000 players rarely
include them. Across seeds 1, 2, 3, 7, 42 and 123 the sample mean ranged from
$3,808.93 to $10,664.65, while the median stayed at $0.5154. Seed 42 is the project's
default and was not picked to match any number.

## Why it happens

One win and one loss multiply to `1.5 × 0.6 = 0.9`, a 10% loss, whichever comes first.
So the typical player, who wins half their bets, ends with:

`$100 × 0.9^50 ≈ $0.515`

The expected value averages over everyone at once and keeps growing:

`$100 × 1.05^100 ≈ $13,150.13`

## Important: this is a toy model

The outcome is programmed. `win_multiplier`, `loss_multiplier` and `win_probability`
decide it: the median falls only because `0.5 × ln(1.5) + 0.5 × ln(0.6)` is negative.
Change those numbers and the result changes with them. Every player also bets their
entire wealth every round, with independent flips and fixed payoffs, and can never
stop, diversify or bet less.

This is **not** evidence that any real investment behaves this way, and it is not
financial advice. It illustrates one idea: a positive average return doesn't by itself
tell you what happens to one person who keeps playing.

## Files

| File | What it does |
|---|---|
| `src/ergodicity_sim/simulation.py` | The config and the simulation itself |
| `src/ergodicity_sim/analysis.py` | Exact expectations, the summary, JSON and CSV output |
| `src/ergodicity_sim/visualization.py` | Static charts and the animated overview |
| `src/ergodicity_sim/cli.py` | The `ergodicity-sim` command and its printed results |
| `src/ergodicity_sim/__main__.py` | Lets `python -m ergodicity_sim` run the same command |
| `tests/test_simulation.py` | Checks shape, reproducibility and the quoted numbers |
| `.gitignore` | Keeps generated `output/` out of the repo |
