from itertools import batched
from typing import Any
from utils import *


tests = [
    test(
        """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    total = 0
    for a, b, c, d in batched(inp.ints, 4):
        e1 = set(range(a, b + 1))
        e2 = set(range(c, d + 1))
        if e1.issubset(e2) or e2.issubset(e1):
            total += 1
    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    total = 0
    for a, b, c, d in batched(inp.ints, 4):
        e1 = set(range(a, b + 1))
        e2 = set(range(c, d + 1))
        if e1 & e2:
            total += 1
    return total
