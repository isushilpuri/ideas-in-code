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

These are **toy models**: their behaviour is written into the code on purpose so
an idea can be seen clearly. They are illustrations, not benchmarks.
