from collections import Counter
from itertools import product

import numpy as np
import pytest

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesims import run_batches
from first_orchard_solver.gameplay.gamesolver import win_perc


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
)  # type: ignore[misc]
def test_win_perc(
    full_inv: tuple[int, int, int, int], spaces: int, strat: str, expected: float
) -> None:
    prob = win_perc(full_inv, spaces, strat)
    win_prob = prob[0]
    loss_prob = prob[1]
    assert loss_prob + win_prob == pytest.approx(1, abs=0.02)
    "The win probability should be approximately 0.553."
    assert win_prob == pytest.approx(expected, abs=0.05)


def test_win_perc_against_carlo() -> None:
    """
    This test is to ensure that the win_perc function is consistent with the
    Monte Carlo method.It uses a known state and compares the output to
    the expected value.
    """
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
    game_state = GameState()
    for scenario in final_result:
        game_state.fruit_inventory.full_inv = {
            3: scenario[0],
            4: scenario[1],
            5: scenario[2],
            6: scenario[3],
        }
        game_state.raven_track.spaces = scenario[4]
        batches = run_batches(2000, 100, scenario[4], scenario[:4])
        solved_small = win_perc(tuple(scenario[:4]), scenario[4], "small")
        solved_large = win_perc(tuple(scenario[:4]), scenario[4], "large")
        solved_random = win_perc(tuple(scenario[:4]), scenario[4], "random")
        assert np.mean(batches.smallest_results) / 100 == pytest.approx(
            solved_small[0], abs=0.05
        )
        assert np.mean(batches.largest_results) / 100 == pytest.approx(
            solved_large[0], abs=0.05
        )
        assert np.mean(batches.random_results) / 100 == pytest.approx(
            solved_random[0], abs=0.05
        )
