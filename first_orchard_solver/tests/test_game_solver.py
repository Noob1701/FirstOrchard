"""
Tests for the First Orchard game solver.

This module contains unit tests for validating the win percentage
calculations and consistency between solver and Monte Carlo simulations for
the First Orchard game.
"""

import logging
from collections import Counter
from itertools import product
from typing import Tuple, cast

import numpy as np
import pytest
import pytest_check as check

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesims import run_batches
from first_orchard_solver.gameplay.gamesolver import win_perc, win_perc_comp


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


@pytest.fixture
def carlo_data() -> list[list[int]]:
    """Generate a list of all possible game states for the Orchard game."""
    unique_states = set()
    for full_inv_list in product(range(5), repeat=4):
        multiple_states = tuple(sorted(Counter(full_inv_list).items()))
        unique_states.add(multiple_states)
    result = []
    final_result = []
    for state in unique_states:
        sub_list = []
        for value, count in state:
            sub_list.extend([value] * count)
        result.append(sub_list)
    for sublist in result:
        for i in range(1, 6):
            final_result.append(sublist + [i])
    for item in final_result:
        assert len(item) == 5, f"Each item should have 5 elements.{len(item)} found."
        assert sum(item[:4]) <= 16
        assert sum(item[:4]) >= 0
        assert sum(item[4:]) <= 5
    assert len(final_result) == 350
    return final_result


@pytest.mark.parametrize(
    ("full_inv", "spaces", "strat", "expected"),
    [
        ((4, 4, 4, 4), 5, "small", 0.553),
        ((0, 0, 1, 0), 1, "small", 0.667),
        ((0, 0, 0, 2), 2, "small", 0.741),
        ((4, 4, 4, 4), 5, "large", 0.632),
        ((0, 0, 1, 0), 1, "large", 0.667),
        ((0, 0, 0, 2), 2, "large", 0.741),
        ((4, 4, 4, 4), 5, "random", 0.596),
        ((0, 0, 1, 0), 1, "random", 0.667),
        ((0, 0, 0, 2), 2, "random", 0.741),
    ],
)
def test_win_perc(
    full_inv: tuple[int, int, int, int], spaces: int, strat: str, expected: float
) -> None:
    """Simple quick test on known absolute values."""
    prob = win_perc(full_inv, spaces, strat)
    win_prob = prob[0]
    loss_prob = prob[1]
    # abs used for rounding errors (assertion 1) and random.choice (assertion 2)
    assert loss_prob + win_prob == pytest.approx(1, abs=0.02)
    "The win probability should be approximately 0.553."
    assert win_prob == pytest.approx(expected, abs=0.02)


logger = logging.getLogger(__name__)


def test_win_perc_against_carlo(carlo_data: list[list[int]]) -> None:
    """
    Ensure win_perc function is consistent with the Monte Carlo method.

    Use a known state and compare the outputs of the Monte Carlo simulation
    and the results from the solver.
    """
    game_state = GameState()
    for scenario in carlo_data:
        game_state.fruit_inventory.full_inv = {
            3: scenario[0],
            4: scenario[1],
            5: scenario[2],
            6: scenario[3],
        }
        game_state.raven_track.spaces = scenario[4]
        batches = run_batches(1000, 100, scenario[4], scenario[:4])
        solved_small = win_perc(tuple(scenario[:4]), scenario[4], "small")
        solved_large = win_perc(tuple(scenario[:4]), scenario[4], "large")
        solved_random = win_perc(tuple(scenario[:4]), scenario[4], "random")
        carlo_small = np.mean(batches.smallest_results) / 100
        carlo_large = np.mean(batches.largest_results) / 100
        carlo_random = np.mean(batches.random_results) / 100
        logger1.info(
            f"SCENARIO: {scenario} "
            f"SOLVED SMALL STRAT: {solved_small[0]} "
            f"CARLO: {carlo_small} "
            f"ABS_DIFFERENCE: {abs(solved_small[0] - carlo_small)}"
        )
        check.equal(carlo_small, pytest.approx(solved_small[0], abs=0.05))
        logger1.info(
            f"SCENARIO: {scenario} "
            f"SOLVED LARGE STRAT: {solved_large[0]} "
            f"CARLO: {carlo_large} "
            f"ABS_DIFFERENCE: {abs(solved_large[0] - carlo_large)}"
        )
        check.equal(carlo_large, pytest.approx(solved_large[0], abs=0.05))
        logger1.info(
            "WIN PERC"
            f"SCENARIO: {scenario} "
            f"SOLVED RANDOM STRAT: {solved_random[0]} "
            f"CARLO: {carlo_random} "
            f"DIFFERENCE: {abs(solved_random[0] - carlo_random)}"
        )
        check.equal(carlo_random, pytest.approx(solved_random[0], abs=0.05))


