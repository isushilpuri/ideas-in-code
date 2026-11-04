from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SimulationConfig:
    players: int = 10_000
    rounds: int = 100
    starting_wealth: float = 100.0
    win_probability: float = 0.5
    win_multiplier: float = 1.5
    loss_multiplier: float = 0.6
    seed: int = 42

    def validate(self) -> None:
        if self.players < 2:
            raise ValueError("players must be at least 2")
        if self.rounds < 1:
            raise ValueError("rounds must be at least 1")
        if self.starting_wealth <= 0:
            raise ValueError("starting_wealth must be positive")
        if not 0 < self.win_probability < 1:
            raise ValueError("win_probability must be between 0 and 1")
        if self.win_multiplier <= 0 or self.loss_multiplier <= 0:
            raise ValueError("multipliers must be positive")


@dataclass
class SimulationResult:
    config: SimulationConfig
    wins: np.ndarray
    wealth_paths: np.ndarray

    @property
    def final_wealth(self) -> np.ndarray:
        return self.wealth_paths[:, -1]


def run_simulation(config: SimulationConfig) -> SimulationResult:
    """Run all players through the same independent multiplicative bet."""
    config.validate()
    rng = np.random.default_rng(config.seed)

    players, rounds = config.players, config.rounds
    wins = rng.random((players, rounds)) < config.win_probability
    multipliers = np.where(
        wins,
        config.win_multiplier,
        config.loss_multiplier,
    )

    start = np.full((players, 1), config.starting_wealth)
    growth = np.cumprod(multipliers, axis=1)
    wealth_paths = np.hstack([start, start * growth])

    return SimulationResult(
        config=config,
        wins=wins,
        wealth_paths=wealth_paths,
    )
