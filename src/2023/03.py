import collections
import math
from typing import Any
from utils import *


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


def discover_num(grid: Grid, coord: Coord) -> tuple[Coord, ...]:
    """Return the number at the given coordinate"""
    # "bfs" to the left and right only
    # print(coord)
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
            for dr, dc in ((0, -1), (0, 1)):
                adj = (coord[0] + dr, coord[1] + dc)
                if adj in grid:
                    if grid[adj] != "#":
                        queue.append(adj)

    nums.sort(key=lambda c: c[1])
    return tuple(nums)


@runs(
    # *tests,
    # submit,
)
def a(inp: Input) -> Any:
    grid = Grid([list(line.strip()) for line in inp.lines])

    symbols = set(inp.raw) - set("0123456789.\n")
    # print(symbols)

    nums: set[tuple[Coord, ...]] = set()

    for row in range(grid.rows):
        for col in range(grid.cols):
            if grid[(row, col)] in symbols:
                # find parts adjacent
                for dr, dc in OCTO_DELTA:
                    adj = (row + dr, col + dc)
                    if adj in grid:
                        if grid[adj].isdigit():
                            nums.add(discover_num(grid, adj))

    total = 0
    for num in nums:
        total += int("".join(grid[c] for c in num))
    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = Grid([list(line.strip()) for line in inp.lines])

    gear_ratios: list[int] = []

    # a gear is any symbol * that is adjacent to exactly two part numbers

    for row in range(grid.rows):
        for col in range(grid.cols):
            if grid[(row, col)] == "*":
                adjacent_nums: set[tuple[Coord, ...]] = set()

                # find parts adjacent
                for dr, dc in OCTO_DELTA:
                    adj = (row + dr, col + dc)
                    if adj in grid:
                        if grid[adj].isdigit():
                            adjacent_nums.add(discover_num(grid, adj))

                if len(adjacent_nums) == 2:
                    gear_ratio: int = math.prod(int("".join(grid[c] for c in num)) for num in adjacent_nums)
                    gear_ratios.append(gear_ratio)

    return sum(gear_ratios)
