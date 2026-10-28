# Context overload

Does giving an AI agent more information make it better at its job — or worse?

Two tiny toy agents answer one question, *"When does the customer's contract
renew?"*, from a list of notes. The one relevant fact is buried among a growing
pile of irrelevant ones: old logs, outdated plans, a coffee-machine schedule.

- **`stuffing_agent`** reads every note it is given.
- **`filtering_agent`** keeps only the relevant notes first, then answers.

`experiment.py` runs 500 trials at each of 21 noise levels (0 to 100 irrelevant
notes) with NumPy.

```bash
uv run pytest -q                  # 7 tests
uv run python agent.py            # one clean question → "A: 14 June"
uv run python context_overload.py # the full experiment + context_overload.png
```

Output (seed 42):

```
500 trials per level, 21 noise levels
noise   stuffing   filtering
    0      97.2%       93.2%
   20      85.4%       94.6%
   40      75.0%       95.2%
   60      65.4%       93.0%
   80      60.2%       94.2%
  100      52.8%       94.0%
```

## Important: this is a toy model

The failure is programmed. In `agent.py`, every irrelevant note costs the
stuffing agent a fixed slice of accuracy (`DISTRACTION = 0.0045`), and the
filter sometimes drops the fact too (`FILTER_MISS = 0.03`). Change those
numbers and the graph changes with them.

This is **not** evidence that real language models get worse with every token.
It illustrates a real engineering problem: more information isn't necessarily
more useful information. Context isn't just something you collect — it's
something you manage.

## Files

| File | What it does |
|---|---|
| `agent.py` | The question, the fact, the noise notes, and both agents |
| `experiment.py` | Builds buried contexts and runs the trials |
| `context_overload.py` | Prints the results table and saves the chart |
| `tests/test_agents.py` | Checks the agents, the filter and the experiment |
