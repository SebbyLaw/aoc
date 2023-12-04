import math
from typing import Any, Iterable
from utils import *


tests = [
    test(
        """
30373
25512
65332
33549
35390
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid(int)

    visible = 0

    def is_visible(tree: Coord, trees: Iterable[Coord], /) -> bool:
        return all(grid[tree] > grid[other] for other in trees)

    for tree in grid.coords():
        if grid.is_edge(tree):
            visible += 1
            continue

        if (
            is_visible(tree, grid.to_left(tree))
            or is_visible(tree, grid.to_right(tree))
            or is_visible(tree, grid.to_up(tree))
            or is_visible(tree, grid.to_down(tree))
        ):
            visible += 1

    return visible


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = inp.into_grid(int)

    def viewable(cmp: int, trees: Iterable[Coord], /) -> int:
        total = 0
        for tree in trees:
            total += 1
            if grid[tree] >= cmp:
                break
        return total

    def score(tree: Coord) -> int:
        if grid.is_edge(tree):
            return 0

        val = grid[tree]
        return math.prod(
            (
                viewable(val, grid.to_left(tree)),
                viewable(val, grid.to_right(tree)),
                viewable(val, grid.to_up(tree)),
                viewable(val, grid.to_down(tree)),
            )
        )

    return max(score(tree) for tree in grid.coords())
