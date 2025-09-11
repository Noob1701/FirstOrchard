"""Module to handle game solving for the Orchard game."""

import copy
from functools import lru_cache
from typing import List, Tuple

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesims import Strategy, _choose_strat
from first_orchard_solver.tests.test_gamelogic import _set_state


def _win_perc_return_logic(game_state: GameState) -> Tuple[int, int] | None:
    """
    Return the win or loss from a game for the win_perc function.

    Args:
    ----
            game_state (GameState): Holds these relevant attributes in game_state.

            ---fruit_values (tuple[int, int, int , int]): Tuple of fruit types & counts.

            ---raven_track (int): Number of spaces left on the Raven Track

    Returns:
    -------
            Either (1) or (2) Seen below.
            (1) Either a tuple of (0,1) or (1,0). A loss or win instance resectively.
            (2) None for a non-finshed game, in which solver will continue until 1.

    """
    if game_state.raven_track.spaces == 0:
        return (0, 1)
    if all(fruit == 0 for fruit in game_state.fruit_inventory.fruit_values):
        return (1, 0)
    return None


def _decrement_logic(game_state: GameState, strat: Strategy) -> List[GameState]:
    """
    Generate all single-roll outcomes from this state.

    Args:
    ----
            game_state (GameState): Holds the relevant attributes.
            ---fruit_inventory (dict[int, int]): Dict of fruit types and their counts.

            ---raven_track (int): Number of spaces left on the Raven Track.

            strat (Strategy): String representation of the strategy to be used.

    Returns:
    -------
            moves (list): A list of next states as (fruit1, fruit2, fruit3,
            fruit4, spaces).

    """
    game_states = []

    # Sides 1–4: fruit colors
    for i in game_state.fruit_inventory.fruit_inventory.keys():
        if game_state.fruit_inventory.fruit_inventory[i] > 0:
            new_state = copy.deepcopy(game_state)
            new_state.fruit_inventory.decrement_fruit(i)
            game_states.append(new_state)

    # Side 5: raven
    if game_state.raven_track.spaces > 0:
        new_state = copy.deepcopy(game_state)
        new_state.raven_track.decrement_raven()
        game_states.append(new_state)

    # Side 6: wild/strategy
    if any(game_state.fruit_inventory.fruit_values):
        new_state = copy.deepcopy(game_state)
        _, strat_func_copy = _choose_strat(new_state, strat)
        strat_func_copy()
        game_states.append(new_state)

    return game_states


@lru_cache(maxsize=None)
def win_perc(
    fruit_count: Tuple[int, int, int, int], raven_track: int, strat: Strategy
) -> Tuple[float, float]:
    """
    Calculate the win and loss probabilities for selected strategies.

    Especially choosing the fruit with the most remaining.

    Args:
    ----
        fruit_count (Tuple[int, int, int, int]): counts of the various fruits
        raven_track (int): Number of spaces left on the raven track
        strat (str): The strategy to use for fruit selection. Defaults to "largest".

    Returns:
    -------
        tuple[float, float]: A tuple containing win probability and loss probability.

    """
    game_state = GameState()
    fruit_dict = {i + 3: fruit_count[i] for i in range(len(fruit_count))}
    _set_state(game_state, fruit_dict, raven_track)
    end_game_check = _win_perc_return_logic(game_state)

    if end_game_check is not None:  # game is over
        return end_game_check
    moves = _decrement_logic(game_state, strat)
    win = 0.0
    loss = 0.0
    for move in moves:
        win_instance, loss_instance = win_perc(
            move.fruit_inventory.fruit_values, move.raven_track.spaces, strat
        )
        win += win_instance
        loss += loss_instance

    return round(win / len(moves), 3), round(loss / len(moves), 3)


def win_perc_comp(
    game_state_1: GameState,
    game_state_2: GameState,
    strat_1: Strategy = "most",
    strat_2: Strategy = "most",
) -> Tuple[float, float, float]:
    """
    Calculate the difference.

    Args:
    ----
        game_state_1 (GameState): Game status of the chosen scenario

        game_state_2 (GameState): Game status of the chosen comparator scenario

        strat_1 (Strategy): Strategy for the first game state. Defaults to "most".

        strat_2 (Strategy): Strategy for the second game state. Defaults to "most".

    Returns:
    -------
        tuple[float, float, float]: A tuple of the difference in win probabilities,
        the win probabilities of each choice assuming future perfect play.

    """
    win_perc_1 = win_perc(
        game_state_1.fruit_inventory.fruit_values,
        game_state_1.raven_track.spaces,
        strat_1,
    )
    win_perc_2 = win_perc(
        game_state_2.fruit_inventory.fruit_values,
        game_state_2.raven_track.spaces,
        strat_2,
    )
    worse_win_perc, best_win_perc = (
        min(win_perc_1[0], win_perc_2[0]) * 100,
        max(win_perc_1[0], win_perc_2[0]) * 100,
    )
    diff = best_win_perc - worse_win_perc
    return diff, worse_win_perc, best_win_perc
