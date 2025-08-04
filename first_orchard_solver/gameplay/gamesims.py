"""Module to handle game simulations for the Orchard game."""

import copy
from typing import List, Optional

from first_orchard_solver.gameplay.gamelogic import GameState


class GameResults:
    """Stores the results of a game run."""

    def __init__(self) -> None:
        """Initialize the game results with counters for raven and fruit ends."""
        self.raven_end = 0
        self.fruit_end = 0


class MultIterGame:
    """
    Stores results of multiple iterations of the game.

    With particular strategies chosen.
    """

    def __init__(self) -> None:
        """Initialize the game results with empty lists for different strategies."""
        self.smallest_results: List[int] = []
        self.largest_results: List[int] = []
        self.random_results: List[int] = []


def play_with_strat(
    strat: str, spaces: int = 5, full_inv: Optional[List[int]] = None
) -> GameState:
    """Play the Orchard game with a specific strategy and return final game state."""
    if full_inv is None:
        full_inv = [4, 4, 4, 4]
    game_state = GameState()
    game_state.raven_track.spaces = spaces
    for key, new_value in zip(game_state.fruit_inventory.full_inv, full_inv):
        game_state.fruit_inventory.full_inv[key] = new_value
    while not game_state.is_game_over():
        result = game_state.orchard_die.roll()
        strategies = {
            "smallest": game_state.fruit_inventory.smallest_strat,
            "largest": game_state.fruit_inventory.largest_strat,
            "random": game_state.fruit_inventory.random_strat,
        }
        if result == 2:
            if strat in strategies:
                strategies[strat]()
        elif result == 1:
            game_state.raven_track.decrement_raven()
        else:
            game_state.fruit_inventory.decrement_fruit(result)

    return game_state


def run_strat_ntimes(
    n_runs: int, strat: str, spaces: int = 5, full_inv: Optional[List[int]] = None
) -> GameResults:
    """Run a specific strategy for a number of iterations and return results."""
    if full_inv is None:
        full_inv = [4, 4, 4, 4]
    game_results = GameResults()
    game_results.raven_end = 0
    game_results.fruit_end = 0
    for _ in range(n_runs):
        game_state = play_with_strat(strat, spaces, full_inv)
        if game_state.raven_track.spaces == 0:
            game_results.raven_end += 1
        else:
            game_results.fruit_end += 1
    return game_results


def run_batches(
    n_runs: int, n_times: int, spaces: int = 5, full_inv: Optional[List[int]] = None
) -> MultIterGame:
    """Run multiple iterations of game with different strategies & return results."""
    if full_inv is None:
        full_inv = [4, 4, 4, 4]
    mult_iter_game = MultIterGame()
    mult_iter_game.smallest_results.clear()
    mult_iter_game.largest_results.clear()
    mult_iter_game.random_results.clear()
    for _ in range(n_runs):
        small_run = run_strat_ntimes(
            n_times, "smallest", spaces, copy.deepcopy(full_inv)
        )
        mult_iter_game.smallest_results.append(small_run.fruit_end)
        large_run = run_strat_ntimes(
            n_times, "largest", spaces, copy.deepcopy(full_inv)
        )
        mult_iter_game.largest_results.append(large_run.fruit_end)
        random_run = run_strat_ntimes(
            n_times, "random", spaces, copy.deepcopy(full_inv)
        )
        mult_iter_game.random_results.append(random_run.fruit_end)
    return mult_iter_game
