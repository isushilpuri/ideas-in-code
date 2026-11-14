"""Paired bar charts of the averaged indices, one PNG per experiment."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

PAPER, INK = "#fdf2e1", "#2a1f16"
COLOURS = {"Agent A": "#e0604a", "Agent B": "#1a9a8a", "The copy": "#6c5bb5"}

EXPERIMENTS = {
    "approval": ("The approval trap", ("engagement", "warmth", "confidence", "continue")),
    "listening": ("Listening is not talking less", ("talk_share", "felt_heard", "flow")),
    "silence": ("Three seconds of silence", ("composure",)),
    "wit": ("Forced humour vs wit", ("humour",)),
}


def save_charts(results: dict[str, dict[str, float]], out: Path) -> None:
    plt.rcParams.update({"figure.facecolor": PAPER, "axes.facecolor": PAPER, "text.color": INK,
                         "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})
    for key, (title, metrics) in EXPERIMENTS.items():
        fig, ax = plt.subplots(figsize=(10, 5.5))
        x = np.arange(len(metrics))
        w = 0.8 / len(results)
        for i, (name, avg) in enumerate(results.items()):
            ax.bar(x + (i - (len(results) - 1) / 2) * w, [avg[m] for m in metrics], w,
                   color=COLOURS[name], label=name)
        ax.set_xticks(x, [m.replace("_", " ") for m in metrics])
        ax.set_ylim(0, 100)
        ax.set_ylabel("Illustrative index (0-100)")
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
        ax.spines[:].set_visible(False)
        ax.grid(axis="y", alpha=0.2)
        ax.legend(frameon=False, ncol=3)
        fig.tight_layout()
        fig.savefig(out / f"{key}.png", dpi=150)
        plt.close(fig)
