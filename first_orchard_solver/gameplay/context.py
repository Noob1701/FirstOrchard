"""
Module defines the GameContext dataclass.

Which holds references to the main game screen,
background, assets, and current game state for the First Orchard game.
"""

from dataclasses import dataclass
from typing import Tuple

import pygame

from first_orchard_solver.gameplay.assets import Assets, load_assets
from first_orchard_solver.gameplay.gamelogic import GameState


@dataclass
class GameContext:
    """
    Class to hold the game context.

    Attributes
    ----------
        screen (pygame.Surface): The main game screen.
        background (pygame.Surface): The background surface.
        assets (Assets): The game assets.
        game_state (GameState): The current state of the game.

    """

    screen: pygame.Surface
    background: pygame.Surface
    assets: Assets
    game_state: GameState


def init_game_context() -> GameContext:
    """Initialize the Pygame environment and returns the inital game context."""
    pygame.init()
    assets = load_assets()
    screen = pygame.display.set_mode(assets.POSITIONS.INITIAL_SCREEN_SIZE)
    pygame.display.set_caption(assets.TEXT.CAPTION_TEXT)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(assets.COLORS.PURPLE)
    game_state = assets.GAME_STATE
    return GameContext(
        screen=screen, background=background, assets=assets, game_state=game_state
    )


def unpack_game_context(
    game_context: GameContext,
) -> Tuple[Assets, pygame.Surface, pygame.Surface, GameState]:
    """Unpacks the GameContext for easier access."""
    assets = game_context.assets
    background = game_context.background
    screen = game_context.screen
    game_state = game_context.game_state
    return assets, background, screen, game_state
