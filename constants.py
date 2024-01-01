"""Constants for Snake game."""
from enum import Enum

import pygame as pg


BOARD_SIDE_LENGTH: int = 15
BOARD_CELL_SIZE: int = 10

DEFAULT_NUMBER_OF_CELLS = 15 # Number of cells on each side
DEFAULT_CELL_SIZE = 10 # Number of pixels per cell (square)
DEFAULT_CELL_COLOUR = "#92A07C"
DEFAULT_CELL_BORDER_COLOUR = DEFAULT_BACKGROUND_COLOUR = "#99A681"
DEFAULT_SNACK_COLOUR = "#83382F"
DEFAULT_SNAKE_CELL_COLOUR = "#0C0C0A"

DEFAULT_FPS = 60 # Number of frames per second

# FPS
DEFAULT_FPS: int = 60

# Snake
SNAKE_INITIAL_LENGTH: int = 4
SNAKE_ENDS_COLORS = ["#22c1c3", "#fdbb2d"]


class MoveDirection(Enum):
    UP: tuple[int] = (0, -1)
    DOWN: tuple[int] = (0, 1)
    RIGHT: tuple[int] = (1, 0)
    LEFT: tuple[int] = (-1, 0)


PG_EVENT_KEY_MOVE_MAPPING = {
    pg.K_UP: MoveDirection.UP,
    pg.K_DOWN: MoveDirection.DOWN,
    pg.K_RIGHT: MoveDirection.RIGHT,
    pg.K_LEFT: MoveDirection.LEFT,
}


# Rewards
SNACK_REWARD = 10
DEFAULT_REWARD = 0
COLLISION_REWARD = -3
