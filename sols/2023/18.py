from typing import Any
from utils import *
import shapely


tests = [
    test(
        """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    x = y = 0
    corners: list[tuple[int, int]] = [(0, 0)]
    for line in inp.lines:
        d, n, *_ = line.split()
        delta = CHAR_TO_DELTA[d] * int(n)
        x += delta.col
        y += delta.row
        corners.append((x, y))

    shape = shapely.Polygon(corners)
    return int(shape.area) + int(shape.length / 2) + 1


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    x = y = 0
    dct = [DELTA_RIGHT, DELTA_DOWN, DELTA_LEFT, DELTA_UP]

    def convert(code: str, /) -> Point:
        # (#70c710)
        n = int(code[-2])
        code = code[2:-2]
        dist = int(code, 16)
        return dct[n] * dist

    corners: list[tuple[int, int]] = [(0, 0)]
    for line in inp.lines:
        *_, code = line.split()
        delta = convert(code)
        x += delta.col
        y += delta.row
        corners.append((x, y))

    shape = shapely.Polygon(corners)
    return int(shape.area) + int(shape.length / 2) + 1
