"""
WHY YOU CAN'T STOP SCROLLING

    uv run python scrolling_experiment.py

Simulates 5,000 users on each of three toy feeds, prints how long they
scrolled and saves still_scrolling.png. An illustrative toy model, not
research on real users, dopamine or addiction.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from experiment import N_USERS, run_experiment, still_scrolling

BG, PANEL, GRID, INK, MUTED = "#07080b", "#0d1016", "#343a46", "#eef1f6", "#aeb5c2"
COLORS = {"predictable": "#62d2c0", "unpredictable": "#f0b35e", "empty": "#ff7b6b"}

sessions = run_experiment()


def print_results():
    print(f"{N_USERS:,} simulated users per feed")
    print("feed            average   longest 10%")
    for name, s in sessions.items():
        print(f"{name:14}  {s.mean():5.1f}     {np.percentile(s, 90):5.0f} swipes")


def save_chart(path=Path("still_scrolling.png")):
    fig, ax = plt.subplots(figsize=(11, 6.2), facecolor=BG)
    ax.set_facecolor(PANEL)
    for name, s in sessions.items():
        x, y = still_scrolling(s)
        ax.plot(x, y, color=COLORS[name], linewidth=3, label=name)
    ax.set_xlim(1, 80)
    ax.set_xlabel("Swipe number", color=MUTED)
    ax.set_ylabel("Users still scrolling", color=MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(color=GRID, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=INK)
    ax.text(0.98, 0.94, "Illustrative toy model — not real-user data",
            transform=ax.transAxes, color=MUTED, fontsize=9, ha="right")
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=BG)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print_results()
    print("saved", save_chart())
    print("Done. Just one more swipe. Obviously.")
