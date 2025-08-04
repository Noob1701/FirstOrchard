"""
Module contains the core game logic for the Orchard game.

It includes classes for managing game state, the raven track, the fruit inventory.

"""

import random


# In the Orchard game, the player loses when the raven reaches the end of the track
class RavenTrack:
    """A class to track the number of spaces left for the raven to move."""

    def __init__(self, spaces: int = 5) -> None:
        """
        Initialize the RavenTrack with a given number of spaces.

        Args:
        ----
            spaces (int): The number of spaces the raven can move. Defaults to 5.

        """
        self.spaces = spaces
        return None

    def decrement_raven(self) -> None:
        """Decrement the number of spaces left for the raven to move."""
        self.spaces -= 1
        return None


# In the base game a die is rolled to determine the action to take.
# The die has 6 sides, with 2 sides being speicial; for this code those sides are 1 & 2
# #1 is the raven, which decrements the raven track
# #2 allows the player to select a fruit of their choice from the inventory
# #3, #4, #5, #6 are fruit types, which decrement 1 from that fruit's inventory
# The player(s) win if all the fruits are collected (i.e. the inventory is empty)
class OrchardDie:
    """A class to represent a die used in the Orchard game."""

    def __init__(self, sides: int = 6, result: int = 0) -> None:
        """Initialize tOrchardDie with a given number of sides & placeholder result."""
        self.sides = sides
        self.result = result
        return None

    def roll(self) -> int:
        """Roll the die and return the result."""
        self.result = random.randint(1, self.sides)
        return self.result


class FruitInventory:
    """A class to manage the inventory of fruits in the Orchard game."""

    def __init__(self, orchard_die: OrchardDie) -> None:
        """
        Initialize class to manage the inventory of fruits in the Orchard game.

        And to implement strategies for fruit selection.

        Args:
        ----
            orchard_die (OrchardDie): An instance of OrchardDie to use for rolling.

        """
        self.fruit_types = orchard_die.sides - 2
        self.fruit_amt = 4
        self.full_inv: dict[int, int] = {}
        self.fruit_count = tuple(self.full_inv.values())
        for fruit in range(self.fruit_types):
            self.full_inv[fruit + 3] = 4
        return None

    def decrement_fruit(self, result: int) -> None:
        """Decrement a specific fruit by one in the inventory based die roll result."""
        if result in self.full_inv.keys() and self.full_inv[result] > 0:
            self.full_inv[result] -= 1

    def smallest_strat(self) -> None:
        """Implement a strategy of decrementing the fruit with the least amount."""
        non_zero_fruits: dict[int, int] = {
            k: v for k, v in self.full_inv.items() if v > 0
        }
        smallest_fruit = min(non_zero_fruits, key=lambda k: non_zero_fruits[k])
        self.full_inv[smallest_fruit] -= 1

    def largest_strat(self) -> None:
        """Implement a strategy of decrementing the fruit with the most amount."""
        largest_fruit = max(self.full_inv, key=lambda k: self.full_inv[k])
        self.full_inv[largest_fruit] -= 1

    def random_strat(self) -> None:
        """Implement a strategy of decrementing a random fruit from the inventory."""
        non_zero_fruits: dict[int, int] = {
            k: v for k, v in self.full_inv.items() if v > 0
        }
        random_fruit: int = random.choice(list(non_zero_fruits.keys()))
        self.full_inv[random_fruit] -= 1

    def check_not_zero(self) -> bool:
        """Check if there are any fruits left in the inventory."""
        return any(value != 0 for value in self.full_inv.values())


class GameState:
    """Initializing a class to represent the state of the Orchard game."""

    def __init__(self) -> None:
        """Initialize game state with an OrchardDie, RavenTrack, and FruitInventory."""
        self.orchard_die = OrchardDie()
        self.raven_track = RavenTrack()
        self.fruit_inventory = FruitInventory(self.orchard_die)

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.raven_track.spaces <= 0 or not self.fruit_inventory.check_not_zero()
