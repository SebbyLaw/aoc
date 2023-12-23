from __future__ import annotations
from aoclib import Point
from typing import Generic, Iterator, Sequence, TypeVar


__all__ = (
    "Point",
    "manhattan_distance",
    "chebyshev_distance",
    "euclidean_distance",
    "Grid",
    "DELTA_UP",
    "DELTA_DOWN",
    "DELTA_LEFT",
    "DELTA_RIGHT",
    "DELTA_NORTH",
    "DELTA_SOUTH",
    "DELTA_WEST",
    "DELTA_EAST",
    "GRID_DELTA",
    "OCTO_DELTA",
    "CHAR_TO_DELTA",
    "DELTA_TO_UDLR",
    "DELTA_TO_NESW",
    "turn_left",
    "turn_right",
    "turn_180",
)

T = TypeVar("T")


def manhattan_distance(p1: Point, p2: Point, /) -> int:
    """Return the Manhattan distance between two points."""
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)


def chebyshev_distance(p1: Point, p2: Point, /) -> int:
    """Return the Chebyshev distance between two points."""
    return max(abs(p1.row - p2.row), abs(p1.col - p2.col))


def euclidean_distance(p1: Point, p2: Point, /) -> float:
    """Return the Euclidean distance between two points."""
    return ((p1.row - p2.row) ** 2 + (p1.col - p2.col) ** 2) ** 0.5


DELTA_UP: Point = Point(-1, 0)
DELTA_DOWN: Point = Point(1, 0)
DELTA_LEFT: Point = Point(0, -1)
DELTA_RIGHT: Point = Point(0, 1)
DELTA_NORTH: Point = DELTA_UP
DELTA_SOUTH: Point = DELTA_DOWN
DELTA_WEST: Point = DELTA_LEFT
DELTA_EAST: Point = DELTA_RIGHT

DELTA_NW: Point = DELTA_NORTH + DELTA_WEST
DELTA_NE: Point = DELTA_NORTH + DELTA_EAST
DELTA_SW: Point = DELTA_SOUTH + DELTA_WEST
DELTA_SE: Point = DELTA_SOUTH + DELTA_EAST


GRID_DELTA: list[Point] = [DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT]
"""The four cardinal directions in a 2D grid."""
OCTO_DELTA: list[Point] = GRID_DELTA + [DELTA_NW, DELTA_NE, DELTA_SW, DELTA_SE]
"""The eight cardinal and ordinal directions in a 2D grid."""
CHAR_TO_DELTA: dict[str, Point] = {
    "E": DELTA_EAST,
    "S": DELTA_SOUTH,
    "W": DELTA_WEST,
    "N": DELTA_NORTH,
    "U": DELTA_UP,
    "D": DELTA_DOWN,
    "R": DELTA_RIGHT,
    "L": DELTA_LEFT,
}
"""Mapping of common characters to their corresponding delta in a 2D grid."""
DELTA_TO_UDLR: dict[Point, str] = {
    DELTA_RIGHT: "R",
    DELTA_DOWN: "D",
    DELTA_LEFT: "L",
    DELTA_UP: "U",
}
"""Mapping of common deltas to their corresponding UDLR character in a 2D grid."""
DELTA_TO_NESW: dict[Point, str] = {
    DELTA_EAST: "E",
    DELTA_SOUTH: "S",
    DELTA_WEST: "W",
    DELTA_NORTH: "N",
}
"""Mapping of common deltas to their corresponding Cardinal character in a 2D grid."""


def turn_left(delta: Point, /) -> Point:
    """Return the delta after turning left."""
    return Point(-delta.col, delta.row)


def turn_right(delta: Point, /) -> Point:
    """Return the delta after turning right."""
    return Point(delta.col, -delta.row)


def turn_180(delta: Point, /) -> Point:
    """Return the delta after turning 180 degrees."""
    return Point(-delta.row, -delta.col)


