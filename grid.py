"""Module for the Grid class."""
from dataclasses import dataclass
import random

import pygame as pg

from constants import (
    DEFAULT_CELL_SIZE,
    DEFAULT_NUMBER_OF_CELLS
)


@dataclass
class GridCell:
    rect: pg.Rect
    x: int
    y: int


class Grid:
    def __init__(self, num_cells: int = DEFAULT_NUMBER_OF_CELLS, cell_size: int = DEFAULT_CELL_SIZE) -> None:
        self._num_cells = num_cells
        self._cell_size = cell_size

        self._cells = [
            GridCell(
                rect=pg.Rect(i*(self._cell_size+1), j*(self._cell_size+1), self._cell_size, self._cell_size),
                x=i,
                y=j,
            )
            for i in range(self._num_cells)
            for j in range(self._num_cells)
        ]

    def random_cell(self, padding: bool = False) -> tuple[int, int]:
        offset = 1 if padding else 0
        x = random.randint(offset, self.num_cells-offset-1)
        y = random.randint(offset, self.num_cells-offset-1)

        return x, y

    @property
    def cells(self) -> list[GridCell]:
        return self._cells
    
    @property
    def num_cells(self) -> int:
        return self._num_cells
    
    @property
    def height(self) -> int:
        return self._num_cells * (self._cell_size+1)
    
    @property
    def width(self) -> int:
        return self._num_cells * (self._cell_size+1)
    
    @property
    def shape(self) -> tuple[int, int]:
        return (self._num_cells, self._num_cells)
