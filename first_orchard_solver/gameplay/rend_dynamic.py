"""Render dynamic updates to screen."""

import copy
from typing import Tuple

import pygame

from first_orchard_solver.gameplay.context import GameContext, unpack_game_context
from first_orchard_solver.gameplay.gamelogic import GameState
from first_orchard_solver.gameplay.gamesolver import win_perc, win_perc_comp


def draw_fruit_circle_texts(game_context: GameContext) -> None:
    """Draws the text inside the fruit circles."""
    assets, _, screen, game_state = unpack_game_context(game_context)
    fruit_ids = [3, 4, 5, 6]  # Exception to hard coding, fruit IDs are fixed
    circle_positions = [
        assets.POSITIONS.BLUE_CIRCLE_TEXT_POS,
        assets.POSITIONS.RED_CIRCLE_TEXT_POS,
        assets.POSITIONS.GREEN_CIRCLE_TEXT_POS,
        assets.POSITIONS.YELLOW_CIRCLE_TEXT_POS,
    ]
    for fruit_id, position in zip(fruit_ids, circle_positions):
        text_surface = assets.FRUIT_CIRCLE_FONT.render(
            str(game_state.fruit_inventory.fruit_inventory[fruit_id]),
            assets.ANTIALIASING.CIRCLE_SURF_ANTIALIAS,
            assets.COLORS.BLACK,
        )
        screen.blit(text_surface, position)


def draw_odds_text(game_context: GameContext) -> None:
    """Draws the initial odds text on the background."""
    assets, _, screen, game_state = unpack_game_context(game_context)
    game_odds = win_perc(
        game_state.fruit_inventory.fruit_values,
        game_state.raven_track.spaces,
        assets.OPTIONS.WIN_PERC_OPTION[0],
    )  # 0 is chance of winning (assuming future perfect play)

    odds_text = assets.TEXT.ODDS_TEXT + f"{game_odds[0] * 100:.2f}%"
    odds_surface = assets.ODDS_FONT.render(
        odds_text, assets.ANTIALIASING.ODDS_TEXT_ANTIALIAS, assets.COLORS.BLACK
    )
    screen.blit(odds_surface, assets.POSITIONS.ODDS_TEXT_POS)


def draw_die(game_context: GameContext) -> None:
    """Draws starting background image of the die (not the die face) on background."""
    assets, _, screen, _ = unpack_game_context(game_context)
    pygame.draw.rect(screen, assets.COLORS.WHITE, assets.RECTANGLES.ROLL_BUTTON_RECT)


def draw_new_die_face(
    game_context: GameContext,
    color: Tuple[int, int, int] | None,
) -> None:
    """
    Draws the die face.

    The arg "color" is a tuple of Red Green Blue values with max of 255.

    When officially called in eventhandler.py, it will use predefined colors from
    context.py
    """
    assets, _, screen, _ = unpack_game_context(game_context)

    if color is not None:
        pygame.draw.circle(
            screen,
            color,
            assets.RECTANGLES.ROLL_BUTTON_RECT.center,
            assets.RECTANGLES.DIE_FACE_RADIUS,
        )
    else:
        pass


def draw_die_replace_text(game_context: GameContext, die_surface_text: str) -> None:
    """
    Will replace the die with text when the raven or wild is rolled.

    When officially called in eventhandler.py the text will come from context.py.

    This will be used when the Raven or Wild is rolled.
    """
    assets, _, screen, _ = unpack_game_context(game_context)
    pygame.draw.rect(screen, assets.COLORS.PURPLE, assets.RECTANGLES.ROLL_BUTTON_RECT)
    die_surface = assets.DIE_REPLACEMENT_FONT.render(
        die_surface_text,
        assets.ANTIALIASING.DIE_REPLACEMENT_ANTIALIAS,
        assets.COLORS.BLACK,
    )
    text_rect = die_surface.get_rect(topleft=assets.POSITIONS.DIE_REPLACEMENT_TEXT_POS)
    screen.blit(die_surface, text_rect)


def _check_if_all_same(game_state: GameState) -> bool:
    """Check to see whether all the values of fruit inventory are the same integer."""
    fruit_count = list(game_state.fruit_inventory.fruit_values)
    non_zero_count = [i for i in fruit_count if i > 0]
    if len(set(non_zero_count)) == 1:
        return True
    else:
        return False


def get_compare_odds(
    game_context: GameContext, choice: int | None
) -> Tuple[float, float, float, bool] | None:
    """
    Compare player & optimal choice from game; also gets odds & difference.

    Arg: 'choice' corresponds the players choice of fruit
    ---

    Returns
    -------
            Tuple [int, int, int, bool]: Tuple[0] is the difference in probabilities
            bewteen optimal and player choice, Tuple[1] is the probability from player
            choice, Tuple[2] is the probability of the optimal strategy, and bool is
            whether or not all fruits have the same number remaining.

    Note: test_strategies in test_game_solver.py formally assets that the largest
    strategy is always equal to or better than other strategies. And is assumed in
    this function.

    Another Note: deepcopy is slow here, but this is acceptable speed for this game.

    """
    if choice is None:
        return None
    _, _, _, game_state = unpack_game_context(game_context)
    game_state_optimal = copy.deepcopy(game_state)
    game_state_optimal.fruit_inventory.increment_fruit(choice)
    same_bool = _check_if_all_same(game_state_optimal)
    game_state_player = copy.deepcopy(game_state_optimal)
    game_state_player.fruit_inventory.decrement_fruit(choice)
    game_state_optimal.fruit_inventory.most_strat()

    diff, player_odds, optimal_odds = win_perc_comp(
        game_state_player, game_state_optimal
    )
    return diff, player_odds, optimal_odds, same_bool


