"""You're Not Your Mind: same thoughts, two responses.

A toy simulation, not a measurement of brain activity. Writes
youre_not_your_mind.gif (the animation) and youre_not_your_mind.png (the final frame).
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from agents import simulate
from thoughts import N_THOUGHTS, generate_thoughts

BG, GRID, INK, MUTED = "#07080b", "#343a46", "#eef1f6", "#aeb5c2"
COLORS = {"A": "#ff7b6b", "B": "#62d2c0"}

thoughts = generate_thoughts()
histories = {agent: simulate(thoughts, agent) for agent in COLORS}

fig, axes = plt.subplots(2, 1, figsize=(11, 6.2), sharex=True, facecolor=BG)
lines = {}
for ax, (agent, color) in zip(axes, COLORS.items()):
    ax.set_facecolor(BG)
    ax.set_xlim(0, N_THOUGHTS)
    ax.set_ylim(0, 2)
    ax.set_ylabel(f"Agent {agent}", color=color)
    ax.tick_params(colors=MUTED)
    ax.grid(color=GRID, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    lines[agent], = ax.plot([], [], color=color, linewidth=2.8)
axes[-1].set_xlabel("Thoughts encountered (illustrative)", color=MUTED)


def update(frame):
    for agent, line in lines.items():
        line.set_data(range(frame + 2), histories[agent][:frame + 2])
    return list(lines.values())


animation = FuncAnimation(fig, update, frames=N_THOUGHTS, interval=200, blit=False)


def summary():
    print("Same thoughts. Different responses.")
    print(f"Thoughts simulated: {N_THOUGHTS}")
    print(f"{'':10}{'average':>10}{'peak':>8}")
    for agent, history in histories.items():
        print(f"Agent {agent}:  {sum(history) / len(history):10.2f}{max(history):8.2f}")


if __name__ == "__main__":
    animation.save("youre_not_your_mind.gif", writer=PillowWriter(fps=5), dpi=100)
    fig.savefig("youre_not_your_mind.png", dpi=180, facecolor=BG)
    summary()
