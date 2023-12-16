from collections import deque
from typing import Any
from utils import *


tests = [
    test(
        r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
    ),
]


def simulate(inp: Input, starting: Coord, start_dir: Coord, /) -> int:
    grid = inp.into_grid()
    seen: set[tuple[Coord, Coord]] = set()
    queue = deque([(starting, start_dir)])

    while queue:
        nxt = queue.popleft()
        if nxt in seen:
            continue
        seen.add(nxt)
        coord, direction = nxt
        dirs = []
        match grid[coord]:
            case "\\":
                if direction[0] == 0:
                    dirs.append(turn_right(direction))
                else:
                    dirs.append(turn_left(direction))
            case "/":
                if direction[0] == 0:
                    dirs.append(turn_left(direction))
                else:
                    dirs.append(turn_right(direction))
            case "|" if direction[0] == 0:
                dirs.append((1, 0))
                dirs.append((-1, 0))
            case "-" if direction[1] == 0:
                dirs.append((0, 1))
                dirs.append((0, -1))
            case _:
                dirs.append(direction)

        for nd in dirs:
            node = (coord[0] + nd[0], coord[1] + nd[1])
            if node in grid:
                queue.append((node, nd))

    return len(set(c for c, _ in seen))


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return simulate(inp, (0, 0), (0, 1))


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = inp.into_grid()

    return max(
        simulate(inp, coord, direction)
        for coord, direction in (
            *(((0, x), (1, 0)) for x in range(0, grid.cols)),
            *(((grid.rows - 1, x), (-1, 0)) for x in range(0, grid.cols)),
            *(((y, 0), (0, 1)) for y in range(0, grid.rows)),
            *(((y, grid.cols - 1), (0, -1)) for y in range(0, grid.rows)),
        )
    )
