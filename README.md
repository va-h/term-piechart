# Term-Piechart
[![Tests](https://github.com/va-h/term-piechart/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/va-h/term-piechart/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/va-h/term-piechart/graph/badge.svg?token=EXDVWU5KBK)](https://codecov.io/github/va-h/term-piechart)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/term-piechart)

Displays pie charts in your terminal. This is a direct python rewrite of the Ruby Gem TTY-Pie.
Maybe someone else would find this usefull as well.
It requires no external dependencies and supports ASCII and HEX color codes as well as automatic generation of random colors.

## Installation
```shell
python -m pip install term-piechart
```

## Examples

![](https://github.com/va-h/term-piechart/blob/main/.github/images/chart_requests.jpg?raw=true)
```python
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
```

More in [examples](./examples)

### Class Arguments:

- `data` (default: `[]`): A list of dicts with following elements representing the slices
    - `name`: Name of the element
    - `value`: Value of the element
    - `fill` (default: `•`): String to fill the slice with
    - `color`: Hexcode or ANSII [Colorname](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
- `radius` (default: `10`): Amount of columns/rows as the radius to change size
- `autocolor` (default: `False`): Can be enabled if there are no colors specified in the `data` dict
- `autocolor_pastel_factor` (default: `0`): Can be increased until 1
- `fill` (default: `•`): Overwrite the fill symboll for every element
- `legend` (default: `True`): Can be disabled via `False` or configured with a dict with those keys:
  - `line` (default: `1`): Number of lines between legend elements
  - `left` (default: `4`): Number of spaces between chart and left of legend
  - `format` (default: `{label} {name} {percent:.2f}`): Supports `{value}` as well
- `aspect_ratio` (default: `2`): Aspect ratio of the printed chart
- `top` (default: `None`): Amount of rows from top of the visible terminal
- `left` (default: `None`): Amount of columns from the left of the visible terminal



## References

_term-piechart_ is a direct python derivate of:

* Original Ruby Library [Piotr Murachs - TTY:Pie](https://github.com/piotrmurach/tty-pie)
* Generation of Random Colors [Andrew Dewes - Distant Colors](https://gist.github.com/adewes/5884820)


## Developement

### Tox

There's a minimal tox.ini with a requirement on [pyenv](https://github.com/pyenv/pyenv) and [un-def/tox-pyenv-redux](https://github.com/un-def/tox-pyenv-redux).
Zsh users can use this as a reference.

```shell
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
. ~/.zshrc
pyenv install -s 3.12 3.11 3.10 3.9 3.8
tox
```
