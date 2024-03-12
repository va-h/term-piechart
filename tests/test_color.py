from __future__ import annotations

import pytest

from term_piechart.color import COLORS
from term_piechart.color import RESET
from term_piechart.color import co
from term_piechart.color import color_distance
from term_piechart.color import cp
from term_piechart.color import generate_new_color
from term_piechart.color import get_distinct_colors
from term_piechart.color import get_random_color
from term_piechart.color import rgb_to_hex


@pytest.mark.parametrize(
    "color, expected_output",
    [
        ("black", "\033[30mHello, world!\033[0m"),
        ("red", "\033[31mHello, world!\033[0m"),
        ("green", "\033[32mHello, world!\033[0m"),
        ("yellow", "\033[33mHello, world!\033[0m"),
        ("blue", "\033[34mHello, world!\033[0m"),
        ("magenta", "\033[35mHello, world!\033[0m"),
        ("cyan", "\033[36mHello, world!\033[0m"),
        ("white", "\033[37mHello, world!\033[0m"),
        ("grey", "\033[90mHello, world!\033[0m"),
        ("bright_red", "\033[91mHello, world!\033[0m"),
        ("bright_green", "\033[92mHello, world!\033[0m"),
        ("bright_yellow", "\033[93mHello, world!\033[0m"),
        ("bright_blue", "\033[94mHello, world!\033[0m"),
        ("bright_magenta", "\033[95mHello, world!\033[0m"),
        ("bright_cyan", "\033[96mHello, world!\033[0m"),
        ("bright_white", "\033[97mHello, world!\033[0m"),
        ("#FF0000", "\033[38;2;255;0;0mHello, world!\033[0m"),
        ("000000", "\033[38;2;0;0;0mHello, world!\033[0m"),
    ],
)
def test_co(color, expected_output):
    text = "Hello, world!"
    assert co(text, color) == expected_output


def test_co_invalid_color():
    text = "Hello, world!"
    with pytest.raises(ValueError):
        co(text, "invalid color")


def test_hardcoded_colors():
    for color, code in COLORS.items():
        text = "Hello, world!"
        expected_output = f"\033[{code}m{text}{RESET}"
        assert co(text, color) == expected_output


@pytest.mark.parametrize(
    "text, color, expected_output",
    [
        ("Hello, world!", "red", "\033[31mHello, world!\033[0m"),
        ("Hello, world!", "green", "\033[32mHello, world!\033[0m"),
        ("Hello, world!", "blue", "\033[34mHello, world!\033[0m"),
        ("Hello, world!", "#FF0000", "\033[38;2;255;0;0mHello, world!\033[0m"),
    ],
)
def test_cp(text, color, expected_output, capsys):
    cp(text, color)
    capured = capsys.readouterr()
    assert capured.out == expected_output + "\n"


@pytest.mark.parametrize(
    "rgb, expected_hex",
    [
        ([0, 0, 0], "000000"),
        ([0.5, 0.5, 0.5], "7f7f7f"),
        ([0.2, 0.4, 0.6], "336699"),
        ([0.8, 0.2, 0.4], "cc3366"),
    ],
)
def test_rgb_to_hex(rgb, expected_hex):
    assert rgb_to_hex(rgb) == expected_hex


def test_get_random_color():
    color = get_random_color()
    assert isinstance(color, list)
    assert len(color) == 3
    for value in color:
        assert isinstance(value, float)
        assert 0 <= value <= 1


def test_color_distance():
    c1 = [0.2, 0.4, 0.6]
    c2 = [0.8, 0.2, 0.4]
    expected_distance = 1.0
    assert color_distance(c1, c2) == expected_distance


def test_generate_new_color():
    existing_colors = [[0.2, 0.4, 0.6], [0.8, 0.2, 0.4]]
    pastel_factor = 0.5
    new_color = generate_new_color(existing_colors, pastel_factor)

    # Check if the generated color is a list
    assert isinstance(new_color, list)

    # Check if the generated color has 3 values
    assert len(new_color) == 3

    # Check if each value in the generated color is a float between 0 and 1
    for value in new_color:
        assert isinstance(value, float)
        assert 0 <= value <= 1

    # Check if the generated color is different from all existing colors
    for color in existing_colors:
        assert color_distance(new_color, color) > 0


def test_get_distinct_colors():
    n = 10
    pastel_factor = 0.9
    distinct_colors = get_distinct_colors(n, pastel_factor)

    # Check if the number of distinct colors is equal to n
    assert len(distinct_colors) == n

    # Check if each color is a string
    for color in distinct_colors:
        assert isinstance(color, str)

    # Check if each color is a valid hexadecimal color code
    for color in distinct_colors:
        assert len(color) == 6
        print(color)
        assert all(c.upper() in "0123456789ABCDEF" for c in color)
