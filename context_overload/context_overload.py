"""
THE CONTEXT OVERLOAD EXPERIMENT

    uv run python context_overload.py

Prints the success rate of both toy agents as irrelevant notes pile up and
saves context_overload.png. Illustrative toy model, not a real LLM benchmark.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiment import N_TRIALS, NOISE_LEVELS, run_experiment

BG, PANEL, GRID, INK, MUTED = "#07080b", "#0d1016", "#343a46", "#eef1f6", "#aeb5c2"
AMBER, TEAL = "#f0b35e", "#62d2c0"

results = run_experiment()
stuffing = results["stuffing"].mean(axis=1)
filtering = results["filtering"].mean(axis=1)


def print_results():
    print(f"{N_TRIALS} trials per level, {len(NOISE_LEVELS)} noise levels")
    print("noise   stuffing   filtering")
    for n, s, f in zip(NOISE_LEVELS, stuffing, filtering):
        if n % 20 == 0:
            print(f"{n:5d}   {s:8.1%}   {f:9.1%}")


def save_chart(path=Path("context_overload.png")):
    fig, ax = plt.subplots(figsize=(11, 6.2), facecolor=BG)
    ax.set_facecolor(PANEL)
    ax.plot(NOISE_LEVELS, stuffing, color=AMBER, linewidth=3, label="Stuff everything")
    ax.plot(NOISE_LEVELS, filtering, color=TEAL, linewidth=3, label="Filter first")
    ax.set_ylim(0.4, 1.02)
    ax.set_xlabel("Irrelevant notes in context", color=MUTED)
    ax.set_ylabel("Answered correctly", color=MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(color=GRID, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=INK, loc="lower left")
    ax.text(0.98, 0.04, "Illustrative toy model — not a real LLM benchmark",
            transform=ax.transAxes, color=MUTED, fontsize=9, ha="right")
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=BG)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print_results()
    print("saved", save_chart())
    print("Done. Your AI has read everything. It would now like a nap.")
