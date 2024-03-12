#!/usr/bin/env python
from term_piechart import Pie

charts = []

charts.append([
    {"name": "A", "value": 60, "color": "bright_yellow"},
    {"name": "B", "value": 30, "color": "bright_green"},
    {"name": "C", "value": 20, "color": "bright_magenta"},
    {"name": "D", "value": 25, "color": "bright_cyan"},
])

charts.append([
    {"name": "A", "value": 30, "color": "red"},
    {"name": "B", "value": 20, "color": "green"},
    {"name": "C", "value": 10, "color": "blue"},
])

charts.append([
    {"name": "A", "value": 10, "color": "ff0000"},
    {"name": "B", "value": 20, "color": "00ff00"},
    {"name": "C", "value": 30, "color": "0000ff"},
])

charts.append([
    {"name": "A", "value": 30, "fill": "*"},
    {"name": "B", "value": 20, "fill": "+"},
    {"name": "C", "value": 10, "fill": "x"},
])

pie = Pie(radius=3)

for data in charts:
    pie.update(data)
    print(pie)

print((Pie(charts[0], radius=3, fill="♡")))