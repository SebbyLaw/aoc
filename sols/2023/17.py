import heapq
from typing import Any, NamedTuple

from utils import *


tests = [
    test(
        """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
    ),
    test(
        """
111111111111
999999999991
999999999991
999999999991
999999999991
"""
    ),
]


class State(NamedTuple):
    cost: int
    point: Point
    direction: Point


def search(grid: Grid[int], mindist: int, maxdist: int, /) -> int:
    start = grid.origin
    goal = grid.bottom_right
    queue: list[State] = [State(0, start, DELTA_UP)]
    seen: set[tuple[Point, Point]] = set()
    costs: dict[tuple[Point, Point], int] = {}

    while queue:
        state = heapq.heappop(queue)
        curr, cost, direction = state.point, state.cost, state.direction
        k = (curr, direction)

        if curr == goal:
            return cost
        if k in seen:
            continue
        seen.add(k)
        for delta in (turn_left(direction), turn_right(direction)):
            incr: int = 0
            for roll in range(1, maxdist + 1):
                new = curr + (delta * roll)
                if new in grid:
                    incr += grid[new]
                    if roll >= mindist:
                        nk = (new, delta)
                        nc = cost + incr
                        try:
                            if costs[nk] <= nc:
                                continue
                        except KeyError:
                            pass
                        costs[nk] = nc
                        heapq.heappush(queue, State(nc, new, delta))

    assert False


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return search(inp.into_grid(int), 0, 3)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    return search(inp.into_grid(int), 4, 10)
