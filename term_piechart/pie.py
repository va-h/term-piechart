# colorama
from __future__ import annotations

from math import atan2
from math import degrees
from math import sqrt

from .color import co
from .color import get_distinct_colors
from .slice import Slice


class Pie:
    """
    A class representing a pie chart.
    """

    POINT_SYMBOL = "•"

    LEGEND_LINE_SPACE = 1
    LEGEND_LEFT_SPACE = 4

    cursor = None
    palette_hex: list = []

    def __init__(
        self,
        data: list[dict] | None = None,
        top: int = 0,
        left: int = 0,
        radius: int = 10,
        legend: dict | bool = True,
        fill: str = POINT_SYMBOL,
        aspect_ratio: int = 2,
        autocolor: bool = False,
        autocolor_pastel_factor: float = 0,
    ) -> None:
        if data is None:
            data = []

        self.data = data
        self.top = top
        self.left = left
        self.radius = radius
        self.legend = legend
        self.fill = fill
        self.aspect_ratio = aspect_ratio
        self.center_x = left + radius * aspect_ratio
        self.center_y = top + radius
        self.autocolor = autocolor

        if autocolor:
            self.palette_hex = get_distinct_colors(len(data), pastel_factor=autocolor_pastel_factor)

    def __str__(self) -> str:
        """
        Prints the chart.
        """
        return self.render()

    @staticmethod
    def data_angles(items: list[Slice]):
        """
        Calculate the angles for each item in the given list of items.
        """
        start_angle = 0
        acc = []
        for item in items:
            acc.append(start_angle + item.angle)
            start_angle += item.angle
        return acc

    @staticmethod
    def select_data_item(angle: float, angles: list) -> int:
        """
        Get the index given angle in the list angles.
        """
        for a in angles:
            if (360 / 2 - angle) < a:
                return angles.index(a)
        return 0

    @staticmethod
    def move(x: int, y: int) -> str:
        """
        Moves the cursor to the specified position on the terminal rows and colums from top.
        """
        return f"\033[{y};{x}H"

    def total(self) -> float:
        """
        Returns the total value of the data.
        """
        return sum(d["value"] for d in self.data)

    def clear(self) -> None:
        """
        Clears the chart data.
        """
        self.data = []

    def update(self, data) -> None:
        """
        Updates the chart data.
        """
        self.data = data

    def legend_left(self) -> int:
        """
        Returns the amount of whitespaces left of the legend until piechart.
        """
        if isinstance(self.legend, bool):
            return self.LEGEND_LEFT_SPACE

        return self.legend.get("left", self.LEGEND_LEFT_SPACE)

    def legend_line(self) -> int:
        """
        Returns the amount of lines between each legend item.
        """
        if isinstance(self.legend, bool):
            return self.LEGEND_LINE_SPACE + 1

        return self.legend.get("line", self.LEGEND_LINE_SPACE) + 1

    def data_items(self) -> list[Slice]:
        """
        Returns a list of Slice Object for the given Data Objects.
        """
        total_value = self.total()
        items = []
        for i, item in enumerate(self.data):
            args = {}
            args["percent"] = (item["value"] * 100) / total_value
            args["fill"] = item.get("fill", self.fill[i % len(self.fill)])
            args["name"] = item.get("name")
            args["value"] = item.get("value")
            args["color"] = item.get("color", None)

            if not args["color"] and self.autocolor:
                args["color"] = self.palette_hex[i]

            if isinstance(self.legend, dict) and "format" in self.legend:
                args["label_format"] = self.legend["format"]

            items.append(Slice(**args))

        return items

    def render(self) -> str:
        """
        Renders the pie chart and returns it as a string.
        """

        items = self.data_items()
        if not items:
            return ""
        angles = Pie.data_angles(items)
        output = []

        labels = [item.label for item in items]
        label_vert_space = self.legend_line()
        label_horiz_space = self.legend_left()
        label_offset = int(len(labels) / 2)
        label_boundry = int(label_vert_space * label_offset)
        labels_range = list(range(-label_boundry, label_boundry + 1, label_vert_space))

        for y in range(-self.radius, self.radius + 1):
            width = round(sqrt(self.radius * self.radius - y * y) * self.aspect_ratio)
            width = width if width != 0 else round(self.radius / self.aspect_ratio)

            if not self.top:
                output.append((self.center_x - width) * " ")

            for x in range(-width, width + 1):
                angle = degrees(atan2(x, y))
                item = items[Pie.select_data_item(angle, angles)]  # type: ignore

                if self.top:
                    output.append(Pie.move(self.center_x + x, self.center_y + y))
                if item.color:
                    output.append(co(item.fill, item.color))
                else:
                    output.append(item.fill)

            if self.legend:
                if self.top:
                    output.append(
                        Pie.move(
                            self.center_x + self.aspect_ratio * self.radius + label_horiz_space,
                            self.center_y + y,
                        )
                    )
                if y in labels_range:
                    if not self.top:
                        output.append(((self.center_x - (self.left + width)) + label_horiz_space) * " ")
                    label_index = int(label_offset + y / label_vert_space)
                    if label_index < len(labels):
                        output.append(labels[label_index])

            output.append("\n")

        return "".join(output)
