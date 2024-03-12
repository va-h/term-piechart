from __future__ import annotations

from term_piechart.color import co
from term_piechart.slice import Slice


def test_data_item():
    name = "Item 1"
    value = 10.5
    percent = 25.0
    color = "blue"
    fill = "#"

    data_item = Slice(name, value, percent, color, fill)

    # Check if the attributes are set correctly
    assert data_item.name == name
    assert data_item.value == value
    assert data_item.percent == percent
    assert data_item.color == color
    assert data_item.fill == fill

    # Check if the angle is calculated correctly
    expected_angle = percent * 360 / 100
    assert data_item.angle == expected_angle

    # Check if the label is generated correctly
    expected_label = f"{co(fill, color)} {name} {percent:.2f}%"
    assert data_item.label == expected_label
