from __future__ import annotations
from enum import Enum
import random

import numpy as np
import pygame as pg

from constants import BOARD_CELL_SIZE, BOARD_SIDE_LENGTH, SNAKE_ENDS_COLORS, SNAKE_INITIAL_LENGTH
from utils import get_color_gradient


class Move(Enum):
    UP: list[int] = [0, -1]
    DOWN: list[int] = [0, 1]
    RIGHT: list[int] = [1, 0]
    LEFT: list[int] = [-1, 0]


class SnakeRect(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int) -> None:
        super().__init__()

        print(x, y, size)
        self.x = x
        self.y = y
        self.size = size
        self.rect = pg.Rect(
            left=self.x,
            top=self.y,
            width=self.size,
            height=self.size,
        )

    @property
    def rect(self) -> pg.Rect:
        return self.rect


class Snake(pg.sprite.Sprite):
    def __init__(
        self,
        rects: list[SnakeRect],
        area: pg.Rect,
        rect_size: int = 10,
    ) -> None:
        super().__init__()
        self.area = area
        self.rects = rects
        self.current_move: Move = Move.RIGHT
        self.rect_size = rect_size

    def get_rects(self) -> list[tuple(pg.Color, pg.Rect)]:
        start, end = SNAKE_ENDS_COLORS
        rect_colors = get_color_gradient(
            start=start,
            end=end,
            num_colors=len(self.rects),
        )
        return [
            (pg.Color(rect_colors[i]), rect.rect)
            for i, rect in enumerate(self.rects)
        ]

    def check_valid_move(self, move: Move) -> bool:
        return sum(move.value * self.rects[0]) != 0

    def check_collision(self) -> bool:
        # Check collision with wall
        max_x, max_y = (
            self.area.width / self.rect_size - 1,
            self.area.height / self.rect_size - 1,
        )
        head_x, head_y = self.rects[0].x, self.rects[0].y
        if not (0 <= head_x <= max_x) or not (0 <= head_y <= max_y):
            return True

        # Check collising with its tail
        return any(
            head_x == rect.x and head_y == rect.y
            for rect in self.rects[1:]
        )

    def move(self, move: Move | None = None) -> bool:
        self.move = move if move is not None and self.check_valid_move(move=move) else self.move

        new_x, new_y = (
            self.rects[0].x + self.move.value[0],
            self.rects[0].y + self.move.value[1],
        )
        self.rects = [
            SnakeRect(
                x=new_x,
                y=new_y,
                size=self.rect_size,
            )
        ] + self.rects[1:-1]
        return self.check_collision()
    
    @classmethod
    def from_starting_length(
        cls,
        snake_initial_length: int = SNAKE_INITIAL_LENGTH,
        num_cells: int = BOARD_SIDE_LENGTH,
        rect_size: int = BOARD_CELL_SIZE,
    ) -> Snake:
        area_half_width = num_cells // 2
        if snake_initial_length > area_half_width:
            raise ValueError(
                "The initial length of the snake cannot be"
                "bigger than halh the area width."
            )

        starting_x = random.randint(snake_initial_length+1, area_half_width)
        starting_y = random.randint(
            num_cells // 3,
            2 * num_cells // 3
        )
        return cls.from_rects(
            rects=[
                np.array([starting_x-i, starting_y])
                for i in range(snake_initial_length)
            ],
            area=area,
            rect_size=rect_size,
        )

    @classmethod
    def from_rects(
        cls,
        rects: list[np.ndarray],
        area: pg.Rect,
        rect_size: int = BOARD_CELL_SIZE,
    ) -> Snake:
        return cls(
            rects=[
                SnakeRect(
                    x=x,
                    y=y,
                    size=rect_size
                )
                for x, y in rects
            ],
            area=area,
            rect_size=rect_size,
        )
