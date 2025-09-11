"""
Tests for the First Orchard game solver.

This module contains unit tests for validating the win percentage
calculations and consistency between solver and Monte Carlo simulations for
the First Orchard game.
"""

import logging
from collections import Counter
from itertools import product
from typing import Dict, List, Tuple

import numpy as np
import pytest
import pytest_check as check

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesims import Strategy, run_batches
from first_orchard_solver.gameplay.gamesolver import win_perc, win_perc_comp
from first_orchard_solver.tests.test_gamelogic import _set_state


def get_test_logger(name: str, log_file: str) -> logging.Logger:
    """Create a logger for testing purposes."""
    # Create or get a named logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Clear existing handlers for clean setup
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler (write to specified file)
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.INFO)

    # Console handler (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger1 = get_test_logger(name="win_perc_test", log_file="win_perc_test.log")
logger2 = get_test_logger(name="win_perc_comp_test", log_file="win_perc_comp_test.log")
logger3 = get_test_logger(name="strategy_test", log_file="strategy_test.log")


@pytest.fixture
def game_state_fixture():
    """Set up game_state_fixture for testing."""
    return GameState()


@pytest.fixture
def game_state_fixture_2():
    """Set up game_state_fixture_2 for comparison testing."""
    return GameState()


@pytest.fixture
def test_data() -> List[Tuple[Dict[int, int], int]]:
    """Generates all possible Orchard game states as (fruit dict, raven_track)."""
    unique_states = set()
    for fruit_inventory_list in product(range(5), repeat=4):
        multiple_states = tuple(sorted(Counter(fruit_inventory_list).items()))
        unique_states.add(multiple_states)

    final_result: List[Tuple[Dict[int, int], int]] = []
    for state in unique_states:
        # always have keys 3,4,5,6 initialized to 0
        sub_dict: Dict[int, int] = {3: 0, 4: 0, 5: 0, 6: 0}
        next_key = 3

        # expand values into slots: e.g. (2,2),(3,2) → {3:2,4:2,5:3,6:3}
        for value, count in state:
            for _ in range(count):
                sub_dict[next_key] = value
                next_key += 1

        for raven_track in range(1, 6):
            final_result.append((sub_dict.copy(), raven_track))

    # Sanity checks
    for fruit_dict, raven_track in final_result:
        assert len(fruit_dict.keys()) == 4
        assert 0 <= sum(fruit_dict.values()) <= 16
        assert 0 <= raven_track <= 5
    assert len(final_result) == 350

    return final_result


@pytest.mark.parametrize(
    ("fruit_inventory", "raven_track", "strat", "expected"),
    [
        ({3: 4, 4: 4, 5: 4, 6: 4}, 5, "fewest", 0.553),
        ({3: 0, 4: 0, 5: 1, 6: 0}, 1, "fewest", 0.667),
        ({3: 0, 4: 0, 5: 0, 6: 2}, 2, "fewest", 0.741),
        ({3: 4, 4: 4, 5: 4, 6: 4}, 5, "most", 0.632),
        ({3: 0, 4: 0, 5: 1, 6: 0}, 1, "most", 0.667),
        ({3: 0, 4: 0, 5: 0, 6: 2}, 2, "most", 0.741),
        ({3: 4, 4: 4, 5: 4, 6: 4}, 5, "random", 0.596),
        ({3: 0, 4: 0, 5: 1, 6: 0}, 1, "random", 0.667),
        ({3: 0, 4: 0, 5: 0, 6: 2}, 2, "random", 0.741),
    ],
)
def test_win_perc(
    game_state_fixture: GameState,
    fruit_inventory: Dict[int, int],
    raven_track: int,
    strat: Strategy,
    expected: float,
) -> None:
    """Simple quick test on known absolute values."""
    _set_state(game_state_fixture, fruit_inventory, raven_track)
    prob = win_perc(
        game_state_fixture.fruit_inventory.fruit_values,
        game_state_fixture.raven_track.spaces,
        strat,
    )
    win_prob = prob[0]
    loss_prob = prob[1]
    # abs used for rounding errors (assertion 1) and random.choice (assertion 2)
    assert loss_prob + win_prob == pytest.approx(1, abs=0.02)
    "The win probability should be approximately 0.553."
    assert win_prob == pytest.approx(expected, abs=0.02)


logger = logging.getLogger(__name__)


