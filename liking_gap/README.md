# The liking gap

After a conversation with a stranger, do people underestimate how much the other
person liked them, and why?

A toy model of 1,000 conversations between two fictional strangers, inspired by
Boothby, Cooney, Sandstrom & Clark (2018), *"The Liking Gap in Conversations: Do
People Like Us More Than We Think?"*, Psychological Science. Everyone is scored on
the research's 1–7 scale (`LOW, HIGH = 1.0, 7.0`).

- **`converse`** gives every pair an actual liking score each way, drawn around a
  pleasant average (`pleasant = 5.8`), and a guess of how much they were liked.
- **`guess`** is how a guess is made: what you saw, blurred by
  `READ_NOISE / sqrt(minutes)`, minus your own self-criticism. Each person's
  `bias` is drawn around `0.6` with `bias_spread = 0.45`. Some people are relaxed
  and some are detectives.
- **`one_pair`** picks a typical pair: both warm, and both underestimating by about
  the usual amount.
- **`show_interest` / `attention` / `notice`** model positive signals (out of
  `CHANCES = 8`) and an attention filter. The more you focus on yourself, the more
  of the other person's signals you miss: `attention = 1.0 - 0.6 * self_focus`.
- **`replay`** remembers one five-minute conversation (`MOMENTS`: eight good
  moments and two awkward ones) with two memory systems. `BALANCED` weights them
  equally; `INNER_CRITIC = Memory(good=0.4, bad=3.0)` shrinks the good and blows up
  the awkward.
- **`by_duration`** reruns the guess for 2-, 5-, 10- and 20-minute conversations,
  where longer conversations sharpen the read but the bias stays.
- **`three_views`** reads one conversation three ways: what actually happened, the
  self-critical guess, and an outside observer, who uses the same `guess` with no
  bias.

```bash
uv run pytest -q                 # 10 tests
uv run liking-gap                # numbers + 6 charts, written to output/
uv run liking-gap --no-charts    # numbers only
```

Output (seed 42):

```
Conversations: 1,000 | people: 2,000
Actual liking:    5.74 / 7
Perceived liking: 5.12 / 7
Liking gap:       0.62
Below the line:   86%
Pair #806: A likes B 5.7, B likes A 6.2
  A thinks 5.6, B thinks 5.1
Signals shown 6.0, noticed 4.2
Memory: balanced 6.6, inner critic 2.1
   2 min  gap 0.62  spread 0.75
   5 min  gap 0.64  spread 0.56
  10 min  gap 0.63  spread 0.49
  20 min  gap 0.62  spread 0.46
Views: actual 5.9, self-critical 5.3, observer 5.8
Illustrative model only; not a reanalysis of the original data.
```

## Important: this is a toy model

The gap is programmed in. `Config.bias = 0.6` subtracts self-criticism from every
guess, so the average gap comes out near 0.6 by construction. It was chosen to sit
close to the 0.65 the paper reports (5.82 actual vs 5.17 estimated in one of its
initial studies). Set `bias=0.0, bias_spread=0.0` and the gap disappears (a test
checks this).

The other behaviours are written in the same way:
- **Attention:** missing signals comes from `attention()`'s `0.6` slope.
- **Memory:** the bleak replay comes from `INNER_CRITIC`'s `0.4` / `3.0` weights.
- **Duration:** the flat gap holds because the bias doesn't change with minutes,
  while the blur does.
- **Example pair:** it is picked by `one_pair` from the seeded run.

This is **not** evidence about how real people judge conversations, and it does
not reproduce the paper's data. It shows how one small, consistent bias in how we
read others can produce a gap that more time alone doesn't close.

## Files

| File | What it does |
|---|---|
| `src/liking_gap/model.py` | The scale, `guess`, the 1,000 conversations, signals, memory, duration and the three views |
| `src/liking_gap/analysis.py` | Turns a run into the summary numbers |
| `src/liking_gap/cli.py` | The `liking-gap` command: prints the results and writes `summary.json` |
| `src/liking_gap/visuals.py` | The six charts |
| `tests/test_model.py` | Checks the scale, the gap, the pair, the filter, memory, duration and observer |
| `pyproject.toml` / `uv.lock` | Dependencies, pinned so the numbers reproduce |
