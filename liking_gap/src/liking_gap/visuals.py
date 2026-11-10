"""Charts for the six experiments, in the video's ivory palette."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .analysis import the_durations, the_pair, the_views  # noqa: E402
from .model import BALANCED, INNER_CRITIC, MOMENTS, Config, Conversations, Signals, actual_and_perceived, replay  # noqa: E402

PAPER, CARD, INK, GRID = "#fdf2e1", "#fff9ee", "#2a1f16", "#e8dcc8"
CORAL, TEAL, VIOLET = "#e0604a", "#1a9a8a", "#6c5bb5"


def _ax(title, size=(9, 6)):
    fig, ax = plt.subplots(figsize=size, dpi=110, facecolor=PAPER)
    ax.set_facecolor(CARD)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID)
    ax.set_title(title, loc="left", color=INK, fontsize=14, fontweight="bold")
    return fig, ax


def save_charts(c: Conversations, s: Signals, config: Config, out: Path) -> None:
    actual, perceived = actual_and_perceived(c)
    fig, ax = _ax("The liking gap: how much they liked you vs. your guess")
    ax.scatter(actual, perceived, s=12, alpha=0.35, color=CORAL, edgecolors="none")
    ax.plot([1, 7], [1, 7], "--", color=INK, label="perfect guess")
    ax.set(xlim=(1, 7), ylim=(1, 7), xlabel="actual liking (1-7)", ylabel="perceived liking (1-7)")
    ax.legend(frameon=False)
    fig.savefig(out / "1_liking_gap.png", bbox_inches="tight")
    plt.close(fig)

    p = the_pair(c)
    fig, ax = _ax("Two people. One conversation.", (9, 4.5))
    labels = ["A likes B", "B thinks A liked them", "B likes A", "A thinks B liked them"]
    vals = [p["a_likes_b"], p["b_thinks"], p["b_likes_a"], p["a_thinks"]]
    ax.barh(labels, vals, color=[TEAL, CORAL, TEAL, CORAL])
    ax.set_xlim(1, 7)
    ax.invert_yaxis()
    fig.savefig(out / "2_two_people.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = _ax("Signals shown vs. signals noticed", (9, 4.5))
    bins = np.arange(-0.5, 9.5, 1)
    ax.hist(s.shown, bins=bins, alpha=0.7, color=TEAL, label="shown")
    ax.hist(s.noticed, bins=bins, alpha=0.7, color=CORAL, label="noticed")
    ax.set(xlabel="positive signals", ylabel="people")
    ax.legend(frameon=False)
    fig.savefig(out / "3_signals.png", bbox_inches="tight")
    plt.close(fig)

    t = [m for m, _, _ in MOMENTS]
    fig, ax = _ax("One conversation, two memories", (9, 4.5))
    ax.plot(t, replay(MOMENTS, BALANCED), "-o", color=TEAL, label="balanced replay")
    ax.plot(t, replay(MOMENTS, INNER_CRITIC), "-o", color=CORAL, label="inner critic")
    ax.set(ylim=(1, 7), xlabel="minute", ylabel="how it went (1-7)")
    ax.legend(frameon=False)
    fig.savefig(out / "4_memory.png", bbox_inches="tight")
    plt.close(fig)

    d = the_durations(config)
    fig, ax = _ax("Does talking longer close the gap?", (9, 4.5))
    ax.bar([str(r["minutes"]) for r in d], [r["gap"] for r in d], color=CORAL)
    ax.set(xlabel="conversation length (minutes)", ylabel="average gap")
    fig.savefig(out / "5_duration.png", bbox_inches="tight")
    plt.close(fig)

    v = the_views(c)
    fig, ax = _ax("One conversation. Three interpretations.", (9, 4))
    ax.barh(["actual", "self-critical", "observer"], [v["actual"], v["self_critical"], v["observer"]], color=[TEAL, CORAL, VIOLET])
    ax.set_xlim(1, 7)
    ax.invert_yaxis()
    fig.savefig(out / "6_three_views.png", bbox_inches="tight")
    plt.close(fig)
