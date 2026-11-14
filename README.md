# ideas-in-code

Small, runnable Python projects behind my explainer videos — each one takes an
idea (a cognitive bias, a paradox, an engineering problem) and tests it in code.

Every folder is self-contained, with its own dependencies. Install
[uv](https://docs.astral.sh/uv/), then:

```bash
cd <folder>
uv run pytest -q          # check it
uv run python <main>.py   # run it
```

| Video | Folder | Run |
|---|---|---|
| More Context Made My AI Agent Worse | [`context_overload/`](context_overload/) | `uv run python context_overload.py` |
| Why You Can't Stop Scrolling | [`scrolling_experiment/`](scrolling_experiment/) | `uv run python scrolling_experiment.py` |
| You're Not Your Mind | [`youre_not_your_mind/`](youre_not_your_mind/) | `uv run python youre_not_your_mind.py` |
| Ergodicity: The Winning Bet That Ruins You | [`ergodicity/`](ergodicity/) | `uv run ergodicity-sim --no-video` |
| Imposter Syndrome | [`imposter_syndrome/`](imposter_syndrome/) | `uv run imposter-sim` |
| People Like You More Than You Think (I Simulated It) | [`liking_gap/`](liking_gap/) | `uv run liking-gap` |
| Why Time Speeds Up as You Get Older | [`time_perception/`](time_perception/) | `uv run time-perception` |
| Can You Code James Bond's Charisma? | [`bond_charisma/`](bond_charisma/) | `uv run bond-charisma` |

These are **toy models**: their behaviour is written into the code on purpose so
an idea can be seen clearly. They are illustrations, not benchmarks.
