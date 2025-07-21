import random
from functools import lru_cache
from typing import Tuple


@lru_cache(maxsize=None)
def win_perc(
    full_inv: Tuple[int, int, int, int], spaces: int, strat: str = "large"
) -> Tuple[float, float]:
    """
    Calculate the win and loss probabilities for the smallest strategy.

    Args:
        full_inv (tuple[int, int, int, int]): The full inventory of fruits.
        spaces (int): The number of spaces left on the raven track.

    Returns:
        tuple[float, float]: A tuple containing win probability and loss probability.
    """
    if spaces == 0:
        return (0, 1)
    if all(fruit == 0 for fruit in full_inv):
        return (1, 0)

    win = 0.0
    loss = 0.0
    moves = []

    if spaces > 0 or any(full_inv) != 0:
        if full_inv[0] != 0:
            new_state = (full_inv[0] - 1, full_inv[1], full_inv[2], full_inv[3], spaces)
            moves.append(new_state)
        if full_inv[1] != 0:
            new_state = (full_inv[0], full_inv[1] - 1, full_inv[2], full_inv[3], spaces)
            moves.append(new_state)
        if full_inv[2] != 0:
            new_state = (full_inv[0], full_inv[1], full_inv[2] - 1, full_inv[3], spaces)
            moves.append(new_state)
        if full_inv[3] != 0:
            new_state = (full_inv[0], full_inv[1], full_inv[2], full_inv[3] - 1, spaces)
            moves.append(new_state)
        if spaces > 0:
            new_state = (full_inv[0], full_inv[1], full_inv[2], full_inv[3], spaces - 1)
            moves.append(new_state)
        if any(full_inv) != 0:
            if strat == "large":
                max_index = full_inv.index(max(full_inv))
                new_state = (
                    full_inv[0] - 1 if max_index == 0 else full_inv[0],
                    full_inv[1] - 1 if max_index == 1 else full_inv[1],
                    full_inv[2] - 1 if max_index == 2 else full_inv[2],
                    full_inv[3] - 1 if max_index == 3 else full_inv[3],
                    spaces,
                )

                moves.append(new_state)

            if strat == "small":
                candidates = [(i, v) for i, v in enumerate(full_inv) if v >= 1]
                min_index, _ = min(candidates, key=lambda x: x[1])
                new_state = (
                    full_inv[0] - 1 if min_index == 0 else full_inv[0],
                    full_inv[1] - 1 if min_index == 1 else full_inv[1],
                    full_inv[2] - 1 if min_index == 2 else full_inv[2],
                    full_inv[3] - 1 if min_index == 3 else full_inv[3],
                    spaces,
                )

                moves.append(new_state)
            if strat == "random":
                index = random.choice([i for i, v in enumerate(full_inv) if v > 0])
                new_state = (
                    full_inv[0] - 1 if index == 0 else full_inv[0],
                    full_inv[1] - 1 if index == 1 else full_inv[1],
                    full_inv[2] - 1 if index == 2 else full_inv[2],
                    full_inv[3] - 1 if index == 3 else full_inv[3],
                    spaces,
                )
                moves.append(new_state)
    for next_state in moves:
        win_instance, loss_instance = win_perc(next_state[:4], next_state[4], strat)
        win += win_instance
        loss += loss_instance

    return round(win / len(moves), 2), round(loss / len(moves), 2)
