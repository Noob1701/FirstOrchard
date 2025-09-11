"""
Module for rendering the background elements of the First Orchard Solver.

Should contain only draw, blit, render, and game_state initialization calls. No hard
coding of values, all values should be imported from GameContext. Assets and GameState
are initialized in the GameContext class. Outside of GameContext, Assets and GameState
should not be directly instantiated.
-> Exception for final screen, this will be flipped in this code.

Though this is repetitive, GameContext is a Class to hold the game context. It has the
following attributes: screen (pygame.Surface): The main game screen,
                      background (pygame.Surface): The background surface,
                      assets (Assets): The game assets,
                      game_state (GameState): The current state of the game.

For more information see context.py for screen, background, and assets. For more info
about game_state see gamelogic.py

Design Note:
There is some repetition in this code when making objects appear on the screen,
especially text. I think it is more readable & easier to maintain/debug to not convert
this repetetive code into functions. Especially as there are many exceptions to the
base drawing template and if base drawing functions were to be used, they would require
multiple arguments making them slightly unwieldy when trying to call them.
"""

import sys

import pygame

from first_orchard_solver.gameplay.context import GameContext, unpack_game_context


def draw_instruction_text(game_context: GameContext) -> None:
    """Draws roll instruction text on the background."""
    assets, background, _, _ = unpack_game_context(game_context)
    instruction_surface = assets.INSTRUCTION_FONT.render(
        assets.TEXT.INSTRUCTION_TEXT,
        assets.ANTIALIASING.INSTRUCTION_SURF_ANTIALIAS,
        assets.COLORS.BLACK,
    )
    background.blit(instruction_surface, assets.POSITIONS.INSTRUCTION_POS)


def draw_fruit_circles(game_context: GameContext) -> None:
    """Draws the fruit circles on the background."""
    assets, background, _, _ = unpack_game_context(game_context)
    pygame.draw.circle(
        background,
        assets.COLORS.BLUE,
        assets.POSITIONS.BLUE_CIRCLE_POS,
        assets.RECTANGLES.CIRCLE_RADIUS,
    )
    pygame.draw.circle(
        background,
        assets.COLORS.RED,
        assets.POSITIONS.RED_CIRCLE_POS,
        assets.RECTANGLES.CIRCLE_RADIUS,
    )
    pygame.draw.circle(
        background,
        assets.COLORS.GREEN,
        assets.POSITIONS.GREEN_CIRCLE_POS,
        assets.RECTANGLES.CIRCLE_RADIUS,
    )
    pygame.draw.circle(
        background,
        assets.COLORS.YELLOW,
        assets.POSITIONS.YELLOW_CIRCLE_POS,
        assets.RECTANGLES.CIRCLE_RADIUS,
    )


def draw_background(game_context: GameContext) -> None:
    """Draw all the necessary game elements on the screen."""
    draw_instruction_text(game_context)
    draw_fruit_circles(game_context)


def draw_restart_text(game_context: GameContext) -> None:
    """Draws text where user will indicate whether they want to start a new game."""
    assets, _, screen, _ = unpack_game_context(game_context)
    yes_surface = assets.RESTART_FONT.render(
        assets.TEXT.RESTART_TEXT_YES, True, assets.COLORS.BLACK
    )
    no_surface = assets.RESTART_FONT.render(
        assets.TEXT.RESTART_TEXT_NO, True, assets.COLORS.BLACK
    )

    assets.RECTANGLES.RESTART_BOX_YES = yes_surface.get_rect(
        topleft=assets.POSITIONS.RESTART_POS_YES
    )
    assets.RECTANGLES.RESTART_BOX_NO = no_surface.get_rect(
        topleft=assets.POSITIONS.RESTART_POS_NO
    )
    screen.blit(yes_surface, assets.RECTANGLES.RESTART_BOX_YES)
    screen.blit(no_surface, assets.RECTANGLES.RESTART_BOX_NO)


def draw_end_result_text(game_context: GameContext, win: bool) -> None:
    """Render the end result on screen."""
    assets, _, screen, _ = unpack_game_context(game_context)
    screen.fill(assets.COLORS.PURPLE)
    if win:
        game_result_text = assets.TEXT.WIN_GAME_TEXT
    else:
        game_result_text = assets.TEXT.LOSE_GAME_TEXT

    game_result_surface = assets.GAME_RESULT_FONT.render(
        game_result_text, assets.ANTIALIASING.GAME_RESULT_ANTIALIAS, assets.COLORS.BLACK
    )
    end_game_rect = game_result_surface.get_rect(
        center=assets.POSITIONS.GAME_RESULT_POS
    )
    screen.blit(game_result_surface, end_game_rect)


def draw_end_screen(game_context: GameContext, game_result: bool) -> None:  # X
    """Draws the end of game screen."""
    draw_end_result_text(game_context, game_result)
    draw_restart_text(game_context)


def draw_final_message(game_context: GameContext) -> None:  # X
    """Draws final message to the screen, thanking player."""
    assets, _, screen, _ = unpack_game_context(game_context)
    screen.fill(assets.COLORS.PURPLE)
    final_text = assets.TEXT.THANKS_TEXT
    final_surface = assets.THANKS_FONT.render(
        final_text, assets.ANTIALIASING.THANKS_ANTIALIAS, assets.COLORS.BLACK
    )
    final_rect = final_surface.get_rect(center=assets.POSITIONS.THANKS_POS)
    screen.blit(final_surface, final_rect)


def final_message_loop(game_context: GameContext) -> None:
    """Display frozen final message until the player quits."""
    draw_final_message(game_context)
    pygame.display.flip()

    # Freeze here until quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
                return