def _draw_stats_text(
    game_context: GameContext, odds_results: Tuple[float, float, float, bool]
) -> None:
    """
    Draws compared odds between player choice and optimal choice when relevant.

    See function draw_coaching_text for arg info.
    """
    assets, _, screen, _ = unpack_game_context(game_context)
    diff, player_odds, optimal_odds, _ = odds_results
    optimal_odds = round(optimal_odds, 2)
    diff = round(diff, 2)
    stats_text = [
        assets.TEXT.BETTER_OPTION_TEXT,
        f"{assets.TEXT.CURRENT_ODDS_TEXT} {player_odds}",
        f"{assets.TEXT.BETTER_ODDS_TEXT} {optimal_odds}",
        f"{assets.TEXT.DIFFERENCE_ODDS_TEXT} {diff}",
    ]
    for offset, message in enumerate(stats_text):
        new_y = (
            int(assets.POSITIONS.COACHING_POS[1])
            + (offset + 1) * assets.POSITIONS.STATS_TEXT_ALTER
        )
        new_pos: Tuple[int, int] = (assets.POSITIONS.COACHING_POS[0], new_y)
        stats_surface = assets.COACHING_FONT.render(
            message, assets.ANTIALIASING.COACHING_ANTIALIAS, assets.COLORS.BLACK
        )
        stats_text_rect = stats_surface.get_rect(topleft=new_pos)
        screen.blit(stats_surface, stats_text_rect)


def draw_coaching_text(
    game_context: GameContext, odds_results: Tuple[float, float, float, bool] | None
) -> None:
    """

    Draws text to explain how player choice compares to optimal choice.

    Arg:
    ---
            odds_result (Tuple[float, float, float]): Tuple[0] is the difference in
            probabilities bewteen optimal and player choice, Tuple[1] is the
            probability of winning resulting from player choice, Tuple[2] is the
            probability of winning resulting from the optimal strategy, and bool is
            whether all the fruit types had equal number remaining or not prior to
            player choice -> Comes from get_compare_odds.

    """
    if odds_results is None:
        return None
    assets, _, screen, _ = unpack_game_context(game_context)
    diff, _, _, same_bool = odds_results
    if diff == 0 and same_bool:
        coaching_text = assets.TEXT.ALL_GOOD_OPTIONS_TEXT
    elif diff == 0 and not same_bool:
        coaching_text = assets.TEXT.BEST_CHOICE_TEXT
    else:
        coaching_text = assets.TEXT.BAD_CHOICE_TEXT
        _draw_stats_text(game_context, odds_results)
    coaching_surface = assets.COACHING_FONT.render(
        coaching_text, assets.ANTIALIASING.COACHING_ANTIALIAS, assets.COLORS.BLACK
    )
    coaching_rect = coaching_surface.get_rect(topleft=assets.POSITIONS.COACHING_POS)
    screen.blit(coaching_surface, coaching_rect)


def draw_wild_instruction(game_context: GameContext) -> None:
    """Draws instructions to user when the wild is rolled."""
    assets, _, screen, _ = unpack_game_context(game_context)
    click_fruit_text = assets.TEXT.CHOOSE_FRUIT_TEXT
    choose_fruit_surface = assets.CHOOSE_FRUIT_FONT.render(
        click_fruit_text,
        assets.ANTIALIASING.CHOOSE_FRUIT_ANTIALIAS,
        assets.COLORS.BLACK,
    )
    click_fruit_rect = choose_fruit_surface.get_rect(
        topleft=assets.POSITIONS.CHOOSE_FRUIT_POS
    )
    screen.blit(choose_fruit_surface, click_fruit_rect)


def erase_coaching_text(game_context: GameContext) -> None:  # X
    """Restores background after displaying coaching text."""
    assets, background, screen, _ = unpack_game_context(game_context)
    fill_rect = assets.RECTANGLES.COACHING_RECT
    screen.blit(background, fill_rect, fill_rect)


def _draw_raven_rects(game_context: GameContext, rectangle: pygame.Rect) -> None:
    """Draws the raven rectangles on the background."""
    assets, background, _, _ = unpack_game_context(game_context)
    pygame.draw.rect(background, assets.COLORS.BLACK, rectangle)


def draw_raven_track(game_context: GameContext) -> None:
    """Draws the raven track rectangles based on the current game state."""
    assets, _, _, game_state = unpack_game_context(game_context)
    raven_map = {
        4: assets.RECTANGLES.RECTANGLE_1,
        3: assets.RECTANGLES.RECTANGLE_2,
        2: assets.RECTANGLES.RECTANGLE_3,
        1: assets.RECTANGLES.RECTANGLE_4,
        0: assets.RECTANGLES.RECTANGLE_5,
    }
    raven = raven_map.get(game_state.raven_track.spaces)
    if raven:
        _draw_raven_rects(game_context, raven)
