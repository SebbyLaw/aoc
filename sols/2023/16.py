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


def simulate(inp: Input, starting: Point, start_dir: Point, /) -> int:
    grid = inp.into_grid()
    seen: set[tuple[Point, Point]] = set()
    queue = deque([(starting, start_dir)])

    while queue:
        nxt = queue.popleft()
        if nxt in seen:
            continue
        if nxt[0] not in grid:
            continue
        seen.add(nxt)
        coord, direction = nxt
        match grid[coord]:
            case "\\":
                if direction.row == 0:
                    direction = turn_right(direction)
                else:
                    direction = turn_left(direction)
            case "/":
                if direction.row == 0:
                    direction = turn_left(direction)
                else:
                    direction = turn_right(direction)
            case "|" if direction.row == 0:
                queue.append((coord.up, DELTA_UP))
                queue.append((coord.down, DELTA_DOWN))
                continue
            case "-" if direction.col == 0:
                queue.append((coord.left, DELTA_LEFT))
                queue.append((coord.right, DELTA_RIGHT))
                continue
            case _:
                pass

        queue.append((coord + direction, direction))

    return len(set(c for c, _ in seen))


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return simulate(inp, Point(0, 0), DELTA_RIGHT)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    grid = inp.into_grid()

    return max(
        simulate(inp, coord, direction)
        for coord, direction in (
            *((p, DELTA_DOWN) for p in grid.top_edge()),
            *((p, DELTA_UP) for p in grid.bottom_edge()),
            *((p, DELTA_RIGHT) for p in grid.left_edge()),
            *((p, DELTA_LEFT) for p in grid.right_edge()),
        )
    )
