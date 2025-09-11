"""Assets for the First Orchard game. All created using pygame."""

from dataclasses import dataclass
from typing import Tuple

import pygame

from first_orchard_solver.gameplay.gamelogic import GameState


# ------------------------
# Colors (RGB)
# ------------------------
@dataclass(frozen=True)
class Color:
    """Class to hold predefined colors."""

    WHITE: Tuple[int, int, int] = (215, 215, 215)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    PURPLE: Tuple[int, int, int] = (128, 0, 128)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)


# ------------------------
# Positions
# ------------------------
@dataclass(frozen=True)
class Positions:
    """Class to hold positions (X,Y)for screen elements."""

    INITIAL_SCREEN_SIZE: Tuple[int, int] = (1280, 720)
    SCREEN_POS: Tuple[int, int] = (0, 0)
    INSTRUCTION_POS: Tuple[int, int] = (100, 100)
    BLUE_CIRCLE_POS: Tuple[int, int] = (850, 600)
    RED_CIRCLE_POS: Tuple[int, int] = (600, 600)
    GREEN_CIRCLE_POS: Tuple[int, int] = (350, 600)
    YELLOW_CIRCLE_POS: Tuple[int, int] = (100, 600)
    BLUE_CIRCLE_TEXT_POS: Tuple[int, int] = (830, 573)
    RED_CIRCLE_TEXT_POS: Tuple[int, int] = (580, 573)
    GREEN_CIRCLE_TEXT_POS: Tuple[int, int] = (330, 573)
    YELLOW_CIRCLE_TEXT_POS: Tuple[int, int] = (80, 573)
    ODDS_TEXT_POS: Tuple[int, int] = (100, 20)
    DIE_REPLACEMENT_TEXT_POS: Tuple[int, int] = (700, 110)
    COACHING_POS: Tuple[int, int] = (100, 175)
    STATS_TEXT_ALTER: int = 50
    CHOOSE_FRUIT_POS: Tuple[int, int] = (100, 175)
    GAME_RESULT_POS: Tuple[int, int] = (640, 150)
    RESTART_POS_YES: Tuple[int, int] = (420, 300)
    RESTART_POS_NO: Tuple[int, int] = (720, 300)
    THANKS_POS: Tuple[int, int] = (640, 150)


# ------------------------
# Rects / Shapes Sizes
# ------------------------
class Rects:
    """Class to hold predifned shapes and sizes."""

    ROLL_BUTTON_RECT: pygame.Rect = pygame.Rect(700, 85, 85, 85)
    DIE_FACE_RADIUS: float = 28
    CIRCLE_RADIUS: float = 75
    BLUE_CIRC_RECT: pygame.Rect = pygame.Rect(
        Positions.BLUE_CIRCLE_POS[0] - CIRCLE_RADIUS,
        Positions.BLUE_CIRCLE_POS[1] - CIRCLE_RADIUS,
        CIRCLE_RADIUS * 2,
        CIRCLE_RADIUS * 2,
    )

    RED_CIRC_RECT: pygame.Rect = pygame.Rect(
        Positions.RED_CIRCLE_POS[0] - CIRCLE_RADIUS,
        Positions.RED_CIRCLE_POS[1] - CIRCLE_RADIUS,
        CIRCLE_RADIUS * 2,
        CIRCLE_RADIUS * 2,
    )

    GREEN_CIRC_RECT: pygame.Rect = pygame.Rect(
        Positions.GREEN_CIRCLE_POS[0] - CIRCLE_RADIUS,
        Positions.GREEN_CIRCLE_POS[1] - CIRCLE_RADIUS,
        CIRCLE_RADIUS * 2,
        CIRCLE_RADIUS * 2,
    )
    YELLOW_CIRC_RECT: pygame.Rect = pygame.Rect(
        Positions.YELLOW_CIRCLE_POS[0] - CIRCLE_RADIUS,
        Positions.YELLOW_CIRCLE_POS[1] - CIRCLE_RADIUS,
        CIRCLE_RADIUS * 2,
        CIRCLE_RADIUS * 2,
    )

    RECTANGLE_1: pygame.Rect = pygame.Rect(1050, 555, 100, 100)
    RECTANGLE_2: pygame.Rect = pygame.Rect(1050, 435, 100, 100)
    RECTANGLE_3: pygame.Rect = pygame.Rect(1050, 315, 100, 100)
    RECTANGLE_4: pygame.Rect = pygame.Rect(1050, 195, 100, 100)
    RECTANGLE_5: pygame.Rect = pygame.Rect(1050, 75, 100, 100)
    COACHING_RECT: pygame.Rect = pygame.Rect(100, 175, 700, 300)
    CIRCLE_RECT_TUPLE: tuple[pygame.Rect, ...] = (
        BLUE_CIRC_RECT,
        RED_CIRC_RECT,
        GREEN_CIRC_RECT,
        YELLOW_CIRC_RECT,
    )

    RESTART_BOX_YES: pygame.Rect | None = None
    RESTART_BOX_NO: pygame.Rect | None = None