class Grid(Generic[T]):
    """A 2D grid of values."""

    __slots__ = ("data", "points", "rows", "cols")

    def __init__(self, grid: list[list[T]]):
        self.rows: int = len(grid)
        self.cols: int = len(grid[0])

        self.points: list[list[Point]] = []
        self.data: dict[Point, T] = {}

        for r, row in enumerate(grid):
            self.points.append([])
            for c, value in enumerate(row):
                point = Point(r, c)
                self.points[r].append(point)
                self.data[point] = value

    @classmethod
    def of(cls, value: T, cols: int, rows: int, /) -> Grid[T]:
        """Return a grid of the given size filled with the given value.

        value: value to fill the grid with
        cols: number of columns (width or x-axis)
        rows: number of rows (height or y-axis)
        """
        return cls([[value] * cols for _ in range(rows)])

    @property
    def origin(self) -> Point:
        """Return the 'origin' (top left) of the grid."""
        return self.points[0][0]

    @property
    def bottom_left(self) -> Point:
        """Return the 'bottom left' of the grid."""
        return self.points[self.rows - 1][0]

    @property
    def center(self) -> Point:
        """Return the 'center' of the grid."""
        return self.points[self.rows // 2][self.cols // 2]

    @property
    def bottom_right(self) -> Point:
        """Return the 'bottom right' of the grid."""
        return self.points[self.rows - 1][self.cols - 1]

    @property
    def top_right(self) -> Point:
        """Return the 'top right' of the grid."""
        return self.points[0][self.cols - 1]

    @property
    def corners(self) -> tuple[Point, Point, Point, Point]:
        """Return the four corners of the grid."""
        return self.origin, self.top_right, self.bottom_right, self.bottom_left

    def find(self, value: T, /) -> Point:
        """Return the coordinate of the first occurrence of the given value in the grid."""
        for point in self.coords():
            if self[point] == value:
                return point

        raise ValueError(f"{value} not found in grid")

    def coords(self) -> Iterator[Point]:
        """Return a list of all coordinates in the grid."""
        for row in self.points:
            yield from row

    def items(self) -> Iterator[tuple[Point, T]]:
        """Return an iterator of all coordinates and their corresponding values in the grid."""
        for point in self.coords():
            yield point, self[point]

    def values(self) -> Iterator[T]:
        """Return an iterator of all values in the grid."""
        for point in self.coords():
            yield self[point]

    def in_bounds(self, row: int, col: int, /) -> bool:
        """Return whether the given coordinate is in bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __contains__(self, point: Point, /) -> bool:
        return self.in_bounds(point.row, point.col)

    def __getitem__(self, point: Point, /) -> T:
        return self.data[point]

    def __setitem__(self, point: Point, value: T, /):
        self.data[point] = value

    def count(self, value: T, /) -> int:
        """Return the number of times the given value appears in the grid."""
        return sum(1 for v in self.data.values() if v == value)

    def set(self, row: int, col: int, value: T, /):
        """Set the value at the given coordinate."""
        self.data[self.points[row][col]] = value

    def wrap(self, point: Point, /) -> Point:
        """Return the wrapped coordinate of the given coordinate."""
        return self.points[point.row % self.rows][point.col % self.cols]

    def adj(self, point: Point, /, *, delta: Sequence[Point] = GRID_DELTA, wraps: bool = False) -> Iterator[Point]:
        """Return an iterator of all adjacent coordinates."""
        for dt in delta:
            adj = point + dt
            if adj in self:
                yield adj
            elif wraps:
                yield self.wrap(adj)

    def is_edge(self, coord: Point, /) -> bool:
        """Return whether the given coordinate is on the edge of the grid."""
        return coord.row in (0, self.rows - 1) or coord.col in (0, self.cols - 1)

    def is_corner(self, coord: Point, /) -> bool:
        """Return whether the given coordinate is on the corner of the grid."""
        return coord.row in (0, self.rows - 1) and coord.col in (0, self.cols - 1)

    def top_edge(self) -> Iterator[Point]:
        """Return an iterator of all coordinates on the top edge of the grid."""
        yield from self.points[0]

    def bottom_edge(self) -> Iterator[Point]:
        """Return an iterator of all coordinates on the bottom edge of the grid."""
        yield from self.points[-1]

    def left_edge(self) -> Iterator[Point]:
        """Return an iterator of all coordinates on the left edge of the grid."""
        for row in self.points:
            yield row[0]

    def right_edge(self) -> Iterator[Point]:
        """Return an iterator of all coordinates on the right edge of the grid."""
        for row in self.points:
            yield row[-1]

    def to_left(self, point: Point, /) -> Iterator[Point]:
        """Return an iterator of all coordinates to the left of the given coordinate."""
        for dc in range(point.col - 1, -1, -1):
            yield self.points[point.row][dc]

    def to_right(self, point: Point, /) -> Iterator[Point]:
        """Return an iterator of all coordinates to the right of the given coordinate."""
        for dc in range(point.col + 1, self.cols):
            yield self.points[point.row][dc]

    def to_up(self, point: Point, /) -> Iterator[Point]:
        """Return an iterator of all coordinates above the given coordinate."""
        for dr in range(point.row - 1, -1, -1):
            yield self.points[dr][point.col]

    def to_down(self, point: Point, /) -> Iterator[Point]:
        """Return an iterator of all coordinates below the given coordinate."""
        for dr in range(point.row + 1, self.rows):
            yield self.points[dr][point.col]

    def print(self, sep: str = "", end: str = "\n", file=None):
        for row in self.points:
            print(*(self.data[r] for r in row), sep=sep, end=end, file=file)

    def __str__(self) -> str:
        return "\n".join("".join(str(self.data[r]) for r in row) for row in self.points)

    def copy(self) -> Grid[T]:
        """Return a shallow copy of the grid."""
        grid = Grid([[]])
        grid.rows = self.rows
        grid.cols = self.cols
        # we can save a lot of time by not creating new Points
        # since points is supposed to be immutable, don't even bother copying it
        grid.points = self.points
        grid.data = self.data.copy()
        return grid
