from itertools import cycle
from typing import Any
from utils import *


tests = [
    test(
        """+1, -2, +3, +1
    """
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return sum(inp.ints)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    nums = inp.ints
    seen: set[int] = set()
    freq = 0

    for num in cycle(nums):
        freq += num
        if freq in seen:
            return freq
        seen.add(freq)
