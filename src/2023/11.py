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


def sol(lines: list[str], expand_factor: int, /) -> int:
    stars: list[Coord] = [(r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "#"]
    empty_rows = {i for i in range(len(lines)) if i not in {s[0] for s in stars}}
    empty_cols = {i for i in range(len(lines[0])) if i not in {s[1] for s in stars}}

    def dist(a, b):
        c = 0
        for col in range(min(a[1], b[1]), max(a[1], b[1])):
            c += expand_factor if col in empty_cols else 1
        for row in range(min(a[0], b[0]), max(a[0], b[0])):
            c += expand_factor if row in empty_rows else 1
        return c

    return sum(dist(a, b) for a, b in itertools.combinations(stars, 2))


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return sol(inp.lines, 2)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    return sol(inp.lines, 1_000_000)
