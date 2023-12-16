from operator import neg
from typing import Any
from utils import *


tests = [
    test(
        """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    elves = inp.raw.split("\n\n")
    return max(lmap(sum, lmap(ints, elves)))


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    elves = inp.raw.split("\n\n")
    counts = lmap(sum, lmap(ints, elves))
    counts.sort(key=neg)
    return counts[0] + counts[1] + counts[2]
