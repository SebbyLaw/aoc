import collections
import math
from typing import Any
from utils import *
from utils.grid import DELTA_LEFT, DELTA_RIGHT


tests = [
    test(
        """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
    ),
]


def discover_num(grid: Grid, coord: Point, /) -> tuple[Point, ...]:
    """Return the number at the given coordinate"""
    # "bfs" to the left and right only
    seen = set()
    nums = []
    queue = collections.deque([coord])
    while queue:
        coord = queue.popleft()
        if coord in seen:
            continue
        seen.add(coord)
        if grid[coord].isdigit():
            nums.append(coord)
            for adj in grid.adj(coord, delta=[DELTA_LEFT, DELTA_RIGHT]):
                if grid[adj] != "#":
                    queue.append(adj)

    nums.sort(key=lambda c: c.col)
    return tuple(nums)


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid()
    symbols = set(inp.raw) - set("0123456789.\n")
    nums: set[tuple[Point, ...]] = set()

    for coord in grid.coords():
        if grid[coord] in symbols:
            # find parts adjacent
            for adj in grid.adj(coord, delta=OCTO_DELTA):
                if grid[adj].isdigit():
                    nums.add(discover_num(grid, adj))

    return sum(int("".join(grid[c] for c in num)) for num in nums)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = inp.into_grid()
    gear_ratios: list[int] = []

    # a gear is any symbol * that is adjacent to exactly two part numbers
    for coord in grid.coords():
        if grid[coord] == "*":
            adjacent_nums: set[tuple[Point, ...]] = set()

            for adj in grid.adj(coord, delta=OCTO_DELTA):
                if grid[adj].isdigit():
                    adjacent_nums.add(discover_num(grid, adj))

            if len(adjacent_nums) == 2:
                gear_ratio: int = math.prod(int("".join(grid[c] for c in num)) for num in adjacent_nums)
                gear_ratios.append(gear_ratio)

    return sum(gear_ratios)