# ------------------------
# Screen Text
# ------------------------
@dataclass(frozen=True)
class ScreenText:
    """Class to hold predefined text that will appear on the screen."""

    INSTRUCTION_TEXT: str = "Roll the Die? Click Here: "
    CAPTION_TEXT: str = "First Orchard Solver"
    ODDS_TEXT: str = "Odds of Winning with Perfect Play: "
    RAVEN_DIE_TEXT: str = "OH NO, RAVEN!!!!"
    WILD_DIE_TEXT: str = "WILD! Choose a Color!"
    ALL_GOOD_OPTIONS_TEXT: str = "All choices had equal winning percentages."
    BEST_CHOICE_TEXT: str = "Great Choice! This was one of the optimal moves"
    BAD_CHOICE_TEXT: str = "This was not the best move"
    BETTER_OPTION_TEXT: str = "Better to choose the fruit with the most remaining"
    CURRENT_ODDS_TEXT: str = "Current Odds:"
    BETTER_ODDS_TEXT: str = "Odds from Optimal Choice: "
    DIFFERENCE_ODDS_TEXT: str = "Difference: "
    CHOOSE_FRUIT_TEXT: str = "Click on a circle of your choice!"
    WIN_GAME_TEXT: str = "YOU WIN!!!! Play again?"
    LOSE_GAME_TEXT: str = "Sorry, you lose. Play again?"
    RESTART_TEXT_YES: str = "YES"
    RESTART_TEXT_NO: str = "NO"
    THANKS_TEXT: str = "Thank you for playing!"


# ------------------------
# Antialiasing
# ------------------------
@dataclass(frozen=True)
class Antialiasing:
    """Class to hold boolean values for antialiasing."""

    INSTRUCTION_SURF_ANTIALIAS: bool = True
    CIRCLE_SURF_ANTIALIAS: bool = True
    ODDS_TEXT_ANTIALIAS: bool = True
    DIE_REPLACEMENT_ANTIALIAS: bool = True
    COACHING_ANTIALIAS: bool = True
    CHOOSE_FRUIT_ANTIALIAS: bool = True
    GAME_RESULT_ANTIALIAS: bool = True
    RESTART_ANTIALIAS: bool = True
    THANKS_ANTIALIAS: bool = True


@dataclass(frozen=True)
class Options:
    """Class to hold predefined other options."""

    WIN_PERC_OPTION: Tuple[str, ...] = ("most", "fewest", "random")


@dataclass(frozen=True)
class Assets:
    """Class to hold all assets for the game."""

    COLORS: Color
    RECTANGLES: Rects
    TEXT: ScreenText
    POSITIONS: Positions
    ANTIALIASING: Antialiasing
    OPTIONS: Options
    GAME_STATE: GameState
    # ------------------------
    # Fonts
    # ------------------------
    INSTRUCTION_FONT: pygame.font.Font
    FRUIT_CIRCLE_FONT: pygame.font.Font
    ODDS_FONT: pygame.font.Font
    DIE_REPLACEMENT_FONT: pygame.font.Font
    COACHING_FONT: pygame.font.Font
    CHOOSE_FRUIT_FONT: pygame.font.Font
    GAME_RESULT_FONT: pygame.font.Font
    RESTART_FONT: pygame.font.Font
    THANKS_FONT: pygame.font.Font


def load_assets() -> Assets:
    """Load all assets necessary for game play."""
    return Assets(
        COLORS=Color(),
        RECTANGLES=Rects(),
        TEXT=ScreenText(),
        POSITIONS=Positions(),
        ANTIALIASING=Antialiasing(),
        OPTIONS=Options(),
        GAME_STATE=GameState(),
        INSTRUCTION_FONT=pygame.font.Font(None, 72),
        FRUIT_CIRCLE_FONT=pygame.font.Font(None, 96),
        ODDS_FONT=pygame.font.Font(None, 48),
        DIE_REPLACEMENT_FONT=pygame.font.Font(None, 36),
        COACHING_FONT=pygame.font.SysFont("Consolas", 24),
        CHOOSE_FRUIT_FONT=pygame.font.Font(None, 48),
        GAME_RESULT_FONT=pygame.font.Font(None, 96),
        RESTART_FONT=pygame.font.Font(None, 144),
        THANKS_FONT=pygame.font.Font(None, 96),
    )
