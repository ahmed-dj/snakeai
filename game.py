from __future__ import annotations

import pygame as pg

from constants import (
    BOARD_CELL_SIZE,
    BOARD_SIDE_LENGTH,
    DEFAULT_FPS,
    SNAKE_INITIAL_LENGTH,
)
from snake import Move, Snake


PG_EVENT_MOVE_MAPPING = {
    pg.K_UP: Move.UP,
    pg.K_DOWN: Move.DOWN,
    pg.K_RIGHT: Move.RIGHT,
    pg.K_LEFT: Move.LEFT,
}


class Game():
    def __init__(
        self,
        side_length: int = BOARD_SIDE_LENGTH,
        cell_size: int = BOARD_CELL_SIZE,
        snake_initial_length: int = SNAKE_INITIAL_LENGTH,
    ) -> None:
        self.screen = self._init_game(
            side_length=side_length,
            cell_size=cell_size,
        )

        self.clock = pg.time.Clock()
        self.snake = Snake.from_starting_length(
            snake_initial_length=snake_initial_length,
            num_cells=side_length,
            rect_size=cell_size,
        )

    def _init_game(
        self,
        side_length: int = 15,
        pixel_size: int = 10,
        fps: int = DEFAULT_FPS,
    ) -> pg.Surface:
        pg.init()
        side_size = side_length * pixel_size
        screen = pg.display.set_mode((side_size, side_size), pg.SCALED)
        pg.display.set_caption("Snake")
        #pg.mouse.set_visible(False)

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pg.display.flip()

        self.fps = fps
        self.clock = pg.time.Clock()

        return screen
    

    def step(self, move: Move | None):
        
        collided = self.snake.move(move=move)

        self.redraw_screen()

        self.clock.tick(self.fps)

        pg.display.flip()

        return collided

    def redraw_screen(self):
   
        for color, rect in self.snake.get_rects():
            pg.draw(self.screen, color, rect)

    def play(self):

        collided, done = False, False
        while not done:
            for event in pg.event.get():  # User did something
                if event.type == pg.QUIT:  # If user clicked close
                    done = True
                collided = self.step(move=PG_EVENT_MOVE_MAPPING.get(event.type, None))

            done = done or collided
