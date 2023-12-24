from dataclasses import dataclass
import itertools
from typing import Any
from utils import *
from z3 import Solver, Int, IntNumRef

tests = [
    test(
        """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
    ),
]


@dataclass(slots=True, frozen=True)
class Stone:
    x: int
    y: int
    dx: int
    dy: int


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    stones: list[Stone] = []
    for line in inp.lines:
        x, y, _z, dx, dy, _dz = ints(line)
        stones.append(Stone(x, y, dx, dy))

    #
    def line_intersection(a: Stone, b: Stone, /) -> bool:
        ax1, ay1 = a.x, a.y
        ax2, ay2 = a.x + a.dx, a.y + a.dy
        bx1, by1 = b.x, b.y
        bx2, by2 = b.x + b.dx, b.y + b.dy

        xdiff = (ax1 - ax2, bx1 - bx2)
        ydiff = (ay1 - ay2, by1 - by2)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return False

        d = (det((ax1, ay1), (ax2, ay2)), det((bx1, by1), (bx2, by2)))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        if (a.dx > 0 and x < a.x) or (a.dx < 0 and x > a.x) or (a.dy > 0 and y < a.y) or (a.dy < 0 and y > a.y):
            return False
        if (b.dx > 0 and x < b.x) or (b.dx < 0 and x > b.x) or (b.dy > 0 and y < b.y) or (b.dy < 0 and y > b.y):
            return False
        # test input
        # if x < 7 or y > 27:
        #     return False
        if not (200000000000000 <= x <= 400000000000000):
            return False
        if not (200000000000000 <= y <= 400000000000000):
            return False
        return True

    return sum(
        1
        for combination in itertools.combinations(stones, 2)
        if combination[0] != combination[1] and line_intersection(*combination)
    )


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    fx, fy, fz = Int("fx"), Int("fy"), Int("fz")
    fdx, fdy, fdz = Int("fdx"), Int("fdy"), Int("fdz")

    solver = Solver()
    for idx, line in enumerate(inp.lines, 1):
        t = Int(f"t{idx}")
        x, y, z, dx, dy, dz = ints(line)
        solver.add(t >= 0)
        solver.add(x + dx * t == fx + fdx * t)
        solver.add(y + dy * t == fy + fdy * t)
        solver.add(z + dz * t == fz + fdz * t)

    solver.check()
    solved: IntNumRef = solver.model().eval(fx + fy + fz)  # type: ignore
    return solved.as_long()
