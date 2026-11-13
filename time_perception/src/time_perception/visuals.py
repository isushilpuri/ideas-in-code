"""Three stills of the model, in the video's ivory palette."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .model import AGES, LANDMARK, MONTH_EDGES, landmarks, year_share

PAPER, INK, CORAL, TEAL, VIOLET = "#fdf2e1", "#2a1f16", "#e0604a", "#1a9a8a", "#6c5bb5"


def _style() -> None:
    plt.rcParams.update({
        "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
        "axes.edgecolor": INK,
    })


def save_charts(a_days: np.ndarray, b_days: np.ndarray, tweaked: np.ndarray, out: Path) -> None:
    _style()

    fig, ax = plt.subplots(figsize=(12, 6))
    y = np.arange(len(AGES))[::-1]
    shares = [year_share(age) for age in AGES]
    ax.barh(y, shares, color=[TEAL, TEAL, CORAL, CORAL], height=0.5)
    ax.set_yticks(y, [f"Age {age}" for age in AGES])
    ax.set_xlim(0, 11.5)
    ax.set_xlabel("One year as a percentage of your life")
    for yi, v in zip(y, shares):
        ax.text(v + 0.15, yi, f"{v:g}%", va="center", fontsize=16, fontweight="bold")
    ax.set_title("Same 365 days. Different proportions.", loc="left", fontsize=20, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "01_proportional_year.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(13, 5), sharex=True)
    for ax, days, name, color in ((axes[0], a_days, "Person A: routine", CORAL), (axes[1], b_days, "Person B: variety", TEAL)):
        ax.bar(np.arange(len(days)), days, width=1, color=color, alpha=0.55)
        ax.axhline(LANDMARK, color=INK, lw=1, ls="--")
        marks = landmarks(days)
        ax.scatter(marks, days[marks] + 0.05, s=18, color=INK)
        ax.set_ylim(0, 1.1)
        ax.set_title(f"{name}: {len(marks)} landmarks", loc="left", fontsize=14, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
    axes[1].set_xticks(MONTH_EDGES[:-1:3], ["Jan", "Apr", "Jul", "Oct"])
    fig.savefig(out / "02_two_lives.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(13, 3.6))
    rows = (("Person A", a_days, CORAL), ("A + small changes", tweaked, VIOLET), ("Person B", b_days, TEAL))
    for k, (name, days, color) in enumerate(rows):
        marks = landmarks(days)
        ax.scatter(marks, np.full(len(marks), k), s=40, color=color)
        ax.text(368, k, f"{len(marks)}", va="center", fontsize=14, fontweight="bold")
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlim(0, 380)
    ax.set_xlabel("Day of the year")
    ax.set_title("Distinctive days to look back on", loc="left", fontsize=18, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "03_landmarks.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
