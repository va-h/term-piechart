from __future__ import annotations

import random

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
RESET = "\033[0m"
COLORS: dict[str, int] = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "grey": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}


def rgb_to_hex(rgb: list[float]) -> str:
    """
    Convert rgb colors to hex colors
    """
    return f"{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"


"""
Distant Color Script by Andreas Dewes
https://gist.github.com/adewes/5884820
"""


def get_random_color(pastel_factor: float = 0.5) -> list[float]:
    """
    Generate a random color in RGB format.
    """
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1: list[float], c2: list[float]) -> float:
    """
    Calculate the distance between two colors.
    """
    return sum(abs(x[0] - x[1]) for x in zip(c1, c2))


def generate_new_color(existing_colors: list[list[float]], pastel_factor: float = 0.5):
    """
    Generates a new color that is different from the existing colors.
    """
    max_distance = None
    best_color = None
    for _ in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min(color_distance(color, c) for c in existing_colors)
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


def get_distinct_colors(n: int = 10, pastel_factor: float = 0.9) -> list[str]:
    colors = []

    for _ in range(0, n):
        colors.append(generate_new_color(colors, pastel_factor))

    return [rgb_to_hex(c) for c in colors]


def co(text: object, color: str) -> str:
    """
    Returns text in color, accepts ANSI Colors or Hex Colors.
    """

    if color in COLORS:
        return f"\033[{COLORS[color]}m{text}{RESET}"

    try:
        hex_int = int(color.lstrip("#"), 16)
        return f"\033[38;2;{hex_int >> 16};{hex_int >> 8 & 0xFF};{hex_int & 0xFF}m{text}{RESET}"
    except ValueError:
        pass

    raise ValueError(f"Invalid color: {color}")


def cp(text: object, color: str) -> None:
    """
    Prints text in color, accepts ANSI Colors or Hex Colors.
    """
    print(co(text, color))
