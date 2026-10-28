"""Hundreds of trials per noise level, for both agents."""

import numpy as np

from agent import FACT, NOISE, filtering_agent, stuffing_agent

SEED = 42
N_TRIALS = 500
NOISE_LEVELS = np.arange(0, 101, 5)
ANSWER = "14 June"

AGENTS = {"stuffing": stuffing_agent, "filtering": filtering_agent}


def build_context(n_noise, rng):
    """One relevant fact, buried among n irrelevant notes."""
    context = [str(note) for note in rng.choice(NOISE, size=n_noise)]
    context.insert(int(rng.integers(0, n_noise + 1)), FACT)
    return context


def trials(agent, n_noise, rng):
    """True wherever the agent got the answer right."""
    return np.array([
        agent(build_context(n_noise, rng), rng) == ANSWER
        for _ in range(N_TRIALS)
    ])


def run_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    return {
        name: np.array([trials(agent, n, rng) for n in NOISE_LEVELS])
        for name, agent in AGENTS.items()
    }
