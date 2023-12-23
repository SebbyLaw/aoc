from typing import Any
from utils import *


tests = [
    test(
        """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    grid = inp.into_grid()
    start = grid.points[0][1]
    goal = grid.points[-1][-2]
    stack: list[tuple[int, Point, set[Point]]] = [(0, start, set())]

    max_path_len = -1
    while stack:
        dist, curr, path = stack.pop()
        if curr == goal:
            if dist < max_path_len:
                max_path_len = dist
            continue
        if curr in path:
            continue

        match grid[curr]:
            case ".":
                for adj in grid.adj(curr):
                    if grid[adj] in ".^v<>" and adj not in path:
                        stack.append((dist - 1, adj, path | {curr}))
                continue
            case "^":
                # must go up
                adj = curr.up
            case "v":
                # must go down
                adj = curr.down
            case "<":
                # must go left
                adj = curr.left
            case ">":
                # must go right
                adj = curr.right
            case _:
                assert False, "what"

        if grid[adj] == "." and adj not in path:
            stack.append((dist - 1, adj, path | {curr}))

    return -max_path_len


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = inp.into_grid()
    start = grid.points[0][1]
    goal = grid.points[-1][-2]

    graph = {}
    for point in grid.coords():
        if grid[point] != "#":
            graph[point] = {adj: 1 for adj in grid.adj(point) if grid[adj] != "#"}

    for node in list(graph.keys()):
        neighbors = graph[node]
        if len(neighbors) == 2:
            left, right = neighbors.keys()
            del graph[left][node]
            del graph[right][node]
            graph[left][right] = graph[right][left] = neighbors[left] + neighbors[right]
            del graph[node]

    max_path_len = 0
    stack = [(0, start, set())]
    while stack:
        dist, curr, path = stack.pop()
        if curr == goal:
            if dist > max_path_len:
                print("new longest path", dist)
                max_path_len = dist
            continue

        for adj in graph[curr]:
            if adj not in path:
                stack.append((dist + graph[curr][adj], adj, path | {curr}))

    assert max_path_len, "no path found"
    return max_path_len
