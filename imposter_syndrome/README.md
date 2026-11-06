# Imposter Syndrome

What if your confidence isn't measuring your competence, but how creatively you
explain away your own success?

A toy model of 1,000 employees who succeed and fail at tasks. Each one updates
their self-belief after every result. The only thing that varies is *how* they
read those results.

- **`Style(credit, blame)`** is how a brain turns a result into self-belief.
  `BALANCED = Style(0.22, 0.22)` reads wins and losses fairly;
  `DISCOUNTING = Style(0.075, 0.30)` barely counts a win and takes a loss hard.
- **`interpret`** moves confidence toward 100% on a success and toward 0% on a
  failure, by that style's `credit` or `blame`.
- **`identical_lives`** gives two employees one shared life: 30 tasks, the same
  ability (0.70) and the exact same wins and losses. A reads it balanced, B discounting.
- **`run`** hires 1,000 employees (`self_doubt` blends each one between the two
  styles), runs 100 tasks, then **`promote`**s the top quarter at task 60 to
  harder work (`harder_by = 0.16`) that they slowly get better at (`learning = 0.003`).
- **`settles_at`** is where self-belief levels off for a given success rate: at a
  70% success rate, A settles at 70% and B at 37%.
- **`the_gap`** counts top-quarter performers who end up believing they're below 50%.

```bash
uv run pytest -q                       # 5 tests
uv run imposter-sim                    # numbers + charts, written to output/
uv run imposter-sim --no-charts        # numbers only
```

Output (seed 42):

```
Employees: 1,000 | tasks: 100
Twins: 21 wins, 9 losses, same for both
  A (balanced) final confidence:    82%
  B (discounting) final confidence: 43%
Promoted: 261
  balanced    88% -> low 74% -> 83%
  discounting 77% -> low 58% -> 66%
Top performers: 273 | believe they're below 50%: 12
Illustrative model only; not clinical evidence.
```

`output/` also gets `summary.json` and three charts: `twins.png`, `promotion.png`
and `gap.png`.

## Important: this is a toy model

The result is programmed. The two `Style` weights decide it: B ends below A
because `DISCOUNTING` gives less `credit` and more `blame` than `BALANCED`. Swap
those numbers and the gap closes or flips. The promotion dip comes from
`harder_by`, and the recovery from `learning`. All of these are assumptions, not
clinical values.

The twins use a fixed seed of 148 (21 wins, 9 losses). Other seeds give other
paths, but B never ends above A: across seeds 0–999 B stayed at or below A at
every step. The workforce run uses the default seed, 42.

This is **not** evidence about how people with imposter feelings think. Real
confidence is shaped by experience, workplace culture, discrimination, feedback
and personality. The model deliberately isolates one mechanism: how success and
failure are interpreted.

## Files

| File | What it does |
|---|---|
| `src/imposter_sim/model.py` | `Config`, the two `Style`s, `interpret`, the twins, promotion and the full `run` |
| `src/imposter_sim/analysis.py` | `settles_at`, `the_gap`, `promotion_story` and the summary |
| `src/imposter_sim/visuals.py` | Saves the three charts in the video's palette |
| `src/imposter_sim/cli.py` | The `imposter-sim` command: runs everything and prints the results |
| `src/imposter_sim/__main__.py` | Lets `python -m imposter_sim` run the same command |
| `tests/test_model.py` | Checks the update rule, the twins, reproducibility and the numbers the video quotes |
