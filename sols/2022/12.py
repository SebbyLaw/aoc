from collections import deque
from typing import Any
from utils import *


tests = [
    test(
        """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
    ),
]


def ford(c: str, /) -> int:
    if c == "S":
        return ord("a")
    if c == "E":
        return ord("z")
    return ord(c)


def bfs(grid: Grid, start: str, dest: str) -> int:
    sc = grid.find(start)

    # bfs shortest path to "E"
    q: deque[tuple[Point, int]] = deque([(sc, 0)])
    seen = {sc}
    prev = {}
    while q:
        lc, dist = q.popleft()
        if grid[lc] == dest:
            return dist
        for nc in grid.adj(lc):
            if nc in seen:
                continue
            if ford(grid[lc]) - ford(grid[nc]) <= 1:
                seen.add(nc)
                prev[nc] = lc
                q.append((nc, dist + 1))

    raise ValueError(f"Could not find {dest} from {start}")


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid()
    return bfs(grid, "E", "S")


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    inp = Input(inp.raw.replace("S", "a"))
    grid = inp.into_grid()
    return bfs(grid, "E", "a")
