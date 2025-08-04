"""
Module to handle gameplay for the Orchard game.

Includes functions to play the game with different strategies and manage game state.
"""

import copy
from typing import Tuple, cast

from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesolver import win_perc_comp


def play_orchard() -> None:
    """Will allow user to play the Orchard game interactively."""
    game_state = GameState()
    while not game_state.is_game_over():
        play = input("Roll the die? (y/n): ").strip().lower()
        if play == "y":
            result = game_state.orchard_die.roll()
            print(f"You rolled a {result}.")
            if result == 1:
                game_state.raven_track.decrement_raven()
                print("The raven moves one space closer!")
            elif result == 2:
                if game_state.fruit_inventory.check_not_zero():
                    fruit_choice = int(
                        input(
                            "Your current fruit inventory is "
                            f"{game_state.fruit_inventory.full_inv}. "
                            "Enter the fruit type (3-6): "
                        )
                    )
                    if fruit_choice in game_state.fruit_inventory.full_inv:
                        game_state_comp = copy.deepcopy(game_state)
                        game_state_comp.fruit_inventory.largest_strat()
                        user_state = copy.deepcopy(game_state)
                        user_state.fruit_inventory.decrement_fruit(fruit_choice)
                        full_inv_1 = tuple(user_state.fruit_inventory.full_inv.values())
                        full_inv_2 = tuple(
                            game_state_comp.fruit_inventory.full_inv.values()
                        )
                        full_inv_1 = cast(Tuple[int, int, int, int], full_inv_1)
                        full_inv_2 = cast(Tuple[int, int, int, int], full_inv_2)
                        perc_comp = win_perc_comp(
                            full_inv_1,
                            game_state.raven_track.spaces,
                            full_inv_2,
                            game_state_comp.raven_track.spaces,
                            "large",
                            "large",
                        )
                        game_state.fruit_inventory.decrement_fruit(fruit_choice)
                        print(
                            f"You collected fruit type {fruit_choice}. This was "
                            f"{perc_comp[0]}% worse than the best strategy."
                            " Your current odds of winning assuming the best"
                            f" strategy is chosen is {perc_comp[1]}%"
                        )

                    else:
                        print("Invalid fruit type.")
            else:
                game_state.fruit_inventory.decrement_fruit(result)
                print(f"You collected fruit type {result}.")
        else:
            print("Thank you for playing!")
            break


play_orchard()
