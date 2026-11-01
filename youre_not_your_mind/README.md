# You're not your mind

What if you aren't your thoughts? And what changes if you notice a thought
instead of believing it?

Two toy agents receive exactly the same stream of 60 thoughts:

- **Agent A** treats a negative thought as a fact (`WEIGHTS["A"] = 0.78`).
- **Agent B** notices the thought before reacting (`WEIGHTS["B"] = 0.28`). It
  still feels the thought; the thought isn't suppressed.

`generate_thoughts` uses NumPy to draw the stream from `THOUGHT_BANK`, giving each
thought a random intensity. `respond` updates an agent's activation for one
thought, and `simulate` runs it over the whole stream. Matplotlib animates both
histories.

```bash
uv run pytest -q                     # 6 tests
uv run python youre_not_your_mind.py # the summary + youre_not_your_mind.gif/.png
```

Output (seed 42):

```
Same thoughts. Different responses.
Thoughts simulated: 60
             average    peak
Agent A:        0.82    1.87
Agent B:        0.25    0.66
```

## Important: this is a toy model

The result is programmed. Nothing is random once the stream is drawn, and both
agents follow the same rule except for one number, so Agent A's reaction to a
negative thought is 0.78 / 0.28 ≈ 2.8 times Agent B's by construction. `DECAY = 0.78`
and `SETTLE = 0.04` shape the curves as well. All of these values were chosen, not
measured. Change them and the graphs change with them.

This is **not** a measurement of brain activity or emotion, and it is **not**
evidence that noticing your thoughts reduces distress. It says nothing about any
clinical outcome. It illustrates an idea inspired by cognitive defusion: a thought
is something your mind produces, and it isn't automatically a fact.

## Files

| File | What it does |
|---|---|
| `thoughts.py` | The thought bank, the seed, and `generate_thoughts` |
| `agents.py` | The weights, `respond` and `simulate` |
| `youre_not_your_mind.py` | Animates both histories, saves the GIF and PNG, prints the summary |
| `tests/test_mind.py` | Checks the stream, both responses and the histories |