def test_win_perc_comp(carlo_data):
    """
    Test the win percentage comparison function with intended use scenarios.

    The intended use scenario is to compare two game states with the same amount of
    total fruit and raven spaces.
    """
    for i in range(len(carlo_data)):
        game_1 = carlo_data[i]
        game_1_sum = np.sum(game_1[:4])
        game_1_raven = game_1[-1]

        for j in range(i + 1, len(carlo_data)):
            game_state_1 = GameState()
            game_state_2 = GameState()
            game_2 = carlo_data[j]
            if np.sum(game_2[:4]) == game_1_sum and game_2[-1] == game_1_raven:
                game_state_1.fruit_inventory.full_inv = {
                    3: game_1[0],
                    4: game_1[1],
                    5: game_1[2],
                    6: game_1[3],
                }
                game_state_1.raven_track.spaces = game_1[4]
                game_state_2.fruit_inventory.full_inv = {
                    3: game_2[0],
                    4: game_2[1],
                    5: game_2[2],
                    6: game_2[3],
                }
                game_state_2.raven_track.spaces = game_2[4]
                tuple_1 = tuple(game_state_1.fruit_inventory.full_inv.values())
                tuple_2 = tuple(game_state_2.fruit_inventory.full_inv.values())
                tuple_1 = cast(Tuple[int, int, int, int], tuple_1)
                tuple_2 = cast(Tuple[int, int, int, int], tuple_2)
                solved_comp = win_perc_comp(
                    tuple_1,
                    game_state_1.raven_track.spaces,
                    tuple_2,
                    game_state_2.raven_track.spaces,
                )
                assert solved_comp[0] >= 0
                assert solved_comp[0] <= 100
                assert solved_comp[1] >= 0
                assert solved_comp[1] <= 100

                game_1_batches = run_batches(
                    1000,
                    100,
                    game_state_1.raven_track.spaces,
                    list(game_state_1.fruit_inventory.full_inv.values()),
                )
                game_2_batches = run_batches(
                    1000,
                    100,
                    game_state_2.raven_track.spaces,
                    list(game_state_2.fruit_inventory.full_inv.values()),
                )
                game_1_batch_mean = np.mean(game_1_batches.largest_results) / 100
                game_2_batch_mean = np.mean(game_2_batches.largest_results) / 100
                carlo_comp = abs(game_1_batch_mean - game_2_batch_mean)
                logger2.info(
                    f"WIN_PERC_COMP: "
                    f"SCENARIO_1: {game_state_1.fruit_inventory.full_inv} "
                    f"{game_state_1.raven_track.spaces} "
                    f"SCENARIO_2: {game_state_2.fruit_inventory.full_inv} "
                    f"{game_state_2.raven_track.spaces} "
                    f"CARLO_1: {game_1_batch_mean} "
                    f"CARLO_2: {game_2_batch_mean} "
                    f"CARLO_DIFF: {carlo_comp} "
                    f"SOLVED_COMP: {solved_comp[0]/100} "
                )
                check.equal(carlo_comp, pytest.approx(solved_comp[0] / 100, abs=0.05))
