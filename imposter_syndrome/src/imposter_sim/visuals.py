"""Static charts of a run, in the video's palette."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.ticker import PercentFormatter  # noqa: E402

from .analysis import settles_at  # noqa: E402
from .model import BALANCED, DISCOUNTING, Results, Twins  # noqa: E402

PAPER, CARD, INK, DIM = "#fdf2e1", "#fff9ee", "#2a1f16", "#7d6f60"
GRID, CORAL, TEAL, YELLOW = "#e8dcc8", "#e0604a", "#1a9a8a", "#fbc844"


def _axes(title: str):
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=PAPER)
    ax.set_facecolor(CARD)
    ax.set_title(title, loc="left", color=INK, fontsize=16, fontweight="bold")
    ax.tick_params(colors=INK)
    for side in ax.spines.values():
        side.set_color(GRID)
    ax.grid(color=GRID)
    ax.set_axisbelow(True)
    return fig, ax


def save_charts(r: Results, twins: Twins, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = _axes("Same results, different self-belief")
    x = np.arange(len(twins.a))
    ax.plot(x, twins.a, color=TEAL, lw=3, label="A: balanced")
    ax.plot(x, twins.b, color=CORAL, lw=3, label="B: discounting")
    for i, ok in enumerate(twins.succeeded):
        ax.axvspan(i + 0.1, i + 0.9, ymax=0.03, color=TEAL if ok else CORAL)
    ax.set(ylim=(0, 1), xlabel="task", ylabel="confidence")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False)
    fig.savefig(out / "twins.png", dpi=150, facecolor=PAPER)
    plt.close(fig)

    fig, ax = _axes("Promoted: harder tasks from the dashed line")
    c, up, d = r.config, r.promoted, r.staff.self_doubt
    for mask, color, name in (
        (up & (d < 1 / 3), TEAL, "low self-doubt"),
        (up & (d > 2 / 3), CORAL, "high self-doubt"),
    ):
        ax.plot(r.confidence[mask].mean(axis=0), color=color, lw=3, label=name)
    ax.axvline(c.promotion_at, color=YELLOW, ls="--", lw=2)
    ax.set(ylim=(0, 1), xlabel="task", ylabel="mean confidence")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False)
    fig.savefig(out / "promotion.png", dpi=150, facecolor=PAPER)
    plt.close(fig)

    fig, ax = _axes("Actual performance vs perceived competence")
    perf, feel = r.outcomes.mean(axis=1), r.confidence[:, -1]
    ax.scatter(perf, feel, c=d, cmap="coolwarm", s=14, alpha=0.6)
    rate = np.linspace(0.01, 0.99, 99)
    ax.plot(rate, settles_at(rate, BALANCED), color=TEAL, lw=2)
    ax.plot(rate, settles_at(rate, DISCOUNTING), color=CORAL, lw=2)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="success rate", ylabel="final confidence")
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    fig.savefig(out / "gap.png", dpi=150, facecolor=PAPER)
    plt.close(fig)
