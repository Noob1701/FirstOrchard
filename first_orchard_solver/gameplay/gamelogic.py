"""
Module contains the core game logic for the Orchard game and strategies for bot play.

It includes classes for managing game state, the raven track, the fruit inventory.

"""

import random
from typing import Tuple


# In the Orchard game, the player loses when the raven reaches the end of the track
class RavenTrack:
    """
    A class to track the number of spaces left for the raven to move.

    Args:
    ----
            spaces (int): The number of spaces the raven can move. Defaults to 5. When
            this is 0, the game is over and player loses.

    """

    def __init__(self, spaces: int = 5) -> None:
        """Initialize the RavenTrack with a given number of spaces."""
        self.spaces = spaces
        return None

    def decrement_raven(self) -> None:
        """Decrement the number of spaces left for the raven to move."""
        self.spaces -= 1
        return None


class OrchardDie:
    """A class to represent a die used in the Orchard game."""

    def __init__(self, sides: int = 6, die_result: int = 0) -> None:
        """
        Initialize OrchardDie with a given number of sides & placeholder result.

        Args:
        ----
                sides (int): represents the number of sides on the die can be altered
                for mathematical purposes. However, currently most functions require
                the default of 6.

                die_result (int): represents the result of the rolled die

        """
        self.sides = sides
        self.die_result = die_result
        return None

    def roll(self) -> int:
        """Roll the die and return the result."""
        self.die_result = random.randint(1, self.sides)
        return self.die_result


class FruitInventory:
    """A class to manage the inventory of fruits in the Orchard game."""

    def __init__(self, orchard_die: OrchardDie) -> None:
        """
        Initialize class to manage the inventory of fruits in the Orchard game.

        And to implement strategies for fruit selection.

        Args:
        ----
            orchard_die (OrchardDie): An instance of OrchardDie to use for rolling.
            Minor customization allowed, however, most functions do not support that.
            Considering removing customizability to stick solely to the base game.

        """
        self.fruit_types: int = orchard_die.sides - 2
        self.fruit_amt: int = 4
        self.fruit_inventory: dict[int, int] = {}
        for fruit in range(self.fruit_types):
            self.fruit_inventory[fruit + 3] = 4
        return None

    @property
    def fruit_values(self) -> tuple[int, ...]:
        """Converts the fruit_inventory dictionary values into a tuple."""
        return tuple(self.fruit_inventory.values())

    def decrement_fruit(self, die_result: int) -> None:
        """
        Decrement a specific fruit by one in the inventory based die roll result.

        Args:
        ----
                die_result (int): result of OrchardDie roll

        """
        if (
            die_result in self.fruit_inventory.keys()
            and self.fruit_inventory[die_result] > 0
        ):
            self.fruit_inventory[die_result] -= 1

    def increment_fruit(self, die_result: int) -> None:
        """Increment specific fruit by one to restore previous game state in drawing."""
        if die_result in self.fruit_inventory.keys():
            self.fruit_inventory[die_result] += 1

    def fewest_strat(self) -> None:
        """Implement a strategy of decrementing the fruit with the least amount."""
        non_zero_fruits: dict[int, int] = {
            k: v for k, v in self.fruit_inventory.items() if v > 0
        }
        fewest_fruit = min(non_zero_fruits, key=lambda k: non_zero_fruits[k])
        self.fruit_inventory[fewest_fruit] -= 1

    def most_strat(self) -> None:
        """Implement a strategy of decrementing the fruit with the most amount."""
        largest_fruit = max(self.fruit_inventory, key=lambda k: self.fruit_inventory[k])
        self.fruit_inventory[largest_fruit] -= 1

    def random_strat(self) -> None:
        """
        Implement a strategy of decrementing a random fruit from the inventory.

        Note: This logic is used in win_perc that is otherwise deterministic. This is a
        known limitation of the current code and should be kept in mind. A future
        refactor might make this deterministic as well. But this is honestly probably
        not something that is strictly necessary.
        """
        non_zero_fruits: dict[int, int] = {
            k: v for k, v in self.fruit_inventory.items() if v > 0
        }
        random_fruit: int = random.choice(list(non_zero_fruits.keys()))
        self.fruit_inventory[random_fruit] -= 1

    def check_not_zero(self) -> bool:
        """Return True if there are any fruits remaining."""
        return any(value != 0 for value in self.fruit_inventory.values())


class GameState:
    """Initializing a class to represent the state of the Orchard game."""

    def __init__(self) -> None:
        """Initialize game state with an OrchardDie, RavenTrack, and FruitInventory."""
        self.reset()

    def reset(self) -> None:
        """Reset the game state to initial conditions."""
        self.orchard_die: OrchardDie = OrchardDie()
        self.raven_track: RavenTrack = RavenTrack()
        self.fruit_inventory: FruitInventory = FruitInventory(self.orchard_die)
        self.die_click_enabled: bool = True
        self.fruit_click_enabled: bool = False
        self.replace_text: str | None = None
        self.pending_fruit_click: bool = False
        self.stats_flag: bool = False

    @property
    def game_status(self) -> Tuple[int, ...]:
        """Returns full passable tuple of fruit_inventory and raven_track."""
        status_list = list(self.fruit_inventory.fruit_inventory.values())
        status_list.append(self.raven_track.spaces)
        return tuple(status_list)

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.raven_track.spaces <= 0 or not self.fruit_inventory.check_not_zero()
