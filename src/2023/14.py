from typing import Any
from utils import *


tests = [
    test(
        """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid()

    for c in grid.coords():
        if grid[c] == "O":
            new_spot = None
            for item in grid.to_up(c):
                if grid[item] != ".":
                    break
                else:
                    new_spot = item

            if new_spot is not None:
                grid[c] = "."
                grid[new_spot] = "O"

    total = 0
    for c in grid.coords():
        if grid[c] == "O":
            total += grid.cols - c[0]

    return total


@runs(
    # *tests,
    # submit,
)
def b(inp: Input) -> Any:
    ...
