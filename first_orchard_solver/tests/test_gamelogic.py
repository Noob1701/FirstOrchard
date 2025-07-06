import pytest

from first_orchard_solver.gameplay.gamelogic import (
    FruitInventory,
    GameState,
    OrchardDie,
    RavenTrack,
)
from first_orchard_solver.gameplay.gamestrategy import play_with_strat

#test_smallest_strat

@pytest.mark.parametrize("full_inv, expected", [
    ({3: 1, 4: 2, 5: 3, 6: 4}, {3: 0, 4: 2, 5: 3, 6: 4}),
    ({3: 0, 4: 1, 5: 2, 6: 3}, {3: 0, 4: 0, 5: 2, 6: 3}),
    ({3: 2, 4: 4, 5: 2, 6: 0}, {3: 1, 4: 4, 5: 2, 6: 0}),
])
def test_smallest_strat(full_inv:dict, expected:dict) -> None:
    orchard_die = OrchardDie()
    inventory = FruitInventory(orchard_die=orchard_die)
    inventory.full_inv = full_inv
    inventory.smallest_strat()

    assert inventory.full_inv == expected


#test_largest_strat
@pytest.mark.parametrize("full_inv, expected", [
    ({3: 1, 4: 2, 5: 3, 6: 4}, {3: 1, 4: 2, 5: 3, 6: 3}),
    ({3: 0, 4: 1, 5: 2, 6: 3}, {3: 0, 4: 1, 5: 2, 6: 2}),
    ({3: 1, 4: 0, 5: 1, 6: 0}, {3: 0, 4: 0, 5: 1, 6: 0}),
])
def test_largest_strat(full_inv:dict, expected:dict) -> None:
    orchard_die = OrchardDie()
    inventory = FruitInventory(orchard_die=orchard_die)
    inventory.full_inv = full_inv
    inventory.largest_strat()

    assert inventory.full_inv == expected
#test_random_strat
@pytest.mark.parametrize("full_inv, expected", [
    ({3: 1, 4: 2, 5: 3, 6: 4}, 9),
    ({3: 0, 4: 1, 5: 2, 6: 3}, 5),
    ({3: 2, 4: 4, 5: 2, 6: 0}, 7),
])
def test_random_strat(full_inv:dict, expected:int) -> None:
    orchard_die = OrchardDie()
    inventory = FruitInventory(orchard_die=orchard_die)
    inventory.full_inv = full_inv
    inventory.random_strat()

    assert sum(inventory.full_inv.values()) == expected

#test_check_zeros
@pytest.mark.parametrize("full_inv, expected", [
    ({3: 1, 4: 2, 5: 3, 6: 4}, True),
    ({3: 0, 4: 0, 5: 0, 6: 0}, False),
    ({3: 2, 4: 0, 5: 1, 6: 0}, True),
])
def test_check_not_zero(full_inv:dict, expected:bool) -> None:
    orchard_die = OrchardDie()
    inventory = FruitInventory(orchard_die=orchard_die)
    inventory.full_inv = full_inv

    assert inventory.check_not_zero() == expected
#test_is_game_over
@pytest.mark.parametrize("spaces, full_inv, expected", [
    (0, {3: 1, 4: 2, 5: 3, 6: 4}, True),
    (1, {3: 0, 4: 0, 5: 0, 6: 0}, True),
    (5, {3: 2, 4: 0, 5: 1, 6: 0}, False),
])
def test_is_game_over(spaces:int, full_inv:dict, expected:bool) -> None:
    orchard_die = OrchardDie()
    inventory = FruitInventory(orchard_die=orchard_die)
    inventory.full_inv = full_inv
    raven_track = RavenTrack()
    raven_track.spaces = spaces
    game_state = GameState()
    game_state.orchard_die = orchard_die
    game_state.fruit_inventory = inventory
    game_state.raven_track = raven_track

    assert game_state.is_game_over() == expected

#test_play_with_strat
@pytest.mark.parametrize("strat", ['smallest', 'largest', 'random'])
def test_play_with_strat(strat:str) -> None:
    game_state = play_with_strat(strat)
    assert game_state.is_game_over()
    assert (
        game_state.raven_track.spaces == 0
        or not game_state.fruit_inventory.check_not_zero()
    )