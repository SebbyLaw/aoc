from collections import deque
from typing import Any
from utils import *


tests = [
    test(
        """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    ),
]


#
# The pipes are arranged in a two-dimensional grid of tiles:
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


def bfs(grid: Grid[str], start: Coord, /) -> dict[Coord, int]:
    dist = {start: 0}
    seen = set()
    queue = deque([start])

    while queue:
        coord = queue.popleft()
        seen.add(coord)

        match grid[coord]:
            case "S":
                deltas = ""
                up = (coord[0] - 1, coord[1])
                down = (coord[0] + 1, coord[1])
                left = (coord[0], coord[1] - 1)
                right = (coord[0], coord[1] + 1)
                if up in grid and grid[up] in "|7F":
                    deltas += "U"
                if down in grid and grid[down] in "|LJ":
                    deltas += "D"
                if left in grid and grid[left] in "-LF":
                    deltas += "L"
                if right in grid and grid[right] in "-J7":
                    deltas += "R"
            case "|":
                deltas = "UD"
            case "-":
                deltas = "LR"
            case "L":
                deltas = "UR"
            case "J":
                deltas = "UL"
            case "7":
                deltas = "DL"
            case "F":
                deltas = "DR"
            case ".":
                continue
            case _:
                assert False, "What"

        for adj in grid.adj(coord, delta=[CHAR_TO_DELTA[d] for d in deltas]):
            if grid[adj] == ".":
                continue
            if adj not in seen:
                dist[adj] = dist[coord] + 1
                queue.append(adj)

    return dist


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid()
    start = grid.find("S")
    dists = bfs(grid, start)
    return max(dists.values())


# fmt: off
@runs(
#     test(
#         """
# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# """
#     ),
    submit,
)
# fmt: on
def b(inp: Input) -> Any:
    # lol
    # add padding of "." all around the input
    g = [list(line.strip() + ".") for line in inp.raw.splitlines()]
    g.append(["."] * len(g[0]))
    g.insert(0, ["."] * len(g[0]))

    # replace S with its real shape
    grid = Grid(g)
    start = grid.find("S")
    # uncomment for examples lol lmao
    # grid[start] = "F"
    # grid[start] = "7"
    grid[start] = "-"

    # bfs from S to find the loop (assume only pipes found are in the loop)
    loop = bfs(grid, start)
    for coord in grid.coords():
        if coord not in loop:
            grid[coord] = "."

    # make it a string
    raw = "\n".join("".join(row) for row in g)

    # thanks oliver
    expand = {
        ".": ["...", "...", "..."],
        "|": [".#.", ".#.", ".#."],
        "-": ["...", "###", "..."],
        "L": [".#.", ".##", "..."],
        "J": [".#.", "##.", "..."],
        "7": ["...", "##.", ".#."],
        "F": ["...", ".##", ".#."],
    }

    expanded = ""
    for line in raw.splitlines():
        for i in range(3):
            expanded += "".join(expand[c][i] for c in line) + "\n"

    egrid = Grid([list(line.strip()) for line in expanded.strip().splitlines()])
    seen: set[Coord] = set()
    queue: deque[Coord] = deque([(0, 0)])
    while queue:
        coord = queue.popleft()
        if coord in seen:
            continue

        seen.add(coord)

        for adj in egrid.adj(coord):
            if egrid[adj] == "." and adj not in seen:
                queue.append(adj)

    total = 0
    for cr in egrid.coords():
        if cr[0] % 3 != 1 or cr[1] % 3 != 1:
            continue
        if egrid[cr] == "#":
            continue
        if cr in seen:  # outside
            continue

        total += 1

    return total
