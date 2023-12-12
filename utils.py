"""Module for utils for the Snake game."""
from colour import Color


def get_color_gradient(start: str, end: str, num_colors: int) -> list[str]:
    return [
        i.hex for i in Color(start).range_to(Color(end), num_colors)
    ]
