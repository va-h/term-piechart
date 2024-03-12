from __future__ import annotations

import random

from term_piechart.pie import Pie


def test_pie_total():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data)
    assert pie.total() == 60


def test_pie_clear():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data)
    pie.clear()
    assert pie.total() == 0


def test_pie_legend_left():
    legend = {"left": 2}
    pie = Pie(legend=legend)
    assert pie.legend_left() == 2


def test_pie_legend_line():
    legend = {"line": 3}
    pie = Pie(legend=legend)
    assert pie.legend_line() == 4


def test_pie_data_items():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data)
    items = pie.data_items()
    assert len(items) == 3
    assert items[0].name == "A"
    assert items[0].value == 10
    assert items[0].percent == 16.666666666666668
    assert items[0].color is None
    assert items[0].fill == "•"


def test_pie_data_angles():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data)
    items = pie.data_items()
    angles = pie.data_angles(items)
    assert len(angles) == 3
    assert angles[0] == 60
    assert angles[1] == 180
    assert angles[2] == 360


def test_pie_select_data_item():
    angles = [60, 180, 360]
    angle = 45
    selected_item = Pie.select_data_item(angle, angles)
    assert selected_item == 1

    angle = -540
    selected_item = Pie.select_data_item(angle, angles)
    assert selected_item == 0


def test_pie_move():
    pie = Pie()
    assert pie.move(2, 1) == "\033[1;2H"


def test_pie_render_nothing():
    data = []
    pie = Pie(data=data)
    expected_output = ""
    assert str(pie) == expected_output


def test_pie_update():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data)

    new_data = [
        {"name": "X", "value": 15},
        {"name": "Y", "value": 25},
        {"name": "Z", "value": 35},
    ]
    pie.update(new_data)

    assert pie.total() == 75
    assert pie.data_items()[0].name == "X"
    assert pie.data_items()[0].value == 15
    assert pie.data_items()[1].name == "Y"
    assert pie.data_items()[1].value == 25
    assert pie.data_items()[2].name == "Z"
    assert pie.data_items()[2].value == 35


def test_pie_render_legend():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data, top=0, left=0, radius=5)
    expected_output = """
        •••••
    •••••••••••••
  •••••••••••••••••
 •••••••••••••••••••     • A 16.67%
•••••••••••••••••••••
•••••••••••••••••••••    • B 33.33%
•••••••••••••••••••••
 •••••••••••••••••••     • C 50.00%
  •••••••••••••••••
    •••••••••••••
        •••••
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_no_legend():
    data = [
        {"name": "A", "value": 10},
        {"name": "B", "value": 20},
        {"name": "C", "value": 30},
    ]
    pie = Pie(data=data, legend=False, radius=5)
    expected_output = """
        •••••
    •••••••••••••
  •••••••••••••••••
 •••••••••••••••••••
•••••••••••••••••••••
•••••••••••••••••••••
•••••••••••••••••••••
 •••••••••••••••••••
  •••••••••••••••••
    •••••••••••••
        •••••
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_fill_symbol():
    data = [
        {"name": "A", "value": 30, "fill": "*"},
        {"name": "B", "value": 20, "fill": "+"},
        {"name": "C", "value": 10, "fill": "x"},
    ]
    pie = Pie(data=data, legend=False, radius=5)
    expected_output = """
        xx***
    xxxxxx*******
  +++xxxxx*********
 ++++++xxx**********
+++++++++x***********
+++++++++++**********
+++++++++++**********
 ++++++++++*********
  +++++++++********
    +++++++******
        +++**
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_legend_format():
    data = [
        {"name": "A", "value": 30},
        {"name": "B", "value": 100},
        {"name": "C", "value": 45},
    ]

    pie = Pie(
        data,
        radius=5,
        legend={
            "line": 0,
            "left": 10,
            "format": "{label} {name} {percent:.2f}% [{value}€]",
        },
    )

    expected_output = """
        •••••
    •••••••••••••
  •••••••••••••••••
 •••••••••••••••••••
