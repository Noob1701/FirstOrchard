"""Unit tests for the game logic of the Orchard game."""

from typing import Dict

import pytest

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesims import Strategy, _play_with_strat


def _set_inventory(game_state: GameState, fruit_inventory: Dict[int, int]) -> GameState:
    game_state.fruit_inventory.fruit_inventory.clear()
    game_state.fruit_inventory.fruit_inventory.update(fruit_inventory)
    return game_state


def _set_state(
    game_state: GameState, fruit_inventory: Dict[int, int], spaces: int
) -> GameState:
    _set_inventory(game_state, fruit_inventory)
    game_state.raven_track.spaces = spaces
    return game_state


@pytest.fixture
def game_state_fixture() -> GameState:
    """Set up a fresh GameContext for testing."""
    return GameState()


@pytest.mark.parametrize(
    "fruit_inventory, expected",
    [
        ({3: 1, 4: 2, 5: 3, 6: 4}, {3: 0, 4: 2, 5: 3, 6: 4}),
        ({3: 0, 4: 1, 5: 2, 6: 3}, {3: 0, 4: 0, 5: 2, 6: 3}),
        ({3: 2, 4: 4, 5: 2, 6: 0}, {3: 1, 4: 4, 5: 2, 6: 0}),
    ],
)
def test_fewest_strat(
    game_state_fixture: GameState,
    fruit_inventory: Dict[int, int],
    expected: Dict[int, int],
) -> None:
    """Test the smallest strategy of FruitInventory."""
    _set_inventory(game_state_fixture, fruit_inventory)
    game_state_fixture.fruit_inventory.fewest_strat()
    assert game_state_fixture.fruit_inventory.fruit_inventory == expected


# test_largest_strat
@pytest.mark.parametrize(
    "fruit_inventory, expected",
    [
        ({3: 1, 4: 2, 5: 3, 6: 4}, {3: 1, 4: 2, 5: 3, 6: 3}),
        ({3: 0, 4: 1, 5: 2, 6: 3}, {3: 0, 4: 1, 5: 2, 6: 2}),
        ({3: 1, 4: 0, 5: 1, 6: 0}, {3: 0, 4: 0, 5: 1, 6: 0}),
    ],
)
def test_largest_strat(
    game_state_fixture: GameState,
    fruit_inventory: Dict[int, int],
    expected: Dict[int, int],
) -> None:
    """Test the largest strategy of FruitInventory."""
    _set_inventory(game_state_fixture, fruit_inventory)
    game_state_fixture.fruit_inventory.most_strat()
    assert game_state_fixture.fruit_inventory.fruit_inventory == expected


# test_random_strat
@pytest.mark.parametrize(
    "fruit_inventory, expected",
    [
        ({3: 1, 4: 2, 5: 3, 6: 4}, 9),
        ({3: 0, 4: 1, 5: 2, 6: 3}, 5),
        ({3: 2, 4: 4, 5: 2, 6: 0}, 7),
    ],
)
def test_random_strat(
    game_state_fixture: GameState, fruit_inventory: Dict[int, int], expected: int
) -> None:
    """Test the random strategy of FruitInventory."""
    _set_inventory(game_state_fixture, fruit_inventory)
    game_state_fixture.fruit_inventory.most_strat()
    total = sum(game_state_fixture.fruit_inventory.fruit_inventory.values())
    assert total == expected


# test_check_zeros
@pytest.mark.parametrize(
    "fruit_inventory, expected",
    [
        ({3: 1, 4: 2, 5: 3, 6: 4}, True),
        ({3: 0, 4: 0, 5: 0, 6: 0}, False),
        ({3: 2, 4: 0, 5: 1, 6: 0}, True),
    ],
)
def test_check_not_zero(
    game_state_fixture: GameState, fruit_inventory: Dict[int, int], expected: bool
) -> None:
    """Test the check_not_zero method of FruitInventory."""
    _set_inventory(game_state_fixture, fruit_inventory)
    assert game_state_fixture.fruit_inventory.check_not_zero() == expected


# test_is_game_over
@pytest.mark.parametrize(
    "raven_track, fruit_inventory, expected",
    [
        (0, {3: 1, 4: 2, 5: 3, 6: 4}, True),
        (1, {3: 0, 4: 0, 5: 0, 6: 0}, True),
        (5, {3: 2, 4: 0, 5: 1, 6: 0}, False),
    ],
)
def test_is_game_over(
    game_state_fixture: GameState,
    fruit_inventory: Dict[int, int],
    raven_track: int,
    expected: bool,
) -> None:
    """Test the is_game_over method of GameState."""
    _set_state(game_state_fixture, fruit_inventory, raven_track)
    assert game_state_fixture.is_game_over() == expected


# test_play_with_strat
@pytest.mark.parametrize("strat", ["fewest", "most", "random"])
def test_play_with_strat(game_state_fixture: GameState, strat: Strategy) -> None:
    """
    Test the play_with_strat function with different strategies.

    Only checks if the game ends.

    """
    game_state_fixture = _play_with_strat(game_state_fixture, strat)
    assert game_state_fixture.is_game_over()
    assert (
        game_state_fixture.raven_track.spaces == 0
        or not game_state_fixture.fruit_inventory.check_not_zero()
    )