def test_win_perc_against_carlo(
    game_state_fixture: GameState, test_data: List[Tuple[Dict[int, int], int]]
) -> None:
    """
    Ensure win_perc function is consistent with the Monte Carlo method.

    Use a known state and compare the outputs of the Monte Carlo simulation
    and the results from the solver.
    """
    for game_component in test_data:
        _set_state(game_state_fixture, game_component[0], game_component[1])
        batches = run_batches(
            game_state_fixture, 100, 1000, ["fewest", "most", "random"]
        )
        solved_least = win_perc(
            game_state_fixture.fruit_inventory.fruit_values,
            game_state_fixture.raven_track.spaces,
            "fewest",
        )
        solved_most = win_perc(
            game_state_fixture.fruit_inventory.fruit_values,
            game_state_fixture.raven_track.spaces,
            "most",
        )
        solved_random = win_perc(
            game_state_fixture.fruit_inventory.fruit_values,
            game_state_fixture.raven_track.spaces,
            "random",
        )
        carlo_small = np.mean(batches.fewest_strat_runs) / 100
        carlo_large = np.mean(batches.most_strat_runs) / 100
        carlo_random = np.mean(batches.random_strat_runs) / 100
        logger1.info(
            f"SCENARIO: {game_component} "
            f"SOLVED SMALL STRAT: {solved_least[0]} "
            f"CARLO: {carlo_small} "
            f"ABS_DIFFERENCE: {abs(solved_least[0] - carlo_small)}"
        )
        check.equal(carlo_small, pytest.approx(solved_least[0], abs=0.05))
        logger1.info(
            f"SCENARIO: {game_component} "
            f"SOLVED LARGE STRAT: {solved_most[0]} "
            f"CARLO: {carlo_large} "
            f"ABS_DIFFERENCE: {abs(solved_most[0] - carlo_large)}"
        )
        check.equal(carlo_large, pytest.approx(solved_most[0], abs=0.05))
        logger1.info(
            "WIN PERC"
            f"SCENARIO: {game_component} "
            f"SOLVED RANDOM STRAT: {solved_random[0]} "
            f"CARLO: {carlo_random} "
            f"ABS_DIFFERENCE: {abs(solved_random[0] - carlo_random)}"
        )
        check.equal(carlo_random, pytest.approx(solved_random[0], abs=0.05))


def test_win_perc_comp(
    game_state_fixture: GameState,
    game_state_fixture_2: GameState,
    test_data: List[Tuple[Dict[int, int], int]],
) -> None:
    """
    Test the win percentage comparison function with intended use scenarios.

    The intended use scenario is to compare two game states with the same amount of
    total fruit and raven spaces.
    """
    for i in range(len(test_data)):
        game_1 = test_data[i]
        game_1_sum = sum(game_1[0].values())
        game_1_raven = game_1[-1]

        for j in range(i + 1, len(test_data)):
            game_2 = test_data[j]
            if sum(game_2[0].values()) == game_1_sum and game_2[-1] == game_1_raven:
                _set_state(game_state_fixture, test_data[i][0], game_1_raven)
                _set_state(game_state_fixture_2, test_data[j][0], game_1_raven)
                solved_comp = win_perc_comp(game_state_fixture, game_state_fixture_2)
                assert solved_comp[0] >= 0
                assert solved_comp[0] <= 100
                assert solved_comp[1] >= 0
                assert solved_comp[1] <= 100

                game_1_batches = run_batches(game_state_fixture, 100, 1000)
                game_2_batches = run_batches(game_state_fixture_2, 100, 1000)
                game_1_batch_mean = np.mean(game_1_batches.most_strat_runs) / 100
                game_2_batch_mean = np.mean(game_2_batches.most_strat_runs) / 100
                carlo_comp = abs(game_1_batch_mean - game_2_batch_mean)
                logger2.info(
                    f"WIN_PERC_COMP: "
                    f"SCENARIO_1:"
                    f"{game_state_fixture.fruit_inventory.fruit_values}"
                    f"{game_state_fixture.raven_track.spaces} "
                    f"SCENARIO_2:"
                    f"{game_state_fixture_2.fruit_inventory.fruit_values} "
                    f"{game_state_fixture_2.raven_track.spaces} "
                    f"CARLO_1: {game_1_batch_mean} "
                    f"CARLO_2: {game_2_batch_mean} "
                    f"CARLO_DIFF: {carlo_comp} "
                    f"SOLVED_DIFF: {solved_comp[0]/100} "
                    f"CARLO_SOLVED_ABS_DIFF: {abs(carlo_comp - solved_comp[0]/100)}"
                )
                check.equal(carlo_comp, pytest.approx(solved_comp[0] / 100, abs=0.05))


def test_strategies(
    game_state_fixture: GameState, test_data: List[Tuple[Dict[int, int], int]]
) -> None:
    """
    Tests to ensure that largest strategy is never worse than other strategies.

    Note: This is more of a mathematical test than a programming test. As the math from
    game_solver, indicates that choosing from one of the fruit types with the most
    fruits is always the best strategy. This is a formal test of that.

    Note to self: I had thoughts about making this test more specific but found that
    there really wasn't much more to be done. Most should always be the max or tied for
    max, but when all the fruits have the same amount we can only expect the most
    strategy to be strtictly better than the fewest, given the current set up of random.
    Which is a known limitation of the current set up. And that is really not high on
    my to do list at all for this project.
    """
    for game_component in test_data:
        _set_state(game_state_fixture, game_component[0], game_component[1])
        fruit_values = game_state_fixture.fruit_inventory.fruit_values
        spaces = game_state_fixture.raven_track.spaces
        results = {
            strat: win_perc(fruit_values, spaces, strat)
            for strat in ["most", "fewest", "random"]
        }
        # below code unpacks win_perc win odds
        win_perc_results = {k: v[0] for k, v in results.items()}
        logger3.info(f"SCENARIO: {game_component} STRATEGY RESULTS: {win_perc_results}")
        assert results["most"][0] == max(val[0] for val in results.values())
        # There are cases the below code doesn't test, but should, such as 0, 1, 1, 2.
        # But the test is sufficent as is for a reasonable human. Might fix later as
        # a hacker rank like problem
        if len(set(fruit_values)) != 1 and all(fruit_values) > 0:
            assert results["most"][0] > results["fewest"][0]
