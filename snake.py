"""Module for the Snake class."""
from __future__ import annotations
import random

from constants import SNAKE_INITIAL_LENGTH, MoveDirection


class Snake:
    def __init__(self, cells_coords: list[tuple[int, int]]) -> None:
        self.cells_coords = cells_coords
        self.current_move_direction = MoveDirection.RIGHT

    @property
    def cells(self) -> list[tuple[int, int]]:
        return self.cells_coords
    
    def __len__(self) -> int:
        return len(self.cells_coords)

    def add_to_tail(self) -> None:
        dx, dy = self.current_move_direction.value
        new_tail_end = (
            self.cells_coords[-1][0] - dx,
            self.cells_coords[-1][1] - dy
        )
        self.cells_coords.append(new_tail_end)
    
    def check_move_direction(self, move_direction: MoveDirection | None) -> MoveDirection:
        if move_direction is None or move_direction == self.current_move_direction:
            return self.current_move_direction
        
        current_dx, current_dy = self.current_move_direction.value
        dx, dy = move_direction.value

        if current_dx == -dx or current_dy == -dy:
            return self.current_move_direction
        
        return move_direction
        
    def move(self, move_direction: MoveDirection | None):
        # Check move w.r.t current direction
        self.current_move_direction = self.check_move_direction(move_direction=move_direction)

        dx, dy = self.current_move_direction.value
        head_x, head_y = self.cells_coords[0]
        new_head = (head_x + dx, head_y + dy)

        self.cells_coords = [new_head] + self.cells_coords[:-1]

    @classmethod
    def from_starting_length(
        cls,
        num_grid_cells: int,
        snake_initial_length: int = SNAKE_INITIAL_LENGTH,
    ) -> Snake:
        area_half_width = num_grid_cells // 2
        if snake_initial_length > area_half_width:
            raise ValueError(
                "The initial length of the snake cannot be"
                "bigger than halh the area width."
            )

        starting_x = random.randint(snake_initial_length+1, area_half_width)
        starting_y = random.randint(
            num_grid_cells // 3,
            2 * num_grid_cells // 3
        )
        cells_coords = [
            (starting_x-i, starting_y)
            for i in range(snake_initial_length)
        ]
        return cls.from_coordinates(
            cells_coords=cells_coords,
        )

    @classmethod
    def from_coordinates(
        cls,
        cells_coords: list[tuple[int, int]],
    ) -> Snake:
        return cls(
            cells_coords=cells_coords,
        )
