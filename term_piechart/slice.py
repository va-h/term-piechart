from __future__ import annotations

from dataclasses import dataclass

from .color import co


@dataclass
class Slice:
    """
    Represents a slice of the pie chart.
    """

    name: str
    value: float
    percent: float
    color: str | None
    fill: str
    label_format: str = "{label} {name} {percent:.2f}%"

    @property
    def angle(self) -> float:
        """
        Calculates the angle (in degrees) of the slice.
        """
        return float(self.percent * 360 / 100)

    @property
    def label(self) -> str:
        """
        Generates the label for the slice.
        """
        label = co(self.fill, self.color) if self.color else self.fill
        return self.label_format.format(label=label, name=self.name, percent=self.percent, value=self.value)
