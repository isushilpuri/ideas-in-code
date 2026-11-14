# Can You Code James Bond's Charisma?

What makes someone charismatic: dominating the conversation, or making the other
person feel heard? And can you get there by copying how someone else behaves?

Three conversational styles (`Style` in `model.py`) each talk to the same 1,000
fictional partners (`partners()`, openness drawn from a Beta(4, 3)):

- **`SEEKER`, Agent A, the approval seeker**: turns replies back to himself
  (`self_focus=0.65`), fills almost every silence (`pause_panic=0.85`), tries a
  lot of jokes that rarely fit.
- **`BOND`, Agent B, Bond-inspired**: asks real follow-ups (`curiosity=0.85`),
  lets pauses be, jokes rarely but on point (`joke_fit=0.80`).
- **`COPY`, the copy**: Agent B's surface (quiet, composed, sarcastic) with
  almost no curiosity (`curiosity=0.10`).

`converse()` plays one 12-turn conversation (`TURNS`). Each turn the agent
redirects to himself, asks a follow-up, or just waits. A quarter of turns end in
three seconds of silence (`PAUSE`), and sometimes he tries a joke. `scores()`
turns those counts into 0–100 indices: engagement, warmth, confidence and
willingness to continue, plus felt-heard, flow, talk share, composure and humour.

```bash
uv run pytest -q                    # 6 tests
uv run bond-charisma                # the table + four bar charts in ./output
uv run bond-charisma --no-charts
```

Output (seed 23):

```
1000 conversations each, same partners
            engagement      warmth  confidence    continue
Agent A           27.7        29.8        33.0        29.6
Agent B           75.9        69.3        70.3        72.1
The copy          47.8        46.5        63.6        50.4
Illustrative model scores, not real measurements of charisma.
```

The copy talks the least of the three, yet partners feel heard by him far less
than by Agent B (`felt_heard` 46.7 vs 78.8). He is also the calmest (`composure`
95.4 vs 84.4), but scores lower on confidence (63.6 vs 70.3).

## Important: this is a toy model

The result is programmed. The six numbers on each `Style` decide how each agent
behaves, and the coefficients in `scores()` decide what that behaviour is worth:
a follow-up question adds to `heard` and a redirect subtracts from it, a missed
joke costs as much as a landed one earns, and needing approval lowers
`confidence` directly (`- 25 * style.approval`). Change those numbers and the
table changes with them.

This is **not** evidence about real people or real charisma, and the indices are
not psychological scales. It makes one idea easy to see: copying someone's
visible behaviour without the reason behind it (curiosity) doesn't copy the
effect.

## Files

| File | What it does |
|---|---|
| `src/bond_charisma/model.py` | The three styles, one conversation (`converse`), the scores, the 1,000 partners |
| `src/bond_charisma/cli.py` | Runs all three styles and prints the table |
| `src/bond_charisma/visuals.py` | Paired bar charts, one PNG per experiment |
| `tests/test_model.py` | Checks the reply counts, score ranges and the three headline comparisons |
