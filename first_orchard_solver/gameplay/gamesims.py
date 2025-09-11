"""Module to handle game simulations for the Orchard game."""

import copy
from typing import Callable, List, Literal, Mapping, Tuple

from first_orchard_solver.gameplay.gamelogic import GameState

Strategy = Literal["fewest", "most", "random"]


class GameResults:
    """Stores the results of a game run."""

    def __init__(self) -> None:
        """Initialize game results to count raven endings (loss) & fruit ends (wins)."""
        self.raven_end = 0
        self.fruit_end = 0


class MultIterGame:
    """Stores results of multiple game results with particular strategies chosen."""

    def __init__(self) -> None:
        """Initialize the game results with empty lists for different strategies."""
        self.fewest_strat_runs: List[int] = []
        self.most_strat_runs: List[int] = []
        self.random_strat_runs: List[int] = []


def _choose_strat(
    game_state: GameState, strat: Strategy
) -> Tuple[GameState, Callable[[], None]]:
    """Return the strategy from fruit_inventory for simulations and comparisons."""
    strategies: Mapping[Strategy, Callable[[], None]] = {
        "fewest": game_state.fruit_inventory.fewest_strat,
        "most": game_state.fruit_inventory.most_strat,
        "random": game_state.fruit_inventory.random_strat,
    }
    return game_state, strategies[strat]


def _play_with_strat(game_state: GameState, strat: Strategy) -> GameState:
    """
    Play the Orchard game with a specific strategy and return final game state.

    Args:
    ----
            strat (Strategy): Indicates which strategy the bot should use. Options
            are fewest, most, and random. Fewest takes from the fruit type with the
            least remaining, most from the most remaining, and random picks a random
            fruit.

            game_state (GameState): Contains the below attributes
            used in this function.

            --raven_track (int): Number of spaces left on the Raven Track

            --fruit_inventory (dict[int, int]): dict of fruit types and their counts.
            Intialiazes to fruit inventory of 4 of each fruit to mimic the start of the
            game if no inventory was given.

    Returns:
    -------
            game_state (GameState): It's game_state includes fruit counts,
            raven position, and whether game is over.

    """
    game_state, strat_func = _choose_strat(game_state, strat)
    while not game_state.is_game_over():
        result = game_state.orchard_die.roll()
        if result == 2:
            strat_func()
        elif result == 1:
            game_state.raven_track.decrement_raven()
        else:
            game_state.fruit_inventory.decrement_fruit(result)

    return game_state


def _run_strat_ntimes(
    game_state: GameState, n_runs: int, strat: Strategy
) -> GameResults:
    """
    Run a specific strategy for a number of iterations and return results.

    Args:
    ----
            game_state (GameState): Has the below properties used in this function.

            ---raven_track (int): Number of spaces left on the Raven Track

            ---fruit_inventory (dict[int, int]: list of fruit types and their counts.
            Intialiazes to fruit inventory of 4 of each fruit to mimic the start of the
            game if no inventory was given.

            n_runs (int): Number of times to play the game

            strat (str): Indicates which strategy the bot should use. Options are
            fewest, most, and random. Fewest takes from the fruit type with the
            least remaining, most from the most, and random chooses a random fruit.

    Returns:
    -------
            game_results(GameResults): number of fruit endings (wins) vs
            raven endings (losses).

    """
    game_results = GameResults()
    game_results.raven_end = 0
    game_results.fruit_end = 0
    for _ in range(n_runs):
        state_copy = copy.deepcopy(game_state)
        _play_with_strat(state_copy, strat)
        if state_copy.raven_track.spaces == 0:
            game_results.raven_end += 1
        else:
            game_results.fruit_end += 1
    return game_results


def run_batches(
    game_state: GameState,
    n_runs: int,
    n_times: int,
    strat: List[Strategy] | None = ["most"],
) -> MultIterGame:
    """
    Run multiple iterations of game with different strategies & return results.

    Args:
    ----
            game_state (GameState): Contains the following properties used in this
            function

            ---raven_track (int): Number of spaces left on the Raven Track

            ---fruit_inventory (dict[int, int]): dict of fruit types and their counts.
            Intialiazes to fruit inventory of 4 of each fruit to mimic the start of the
            game if no inventory was given.

            n_runs (int): Number of times to play the game

            n_times (int): Number of times to run simulation of n_run number of games

            strat (Strategy | None): If none will run all strategies, will also take a
            list of strategies to run. Will default to largest strategy.

    Returns:
    -------
            mult_iter_game (MultIterGame): Storage for the simulation results


    """
    mult_iter_game = MultIterGame()
    mult_iter_game.fewest_strat_runs.clear()
    mult_iter_game.most_strat_runs.clear()
    mult_iter_game.random_strat_runs.clear()
    if strat is None:
        strat = ["most", "fewest", "random"]
    for _ in range(n_times):
        for s in strat:
            if s == "fewest":
                least_run = _run_strat_ntimes(game_state, n_runs, "fewest")
                mult_iter_game.fewest_strat_runs.append(least_run.fruit_end)
            elif s == "most":
                most_run = _run_strat_ntimes(game_state, n_runs, "most")
                mult_iter_game.most_strat_runs.append(most_run.fruit_end)
            elif s == "random":
                random_run = _run_strat_ntimes(game_state, n_runs, "random")
                mult_iter_game.random_strat_runs.append(random_run.fruit_end)
    return mult_iter_game
