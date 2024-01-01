from __future__ import annotations
from tqdm import tqdm

import numpy as np
import pygame as pg

from agent import ReinforceAgent
from grid import Grid
from snack import Snack
from snake import Snake
from stats import GameStats
from utils import manhattan_distance


from constants import (
    DEFAULT_CELL_SIZE,
    DEFAULT_FPS,
    DEFAULT_BACKGROUND_COLOUR,
    DEFAULT_CELL_COLOUR,
    DEFAULT_SNACK_COLOUR,
    DEFAULT_SNAKE_CELL_COLOUR,
    DEFAULT_NUMBER_OF_CELLS,
    MoveDirection,
    PG_EVENT_KEY_MOVE_MAPPING,
    SNACK_REWARD,
    DEFAULT_REWARD,
    COLLISION_REWARD,
)


class Game:
    def __init__(
        self,
        num_cells: int = DEFAULT_NUMBER_OF_CELLS,
        cell_size: int = DEFAULT_CELL_SIZE,
        fps: int = DEFAULT_FPS,
    ) -> None:
        self.grid = Grid(
            num_cells=num_cells,
            cell_size=cell_size,
        )
        self.reset()
        self.state = self.get_state()
    
        self.fps = fps

        self._init_game()

    def _init_game(self):
        screen_dims = (self.grid.width, self.grid.height)
        self.screen = pg.display.set_mode(screen_dims, pg.SCALED)
        pg.display.set_caption("Snake")

        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(DEFAULT_BACKGROUND_COLOUR)

        self.background = background

        #self.screen.blit(background, (0, 0))
        #pg.display.flip()

        self.clock = pg.time.Clock()

    def generate_snack(self, padding: bool = False) -> Snack:
        x, y = self.grid.random_cell(padding=padding)
        while (hasattr(self, "snack") and (x, y) == self.snack) or (x, y) in self.snake.cells:
            x, y = self.grid.random_cell(padding=padding)

        if padding:
            while any(manhattan_distance((x, y), (sx, sy)) < 2 for sx, sy in self.snake.cells):
                x, y = self.grid.random_cell(padding=padding)

        return Snack(x=x, y=y)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        snake_cells = self.snake.cells
        for cell in self.grid.cells:
            colour = (
                DEFAULT_SNAKE_CELL_COLOUR
                if (cell.x, cell.y) in snake_cells
                else (
                    DEFAULT_SNACK_COLOUR
                    if (cell.x, cell.y) == self.snack.coords
                    else DEFAULT_CELL_COLOUR
                )
            )
            pg.draw.rect(self.screen, pg.Color(colour), cell)

    def is_snack_eaten(self):
        return self.snake.cells[0] == self.snack.coords
    
    def step(self, move_direction: MoveDirection | None, render: bool = True) -> tuple[bool, int]:
        self.snake.move(move_direction=move_direction)

        reward = DEFAULT_REWARD
        if self.is_snack_eaten():
            self.snack = self.generate_snack()
            self.snake.add_to_tail()
            reward = SNACK_REWARD

        if render:
            self.draw()
            pg.display.update()
            pg.time.delay(200)

        done = self.is_collision()

        reward = COLLISION_REWARD if done else reward
        return done, reward

    def is_collision(self):
        snake_head_x, snake_head_y = snake_head = self.snake.cells[0]
        if not (0 <= snake_head_x < self.grid.num_cells and 0 <= snake_head_y < self.grid.num_cells):
            return True

        if snake_head in self.snake.cells[1:]:
            return True

        return False
    
    def reset(self):
        self.snake = Snake.from_starting_length(num_grid_cells=self.grid.num_cells)
        self.snack = self.generate_snack(padding=True)
        self.points = 0
        self.num_steps = 0
    
    def get_state(self) -> np.ndarray:
        try:
            grid_cells = np.zeros(self.grid.shape)
            for sx, sy in self.snake.cells_coords + [self.snack.coords]:
                grid_cells[sx, sy] = 1
            self.state = grid_cells
        except IndexError:
            grid_cells = self.state
        return grid_cells[None, None, :, :].astype(dtype=np.float32) # Channel, H, W
    
    def summary(self, episode_i: int):
        return f"""
            Summary for episode {episode_i}: \n
            - The snake has {len(self.snake)} cells.
            - The total reward of this current episode is {self.points}.
            - Current episode length is {self.num_steps}. \n
        """

    def play_agent(self, agent: ReinforceAgent, num_episodes: int = 2, eval: bool = False, render: bool = True) -> GameStats:
        game_stats = GameStats()
        for episode_i in tqdm(range(1, num_episodes+1), total=num_episodes):
            done = False
            self.reset()
            while not done:
                action = agent.select_policy_action(state=self.get_state(), eval=eval)
                done, reward = self.step(move_direction=action, render=render)
                agent.add_reward(reward=reward)
                self.points += reward
                self.num_steps += 1
            
            if not eval:
                agent.train_step()
            game_stats.add_episode(reward=self.points, duration=self.num_steps)
            tqdm.write(self.summary(episode_i))

        return game_stats


    def play(self):
        collided, done = False, False
        from time import time
        start = time()
        while not done:
            self.clock.tick(60)
            move_direction = None
            for event in pg.event.get():  # User did something
                if event.type == pg.QUIT:  # If user clicked close
                    done = True
                #collided = self.step(move_direction=PG_EVENT_MOVE_MAPPING.get(event.type, None))

                if event.type == pg.KEYDOWN:
                    if event.key in PG_EVENT_KEY_MOVE_MAPPING.keys():
                        move_direction = PG_EVENT_KEY_MOVE_MAPPING.get(event.key, None)
                
            done, _ = self.step(move_direction=move_direction)
            
            #pg.display.flip()
            

            

