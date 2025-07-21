import pytest

from first_orchard_solver.gameplay.gamesolver import win_perc


@pytest.mark.parametrize(
    ("full_inv", "spaces", "strat", "expected"),
    [
        ((4, 4, 4, 4), 5, "small", 0.553),
        ((0, 0, 1, 0), 1, "small", 0.667),
        ((0, 0, 0, 2), 2, "small", 0.741),
        ((4, 4, 4, 4), 5, "large", 0.632),
        ((0, 0, 1, 0), 1, "large", 0.667),
        ((0, 0, 0, 2), 2, "large", 0.741),
        ((4, 4, 4, 4), 5, "random", 0.596),
        ((0, 0, 1, 0), 1, "random", 0.667),
        ((0, 0, 0, 2), 2, "random", 0.741),
    ],
)
def test_win_perc(
    full_inv: tuple[int, int, int, int], spaces: int, strat: str, expected: float
) -> None:
    prob = win_perc(full_inv, spaces, strat)
    win_prob = prob[0]
    loss_prob = prob[1]
    assert loss_prob + win_prob == pytest.approx(1, abs=0.02)
    "The win probability should be approximately 0.553."
    assert win_prob == pytest.approx(expected, abs=0.05)
