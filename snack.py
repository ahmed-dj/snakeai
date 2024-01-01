"""Module for the Snack class."""
from __future__ import annotations


class Snack:
    def __init__(self, x: int | None, y: int | None) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> None:
        return self._y
    
    @property
    def coords(self) -> tuple[int, int]:
        return (self._x, self._y)

    @x.setter
    def set_x(self, x: int) -> None:
        self._x = x

    @y.setter
    def set_y(self, y: int) -> None:
        self._y = y
