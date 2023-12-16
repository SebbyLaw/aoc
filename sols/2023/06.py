import re
from typing import Any
from utils import *


tests = [
    test(
        """
Time:      7  15   30
Distance:  9  40  200
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    t, d = inp.lines
    times = ints(t)
    distances = ints(d)

    total = 1
    for time, dist in zip(times, distances):
        a, b = quadratic(1, -time, dist)
        total *= int(b - a)

    return total


@runs(*tests, submit)
def b(inp: Input) -> Any:
    t, d = inp.lines
    time = int("".join(re.findall(r"\d+", t)))
    dist = int("".join(re.findall(r"\d+", d)))
    a, b = quadratic(-1, time, -dist)
    return int(b - a)
