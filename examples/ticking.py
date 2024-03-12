#!/usr/bin/env python
from term_piechart import Pie
from time import sleep

data = [
    {"name": "A", "value": 0},
    {"name": "B", "value": 100},
]

pie_basic = Pie(data, radius=5, top=5, left=1, autocolor=True, legend=False)

step_size = 10
for i in range(0, step_size + 1):
    data[0]["value"] = i * step_size
    data[1]["value"] = 100 - (i * step_size)
    pie_basic.update(data)
    print(pie_basic)
    sleep(0.5)