•••••••••••••••••••••          • A 17.14% [30€]
•••••••••••••••••••••          • B 57.14% [100€]
•••••••••••••••••••••          • C 25.71% [45€]
 •••••••••••••••••••
  •••••••••••••••••
    •••••••••••••
        •••••
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_rgb_ascii():
    data = [
        {"name": "A", "value": 30, "color": "red"},
        {"name": "B", "value": 20, "color": "green"},
        {"name": "C", "value": 10, "color": "blue"},
    ]
    pie = Pie(data=data, legend=False, radius=5)
    expected_output = """
        \x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
    \x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
  \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
 \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[34m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[34m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
 \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
  \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
    \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
        \x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[32m•\x1b[0m\x1b[31m•\x1b[0m\x1b[31m•\x1b[0m
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_rgb_hex():
    data = [
        {"name": "A", "value": 30, "color": "ff0000"},
        {"name": "B", "value": 20, "color": "00ff00"},
        {"name": "C", "value": 10, "color": "0000ff"},
    ]
    pie = Pie(data=data, legend=False, radius=5)
    expected_output = """
        \x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
    \x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
  \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
 \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;0;255m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
 \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
  \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
    \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
        \x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;0;255;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m\x1b[38;2;255;0;0m•\x1b[0m
"""

    assert f"\n{str(pie)}" == expected_output


def test_pie_render_autocolor():
    random.seed(10)
    data = [
        {"name": "A", "value": 30},
        {"name": "B", "value": 100},
        {"name": "C", "value": 45},
    ]
    pie = Pie(data=data, legend=False, radius=5, autocolor=True, autocolor_pastel_factor=0.5)
    expected_output = """
        \x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m
    \x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m
  \x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
 \x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;182;157;183m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;120;87;115m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
 \x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
  \x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
    \x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
        \x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m\x1b[38;2;101;248;105m•\x1b[0m
"""
    random.seed()
    assert f"\n{str(pie)}" == expected_output


def test_pie_render_offset():
    data = [
        {"name": "A", "value": 60, "color": "bright_yellow"},
        {"name": "B", "value": 30, "color": "bright_green"},
        {"name": "C", "value": 20, "color": "bright_magenta"},
        {"name": "D", "value": 25, "color": "bright_cyan"},
    ]
    pie = Pie(data, radius=5, top=5, left=5, legend=True)
    expected_output = """
\x1b[5;13H\x1b[96m•\x1b[0m\x1b[5;14H\x1b[96m•\x1b[0m\x1b[5;15H\x1b[93m•\x1b[0m\x1b[5;16H\x1b[93m•\x1b[0m\x1b[5;17H\x1b[93m•\x1b[0m\x1b[5;29H
\x1b[6;9H\x1b[96m•\x1b[0m\x1b[6;10H\x1b[96m•\x1b[0m\x1b[6;11H\x1b[96m•\x1b[0m\x1b[6;12H\x1b[96m•\x1b[0m\x1b[6;13H\x1b[96m•\x1b[0m\x1b[6;14H\x1b[96m•\x1b[0m\x1b[6;15H\x1b[93m•\x1b[0m\x1b[6;16H\x1b[93m•\x1b[0m\x1b[6;17H\x1b[93m•\x1b[0m\x1b[6;18H\x1b[93m•\x1b[0m\x1b[6;19H\x1b[93m•\x1b[0m\x1b[6;20H\x1b[93m•\x1b[0m\x1b[6;21H\x1b[93m•\x1b[0m\x1b[6;29H\x1b[93m•\x1b[0m A 44.44%
\x1b[7;7H\x1b[95m•\x1b[0m\x1b[7;8H\x1b[95m•\x1b[0m\x1b[7;9H\x1b[96m•\x1b[0m\x1b[7;10H\x1b[96m•\x1b[0m\x1b[7;11H\x1b[96m•\x1b[0m\x1b[7;12H\x1b[96m•\x1b[0m\x1b[7;13H\x1b[96m•\x1b[0m\x1b[7;14H\x1b[96m•\x1b[0m\x1b[7;15H\x1b[93m•\x1b[0m\x1b[7;16H\x1b[93m•\x1b[0m\x1b[7;17H\x1b[93m•\x1b[0m\x1b[7;18H\x1b[93m•\x1b[0m\x1b[7;19H\x1b[93m•\x1b[0m\x1b[7;20H\x1b[93m•\x1b[0m\x1b[7;21H\x1b[93m•\x1b[0m\x1b[7;22H\x1b[93m•\x1b[0m\x1b[7;23H\x1b[93m•\x1b[0m\x1b[7;29H
\x1b[8;6H\x1b[95m•\x1b[0m\x1b[8;7H\x1b[95m•\x1b[0m\x1b[8;8H\x1b[95m•\x1b[0m\x1b[8;9H\x1b[95m•\x1b[0m\x1b[8;10H\x1b[95m•\x1b[0m\x1b[8;11H\x1b[96m•\x1b[0m\x1b[8;12H\x1b[96m•\x1b[0m\x1b[8;13H\x1b[96m•\x1b[0m\x1b[8;14H\x1b[96m•\x1b[0m\x1b[8;15H\x1b[93m•\x1b[0m\x1b[8;16H\x1b[93m•\x1b[0m\x1b[8;17H\x1b[93m•\x1b[0m\x1b[8;18H\x1b[93m•\x1b[0m\x1b[8;19H\x1b[93m•\x1b[0m\x1b[8;20H\x1b[93m•\x1b[0m\x1b[8;21H\x1b[93m•\x1b[0m\x1b[8;22H\x1b[93m•\x1b[0m\x1b[8;23H\x1b[93m•\x1b[0m\x1b[8;24H\x1b[93m•\x1b[0m\x1b[8;29H\x1b[92m•\x1b[0m B 22.22%
\x1b[9;5H\x1b[95m•\x1b[0m\x1b[9;6H\x1b[95m•\x1b[0m\x1b[9;7H\x1b[95m•\x1b[0m\x1b[9;8H\x1b[95m•\x1b[0m\x1b[9;9H\x1b[95m•\x1b[0m\x1b[9;10H\x1b[95m•\x1b[0m\x1b[9;11H\x1b[95m•\x1b[0m\x1b[9;12H\x1b[95m•\x1b[0m\x1b[9;13H\x1b[96m•\x1b[0m\x1b[9;14H\x1b[96m•\x1b[0m\x1b[9;15H\x1b[93m•\x1b[0m\x1b[9;16H\x1b[93m•\x1b[0m\x1b[9;17H\x1b[93m•\x1b[0m\x1b[9;18H\x1b[93m•\x1b[0m\x1b[9;19H\x1b[93m•\x1b[0m\x1b[9;20H\x1b[93m•\x1b[0m\x1b[9;21H\x1b[93m•\x1b[0m\x1b[9;22H\x1b[93m•\x1b[0m\x1b[9;23H\x1b[93m•\x1b[0m\x1b[9;24H\x1b[93m•\x1b[0m\x1b[9;25H\x1b[93m•\x1b[0m\x1b[9;29H
\x1b[10;5H\x1b[95m•\x1b[0m\x1b[10;6H\x1b[95m•\x1b[0m\x1b[10;7H\x1b[95m•\x1b[0m\x1b[10;8H\x1b[95m•\x1b[0m\x1b[10;9H\x1b[95m•\x1b[0m\x1b[10;10H\x1b[95m•\x1b[0m\x1b[10;11H\x1b[95m•\x1b[0m\x1b[10;12H\x1b[95m•\x1b[0m\x1b[10;13H\x1b[95m•\x1b[0m\x1b[10;14H\x1b[95m•\x1b[0m\x1b[10;15H\x1b[92m•\x1b[0m\x1b[10;16H\x1b[93m•\x1b[0m\x1b[10;17H\x1b[93m•\x1b[0m\x1b[10;18H\x1b[93m•\x1b[0m\x1b[10;19H\x1b[93m•\x1b[0m\x1b[10;20H\x1b[93m•\x1b[0m\x1b[10;21H\x1b[93m•\x1b[0m\x1b[10;22H\x1b[93m•\x1b[0m\x1b[10;23H\x1b[93m•\x1b[0m\x1b[10;24H\x1b[93m•\x1b[0m\x1b[10;25H\x1b[93m•\x1b[0m\x1b[10;29H\x1b[95m•\x1b[0m C 14.81%
\x1b[11;5H\x1b[95m•\x1b[0m\x1b[11;6H\x1b[95m•\x1b[0m\x1b[11;7H\x1b[95m•\x1b[0m\x1b[11;8H\x1b[95m•\x1b[0m\x1b[11;9H\x1b[95m•\x1b[0m\x1b[11;10H\x1b[95m•\x1b[0m\x1b[11;11H\x1b[95m•\x1b[0m\x1b[11;12H\x1b[95m•\x1b[0m\x1b[11;13H\x1b[95m•\x1b[0m\x1b[11;14H\x1b[92m•\x1b[0m\x1b[11;15H\x1b[92m•\x1b[0m\x1b[11;16H\x1b[93m•\x1b[0m\x1b[11;17H\x1b[93m•\x1b[0m\x1b[11;18H\x1b[93m•\x1b[0m\x1b[11;19H\x1b[93m•\x1b[0m\x1b[11;20H\x1b[93m•\x1b[0m\x1b[11;21H\x1b[93m•\x1b[0m\x1b[11;22H\x1b[93m•\x1b[0m\x1b[11;23H\x1b[93m•\x1b[0m\x1b[11;24H\x1b[93m•\x1b[0m\x1b[11;25H\x1b[93m•\x1b[0m\x1b[11;29H
\x1b[12;6H\x1b[95m•\x1b[0m\x1b[12;7H\x1b[95m•\x1b[0m\x1b[12;8H\x1b[95m•\x1b[0m\x1b[12;9H\x1b[95m•\x1b[0m\x1b[12;10H\x1b[95m•\x1b[0m\x1b[12;11H\x1b[95m•\x1b[0m\x1b[12;12H\x1b[92m•\x1b[0m\x1b[12;13H\x1b[92m•\x1b[0m\x1b[12;14H\x1b[92m•\x1b[0m\x1b[12;15H\x1b[92m•\x1b[0m\x1b[12;16H\x1b[93m•\x1b[0m\x1b[12;17H\x1b[93m•\x1b[0m\x1b[12;18H\x1b[93m•\x1b[0m\x1b[12;19H\x1b[93m•\x1b[0m\x1b[12;20H\x1b[93m•\x1b[0m\x1b[12;21H\x1b[93m•\x1b[0m\x1b[12;22H\x1b[93m•\x1b[0m\x1b[12;23H\x1b[93m•\x1b[0m\x1b[12;24H\x1b[93m•\x1b[0m\x1b[12;29H\x1b[96m•\x1b[0m D 18.52%
\x1b[13;7H\x1b[95m•\x1b[0m\x1b[13;8H\x1b[95m•\x1b[0m\x1b[13;9H\x1b[95m•\x1b[0m\x1b[13;10H\x1b[92m•\x1b[0m\x1b[13;11H\x1b[92m•\x1b[0m\x1b[13;12H\x1b[92m•\x1b[0m\x1b[13;13H\x1b[92m•\x1b[0m\x1b[13;14H\x1b[92m•\x1b[0m\x1b[13;15H\x1b[92m•\x1b[0m\x1b[13;16H\x1b[92m•\x1b[0m\x1b[13;17H\x1b[93m•\x1b[0m\x1b[13;18H\x1b[93m•\x1b[0m\x1b[13;19H\x1b[93m•\x1b[0m\x1b[13;20H\x1b[93m•\x1b[0m\x1b[13;21H\x1b[93m•\x1b[0m\x1b[13;22H\x1b[93m•\x1b[0m\x1b[13;23H\x1b[93m•\x1b[0m\x1b[13;29H
\x1b[14;9H\x1b[92m•\x1b[0m\x1b[14;10H\x1b[92m•\x1b[0m\x1b[14;11H\x1b[92m•\x1b[0m\x1b[14;12H\x1b[92m•\x1b[0m\x1b[14;13H\x1b[92m•\x1b[0m\x1b[14;14H\x1b[92m•\x1b[0m\x1b[14;15H\x1b[92m•\x1b[0m\x1b[14;16H\x1b[92m•\x1b[0m\x1b[14;17H\x1b[93m•\x1b[0m\x1b[14;18H\x1b[93m•\x1b[0m\x1b[14;19H\x1b[93m•\x1b[0m\x1b[14;20H\x1b[93m•\x1b[0m\x1b[14;21H\x1b[93m•\x1b[0m\x1b[14;29H
\x1b[15;13H\x1b[92m•\x1b[0m\x1b[15;14H\x1b[92m•\x1b[0m\x1b[15;15H\x1b[92m•\x1b[0m\x1b[15;16H\x1b[92m•\x1b[0m\x1b[15;17H\x1b[93m•\x1b[0m\x1b[15;29H
"""

    assert f"\n{str(pie)}" == expected_output
