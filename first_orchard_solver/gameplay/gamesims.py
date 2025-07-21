from typing import List

from first_orchard_solver.gameplay.gamelogic import GameState


class GameResults:
    raven_end = 0
    fruit_end = 0


class MultIterGame:
    smallest_results: List[int] = []
    largest_results: List[int] = []
    random_results: List[int] = []


def play_with_strat(strat: str) -> GameState:
    game_state = GameState()
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


def run_strat_ntimes(n_runs: int, strat: str) -> GameResults:
    game_results = GameResults()
    game_results.raven_end = 0
    game_results.fruit_end = 0
    for _ in range(n_runs):
        game_state = play_with_strat(strat)
        if game_state.raven_track.spaces == 0:
            game_results.raven_end += 1
        else:
            game_results.fruit_end += 1
    return game_results


def run_batches(n_runs: int, n_times: int) -> MultIterGame:
    mult_iter_game = MultIterGame()
    mult_iter_game.smallest_results.clear()
    mult_iter_game.largest_results.clear()
    mult_iter_game.random_results.clear()
    for _ in range(n_runs):
        small_run = run_strat_ntimes(n_times, "smallest")
        mult_iter_game.smallest_results.append(small_run.fruit_end)
        large_run = run_strat_ntimes(n_times, "largest")
        mult_iter_game.largest_results.append(large_run.fruit_end)
        random_run = run_strat_ntimes(n_times, "random")
        mult_iter_game.random_results.append(random_run.fruit_end)
    return mult_iter_game
