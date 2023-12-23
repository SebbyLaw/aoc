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

    graph = {}
    for point in grid.coords():
        match grid[point]:
            case "#":
                continue
            case ".":
                graph[point] = {adj: 1 for adj in grid.adj(point) if grid[adj] != "#"}
            case "^":
                graph[point] = {point.up: 1}
            case "v":
                graph[point] = {point.down: 1}
            case "<":
                graph[point] = {point.left: 1}
            case ">":
                graph[point] = {point.right: 1}
            case _:
                assert False, "what"

    for node in list(graph.keys()):
        neighbors = graph[node]
        if len(neighbors) == 2:
            left, right = neighbors.keys()
            graph[left].pop(node, None)
            graph[right].pop(node, None)
            graph[left][right] = graph[right][left] = neighbors[left] + neighbors[right]
            del graph[node]

    max_path_len = 0
    stack: list[tuple[int, Point, set[Point]]] = [(0, start, set())]
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
    stack: list[tuple[int, Point, set[Point]]] = [(0, start, set())]
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
