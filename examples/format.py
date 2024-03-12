#!/usr/bin/env python
from term_piechart import Pie

requests = [
    {"name": "GET", "value": 9983},
    {"name": "POST", "value": 7005},
    {"name": "DELETE", "value": 3323},
    {"name": "PUT", "value": 2794},
    {"name": "PATCH", "value": 1711},
]

pie = Pie(
    requests,
    radius=5,
    autocolor=True,
    autocolor_pastel_factor=0.7,
    legend={"line": 0, "format": "{label} {name:<8} {percent:>5.2f}% [{value}]"},
)

print(pie)