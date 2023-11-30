from collections import Counter
from typing import Any
from utils import *


tests = [
    test(
        """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2


"""
    ),
]


def parse_line(line: str, /) -> tuple[int, int, int, int, int]:
    return tuple(ints(line))  # type: ignore


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    lines = lmap(parse_line, inp.lines)

    fabric: Counter[tuple[int, int]] = Counter()

    for _n, x, y, w, h in lines:
        for i in range(x, x + w):
            for j in range(y, y + h):
                fabric[(i, j)] += 1

    return sum(v >= 2 for v in fabric.values())


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    lines = lmap(parse_line, inp.lines)

    fabric: dict[tuple[int, int], int] = {}
    claims: set[int] = set()

    for c_n, x, y, w, h in lines:
        claims.add(c_n)

        for i in range(x, x + w):
            for j in range(y, y + h):
                if (i, j) in fabric:
                    claims.discard(fabric[(i, j)])
                    claims.discard(c_n)
                fabric[(i, j)] = c_n

    return claims.pop()
