"""Module for utils for the Snake game."""
from colour import Color


def get_color_gradient(start: str, end: str, num_colors: int) -> list[str]:
    return [
        i.hex for i in Color(start).range_to(Color(end), num_colors)
    ]


def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return sum(
        abs(point1[i] - point2[i])
        for i in range(len(point1))
    )
