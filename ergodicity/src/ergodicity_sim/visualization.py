from __future__ import annotations

from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.ticker import FuncFormatter

from .simulation import SimulationResult
from .analysis import theoretical_metrics


# Noetic Room — Editorial Clean palette
PAPER = "#F4EBD5"
PANEL = "#FFF9EA"
INK = "#252525"
MUTED = "#77736A"
GRID = "#DED5C2"
CORAL = "#D97855"
TEAL = "#399D91"
GOLD = "#E8C94F"


def _style_axis(ax, title: str) -> None:
    ax.set_facecolor(PANEL)
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=12)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)


def _money(x, _):
    if x >= 1_000_000:
        return f"${x/1_000_000:.0f}M"
    if x >= 1_000:
        return f"${x/1_000:.0f}k"
    if x >= 1:
        return f"${x:.0f}"
    return f"${x:.2f}"


def save_static_charts(result: SimulationResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = result.wealth_paths
    c = result.config
    rounds = np.arange(c.rounds + 1)
    mean = paths.mean(axis=0)
    median = np.median(paths, axis=0)

    # Wealth paths overview: show a readable subset, calculate statistics on everyone.
    rng = np.random.default_rng(c.seed + 1)
    sample_n = min(220, c.players)
    sample_idx = rng.choice(c.players, size=sample_n, replace=False)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), facecolor=PAPER)
    fig.subplots_adjust(left=0.09, right=0.96, top=0.83, bottom=0.14)
    _style_axis(ax, "10,000 parallel players — individual wealth trajectories")
    for idx in sample_idx:
        ax.plot(rounds, paths[idx], color=TEAL, alpha=0.10, linewidth=0.65)
    ax.plot(rounds, mean, color=CORAL, linewidth=3, label="Ensemble mean")
    ax.plot(rounds, median, color=INK, linewidth=2.5, label="Median player")
    ax.axhline(c.starting_wealth, color=GOLD, linewidth=1.8, linestyle="--",
               label="Starting wealth ($100)")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(_money))
    ax.set_xlabel("BET NUMBER", color=MUTED, labelpad=10)
    ax.set_ylabel("WEALTH (LOG SCALE)", color=MUTED, labelpad=10)
    ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=9)
    fig.suptitle("THE WINNING BET THAT RUINS YOU", x=0.09, y=0.95,
                 ha="left", fontsize=23, fontweight="bold", color=INK)
    fig.text(0.09, 0.895, "A 50/50 bet: +50% on a win, −40% on a loss",
             color=MUTED, fontsize=11)
    fig.savefig(output_dir / "wealth_paths.png", dpi=160, facecolor=PAPER)
    plt.close(fig)

    # Final distribution on log wealth axis.
    final = result.final_wealth
    fig, ax = plt.subplots(figsize=(13.33, 7.5), facecolor=PAPER)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.82, bottom=0.17)
    _style_axis(ax, "Where everyone ended up")
    log_final = np.log10(final)
    ax.hist(log_final, bins=55, color=TEAL, alpha=0.85, edgecolor=PANEL, linewidth=0.6)
    start_log = np.log10(c.starting_wealth)
    ax.axvline(start_log, color=CORAL, linewidth=2.5, linestyle="--",
               label="Starting wealth ($100)")
    ax.set_xlabel("FINAL WEALTH — LOG SCALE", color=MUTED, labelpad=10)
    ax.set_ylabel("NUMBER OF PLAYERS", color=MUTED, labelpad=10)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3, 4, 5])
    ax.set_xticklabels(["$0.001", "$0.01", "$0.1", "$1", "$10", "$100",
                        "$1k", "$10k", "$100k"])
    below = np.mean(final < c.starting_wealth) * 100
    ax.text(0.98, 0.94, f"{below:.1f}% finished below $100",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=14, color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper left")
    fig.suptitle("THE CROWD AND THE OUTLIERS", x=0.10, y=0.95,
                 ha="left", fontsize=23, fontweight="bold", color=INK)
    fig.savefig(output_dir / "final_distribution.png", dpi=160, facecolor=PAPER)
    plt.close(fig)


def render_animation(result: SimulationResult, output_dir: Path, fps: int = 30) -> Path:
    """Render an animated overview. MP4 requires FFmpeg; otherwise writes GIF."""
    output_dir.mkdir(parents=True, exist_ok=True)
    c = result.config
    paths = result.wealth_paths
    rounds = np.arange(c.rounds + 1)
    mean = paths.mean(axis=0)
    median = np.median(paths, axis=0)

    rng = np.random.default_rng(c.seed + 2)
    sample_n = min(180, c.players)
    sample_idx = rng.choice(c.players, size=sample_n, replace=False)

    fig = plt.figure(figsize=(16, 9), facecolor=PAPER)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.65, 1], height_ratios=[1, 0.12],
                          left=0.07, right=0.96, top=0.83, bottom=0.10,
                          wspace=0.23, hspace=0.30)
    ax_main = fig.add_subplot(gs[0, 0])
    ax_dist = fig.add_subplot(gs[0, 1])
    ax_footer = fig.add_subplot(gs[1, :])
    ax_footer.axis("off")

    _style_axis(ax_main, "THE SAME BET. 10,000 DIFFERENT LIVES.")
    _style_axis(ax_dist, "FINAL WEALTH DISTRIBUTION")
    ax_main.set_yscale("log")
    ax_main.set_xlim(0, c.rounds)
    positive = paths[paths > 0]
    y_min = max(float(np.min(positive)) * 0.5, 1e-12)
    y_max = float(np.max(paths)) * 1.35
    ax_main.set_ylim(y_min, y_max)
    ax_main.yaxis.set_major_formatter(FuncFormatter(_money))
    ax_main.set_xlabel("BET NUMBER", color=MUTED)
    ax_main.set_ylabel("WEALTH — LOG SCALE", color=MUTED)

    # A faint bundle of sampled paths, plus the two population statistics.
    player_lines = [
        ax_main.plot([], [], color=TEAL, alpha=0.16, linewidth=0.8)[0]
        for _ in sample_idx
    ]
    mean_line, = ax_main.plot([], [], color=CORAL, linewidth=3.3, label="Ensemble mean")
    median_line, = ax_main.plot([], [], color=INK, linewidth=2.7, label="Median player")
    ax_main.axhline(c.starting_wealth, color=GOLD, linewidth=1.8, linestyle="--",
                    label="Starting $100")
    ax_main.legend(frameon=False, fontsize=9, loc="upper left")

    # Final distribution is shown as a destination preview, progressively revealed.
    final_log = np.log10(result.final_wealth)
    bins = np.linspace(float(final_log.min()) - 0.05, float(final_log.max()) + 0.05, 45)
    counts, edges = np.histogram(final_log, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    bars = ax_dist.bar(centers, np.zeros_like(counts), width=np.diff(edges) * 0.86,
                       color=TEAL, alpha=0.88)
    ax_dist.axvline(np.log10(c.starting_wealth), color=CORAL, linewidth=2,
                    linestyle="--", label="Starting $100")
    ax_dist.set_xlabel("FINAL WEALTH — LOG SCALE", color=MUTED)
    ax_dist.set_ylabel("PLAYERS", color=MUTED)
    ax_dist.set_ylim(0, max(counts) * 1.25 + 1)
    ax_dist.legend(frameon=False, fontsize=8, loc="upper right")
    ax_dist.set_xticks([-2, 0, 2, 4, 6])
    ax_dist.set_xticklabels(["$0.01", "$1", "$100", "$10k", "$1M"])

    title = fig.suptitle("THE WINNING BET THAT RUINS YOU",
                         x=0.07, y=0.95, ha="left",
                         fontsize=25, fontweight="bold", color=INK)
    subtitle = fig.text(0.07, 0.895,
                        "50% chance: +50%     |     50% chance: −40%     |     Expected return: +5%",
                        fontsize=12, color=MUTED)
    stat_text = ax_footer.text(0.0, 0.42, "", fontsize=13, color=INK,
                               fontweight="bold", transform=ax_footer.transAxes)

    def update(frame: int):
        x = rounds[:frame + 1]
        for line, idx in zip(player_lines, sample_idx):
            line.set_data(x, paths[idx, :frame + 1])
        mean_line.set_data(x, mean[:frame + 1])
        median_line.set_data(x, median[:frame + 1])

        # Reveal the final distribution progressively as the experiment runs.
        reveal = frame / max(c.rounds, 1)
        for bar, count in zip(bars, counts):
            bar.set_height(count * reveal)

        stat_text.set_text(
            f"BET {frame:03d}/{c.rounds}     "
            f"MEAN  {_money(mean[frame], None)}     "
            f"MEDIAN  {_money(median[frame], None)}"
        )
        return (*player_lines, mean_line, median_line, *bars, stat_text)

    animation = FuncAnimation(
        fig, update, frames=c.rounds + 1, interval=1000 / fps,
        blit=False, repeat=False,
    )

    mp4_path = output_dir / "ergodicity_simulation.mp4"
    gif_path = output_dir / "ergodicity_simulation.gif"

    try:
        if shutil.which("ffmpeg"):
            animation.save(mp4_path, writer=FFMpegWriter(fps=fps, bitrate=5000),
                           dpi=120)
            output_path = mp4_path
        else:
            animation.save(gif_path, writer=PillowWriter(fps=min(fps, 20)), dpi=90)
            output_path = gif_path
    finally:
        plt.close(fig)

    return output_path
