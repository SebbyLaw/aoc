import itertools
from typing import Any
from utils import *


tests = [
    test(
        """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
    ),
]


def sol(grid: Grid[str], expand_factor: int, /) -> int:
    stars: list[Point] = [p for p, c in grid.items() if c == "#"]
    empty_rows = {i for i in range(grid.rows) if i not in {s.row for s in stars}}
    empty_cols = {i for i in range(grid.cols) if i not in {s.col for s in stars}}

    def dist(a, b):
        c = 0
        for col in range(min(a.col, b.col), max(a.col, b.col)):
            c += expand_factor if col in empty_cols else 1
        for row in range(min(a.row, b.row), max(a.row, b.row)):
            c += expand_factor if row in empty_rows else 1
        return c

    return sum(dist(a, b) for a, b in itertools.combinations(stars, 2))


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return sol(inp.into_grid(), 2)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    return sol(inp.into_grid(), 1_000_000)
