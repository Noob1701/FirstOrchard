"""

Perform event handling for the playable version of the game.

eventhandler.py should not reference background or screen at all. If something new
needs to be drawn this should be handled in renderer.py
"""

from typing import Tuple

import pygame

from first_orchard_solver.gameplay import rend_dynamic as dyna
from first_orchard_solver.gameplay import rend_static as static
from first_orchard_solver.gameplay.context import GameContext, unpack_game_context


def die_results_color(game_context: GameContext) -> Tuple[int, int, int] | None:
    """Handle events when die roll is fruit."""
    assets, _, _, game_state = unpack_game_context(game_context)
    color_map = {
        3: assets.COLORS.BLUE,
        4: assets.COLORS.RED,
        5: assets.COLORS.GREEN,
        6: assets.COLORS.YELLOW,
    }
    color = color_map.get(game_state.orchard_die.die_result)
    if color:
        game_state.fruit_inventory.decrement_fruit(game_state.orchard_die.die_result)
        return color
    return None


def die_results_raven(game_context: GameContext) -> None:
    """Handle events when die roll is raven."""
    assets, _, _, game_state = unpack_game_context(game_context)
    game_state.raven_track.decrement_raven()
    game_state.replace_text = assets.TEXT.RAVEN_DIE_TEXT


def die_results_wild(game_context: GameContext) -> None:
    """Handle events when die roll is wild."""
    assets, _, _, game_state = unpack_game_context(game_context)
    game_state.replace_text = assets.TEXT.CHOOSE_FRUIT_TEXT
    game_state.die_click_enabled = False
    game_state.pending_fruit_click = True


def choose_fruit(game_context: GameContext, event: pygame.event.Event) -> int | None:
    """Handle events relating to choosing the fruit when die roll is wild."""
    assets, _, _, game_state = unpack_game_context(game_context)
    for idx, rect in enumerate(assets.RECTANGLES.CIRCLE_RECT_TUPLE, start=3):
        if rect.collidepoint(event.pos):
            game_state.fruit_inventory.decrement_fruit(idx)
            game_state.die_click_enabled = True
            game_state.fruit_click_enabled = False
            return idx
    return None


def end_of_game(game_context: GameContext) -> None:
    """Handle events at end of game."""
    _, _, _, game_state = unpack_game_context(game_context)
    if not game_state.is_game_over():
        return
    if sum(game_state.fruit_inventory.fruit_values) == 0:
        static.draw_end_screen(game_context, True)
    elif game_state.raven_track.spaces == 0:
        static.draw_end_screen(game_context, False)


def draw_all_screen(
    game_context: GameContext, color: Tuple[int, int, int] | None, idx: int | None
) -> None:
    """Draw all necessary game elements on the screen."""
    _, _, _, game_state = unpack_game_context(game_context)
    dyna.draw_fruit_circle_texts(game_context)
    dyna.draw_die(game_context)
    dyna.draw_new_die_face(game_context, color)
    dyna.draw_raven_track(game_context)
    if game_state.replace_text:
        dyna.draw_die_replace_text(game_context, game_state.replace_text)
    dyna.draw_odds_text(game_context)
    if game_state.stats_flag:
        odds_result = dyna.get_compare_odds(game_context, idx)
        dyna.draw_coaching_text(game_context, odds_result)
    end_of_game(game_context)
    pygame.display.flip()
