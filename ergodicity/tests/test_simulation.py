import numpy as np
import pytest
from ergodicity_sim.analysis import theoretical_metrics
from ergodicity_sim.simulation import SimulationConfig, run_simulation


def test_simulation_shape_and_starting_wealth():
    result = run_simulation(SimulationConfig(players=100, rounds=10, seed=7))
    assert result.wealth_paths.shape == (100, 11)
    assert np.all(result.wealth_paths[:, 0] == 100)
    assert np.all(result.final_wealth > 0)


def test_same_seed_is_reproducible():
    config = SimulationConfig(players=100, rounds=10, seed=12)
    a = run_simulation(config)
    b = run_simulation(config)
    assert np.array_equal(a.wealth_paths, b.wealth_paths)


def test_the_numbers_the_video_quotes():
    result = run_simulation(SimulationConfig())
    final = result.final_wealth
    assert np.median(final) == pytest.approx(100 * 0.9**50)
    assert 0.86 < np.mean(final < 100) < 0.87
    summary = theoretical_metrics(result)
    assert summary["expected_final_wealth"] == pytest.approx(13150.13, abs=0.01)
    assert summary["theoretical_probability_below_start"] == pytest.approx(0.8644, abs=0.0001)
