"""Graphical version of the First Orchard game using pygame."""

import pygame

from first_orchard_solver.gameplay import eventhandler as eh
from first_orchard_solver.gameplay import rend_static as static
from first_orchard_solver.gameplay.context import init_game_context, unpack_game_context


def play_orchard_screen() -> None:
    """Ind for a graphical version of the Orchard game."""
    game_context = init_game_context()
    assets, background, screen, game_state = unpack_game_context(game_context)
    static.draw_background(game_context)
    clock = pygame.time.Clock()
    running = True
    color = None
    idx = None

    # initialize flags
    game_state.pending_fruit_click = False
    game_state.fruit_click_enabled = False
    game_state.die_click_enabled = True

    while running:
        # Enable fruit clicks if pending (only at start of loop)
        if game_state.pending_fruit_click:
            game_state.fruit_click_enabled = True
            game_state.pending_fruit_click = False

        screen.blit(background, assets.POSITIONS.SCREEN_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --------- DIE ROLL ---------
            if event.type == pygame.MOUSEBUTTONUP and game_state.die_click_enabled:
                if assets.RECTANGLES.ROLL_BUTTON_RECT.collidepoint(event.pos):
                    game_state.orchard_die.roll()
                    game_state.stats_flag = False

                    if game_state.orchard_die.die_result == 1:
                        eh.die_results_raven(game_context)

                    elif game_state.orchard_die.die_result == 2:
                        eh.die_results_wild(game_context)

                    else:
                        color = eh.die_results_color(game_context)
                        game_state.replace_text = None

            # --------- FRUIT PICK ---------
            if event.type == pygame.MOUSEBUTTONDOWN and game_state.fruit_click_enabled:
                idx = eh.choose_fruit(game_context, event)
                game_state.stats_flag = True
                if idx is not None:
                    game_state.fruit_click_enabled = False
                    game_state.die_click_enabled = True

            # --------- RESTART GAME ---------
            if event.type == pygame.MOUSEBUTTONDOWN and game_state.is_game_over():
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
                if assets.RECTANGLES.RESTART_BOX_YES.collidepoint(event.pos):
                    play_orchard_screen()  # restart game
                    continue
                elif assets.RECTANGLES.RESTART_BOX_NO.collidepoint(event.pos):
                    static.final_message_loop(game_context)

        # --------- DRAWING ---------
        eh.draw_all_screen(game_context, color, idx)
        clock.tick(60)

    pygame.quit()


play_orchard_screen()
