from typing import Any
from utils import *


tests = [
    test(
        """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    ),
]


def sol(inp: Input, xval: int, /) -> int:
    total = 0

    def reflects_at(s: list[str], n: int, /) -> int:
        x = 0
        for a, b in zip(s[n:], s[:n][::-1]):
            x += sum(i != j for i, j in zip(a, b))
        return x

    for grid in [c.raw.splitlines() for c in inp.split("\n\n")]:
        try:
            total += next(r for r in range(1, len(grid)) if reflects_at(grid, r) == xval) * 100
        except StopIteration:
            cols = ["".join(row[i] for row in grid) for i in range(len(grid[0]))]
            total += next(c for c in range(1, len(cols)) if reflects_at(cols, c) == xval)

    return total


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return sol(inp, 0)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    return sol(inp, 1)
