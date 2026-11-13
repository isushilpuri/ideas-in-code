# Why time speeds up as you get older

Why does a year feel endless at ten and gone in a blink at forty? Is it just
arithmetic, or is it about how much a year leaves behind to remember?

The model puts two ideas side by side:

- **The proportional theory.** `year_share(age)` returns `100 / age`: one more
  year as a percentage of the life already lived, for each of `AGES = (10, 20, 40, 80)`.
- **Memory landmarks.** Two fictional people get the same `DAYS = 365`.
  `live()` gives every day a novelty score from 0 to 1. A day at or above
  `LANDMARK = 0.62` counts as distinctive enough to look back on, and
  `landmarks()` finds them.
  - **`ROUTINE`** (Person A): ordinary days with little novelty (`usual=0.18`) and
    little variation (`variety=0.07`), plus 3 surprise days.
  - **`VARIED`** (Person B): more novelty (`usual=0.46`), more variation
    (`variety=0.18`), plus 15 surprise days.
  - **`small_changes()`** gives Person A one small new thing a week (a new
    route, a new skill, a new face) by lifting one random day per week by 0.5.
- `per_week()` and `looking_back()` count the landmarks in each week and month.

```bash
uv run pytest -q                    # 6 tests
uv run time-perception              # prints the numbers + saves 3 charts to ./output
uv run time-perception --no-charts  # numbers only
```

Output (seed 27):

```
One year as a share of your life
  age 10     10%
  age 20      5%
  age 40    2.5%
  age 80   1.25%
Person A: 365 days, 3 landmarks
Person B: 365 days, 85 landmarks
Person A + one small change a week: 44 landmarks
Illustrative model, not a measurement of real brains.
```

## Important: this is a toy model

The proportions are plain arithmetic. Everything else is programmed. The
novelty scores are made up: `ROUTINE` and `VARIED` set how new each person's
days are, and `LANDMARK = 0.62` decides what counts as memorable. The +0.5 lift
in `small_changes()` is chosen so that one change a week clears that
threshold. Change any of these and the landmark counts change with them. The
seed (27) was picked so that Person A has a few landmarks rather than none.

This is **not** evidence that novelty makes time feel slower, or that every new
experience makes a stronger memory. Nothing here measures a real brain. It
illustrates one possibility: when days look almost identical, there may be
fewer distinctive moments to mark where a year went. Attention, emotion, memory
and circumstance all shape how we perceive time too.

## Files

| File | What it does |
|---|---|
| `src/time_perception/model.py` | `year_share`, the two lives, `live`, `landmarks`, `per_week`, `looking_back`, `small_changes` |
| `src/time_perception/cli.py` | `time-perception` command: prints the results, optionally saves charts |
| `src/time_perception/visuals.py` | Three matplotlib charts: year shares, two lives, landmarks |
| `src/time_perception/__main__.py` | Lets `python -m time_perception` run the CLI |
| `tests/test_model.py` | Checks the shares, the 365 days, reproducibility, and the landmark counts |
