# region: grid
from typing import Generic, Iterator, Sequence, TypeVar


__all__ = (
    "Coord",
    "manhattan_distance",
    "chebyshev_distance",
    "euclidean_distance",
    "Grid",
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


type Coord = tuple[int, int]
"""A coordinate in a 2D grid. Tuple of (row, col)."""


def manhattan_distance(coord1: Coord, coord2: Coord, /) -> int:
    """Return the Manhattan distance between two coordinates."""
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def chebyshev_distance(coord1: Coord, coord2: Coord, /) -> int:
    """Return the Chebyshev distance between two coordinates."""
    return max(abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1]))


def euclidean_distance(coord1: Coord, coord2: Coord, /) -> float:
    """Return the Euclidean distance between two coordinates."""
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5


GRID_DELTA: list[Coord] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
"""The four cardinal directions in a 2D grid."""
OCTO_DELTA: list[Coord] = [(1, 1), (-1, -1), (1, -1), (-1, 1)] + GRID_DELTA
"""The eight cardinal and ordinal directions in a 2D grid."""
CHAR_TO_DELTA: dict[str, Coord] = {
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
    "N": (-1, 0),
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1),
}
"""Mapping of common characters to their corresponding delta in a 2D grid."""
DELTA_TO_UDLR: dict[Coord, str] = {
    (0, 1): "R",
    (1, 0): "D",
    (0, -1): "L",
    (-1, 0): "U",
}
"""Mapping of common deltas to their corresponding UDLR character in a 2D grid."""
DELTA_TO_NESW: dict[Coord, str] = {
    (0, 1): "E",
    (1, 0): "S",
    (0, -1): "W",
    (-1, 0): "N",
}
"""Mapping of common deltas to their corresponding Cardinal character in a 2D grid."""


def turn_left(delta: Coord, /) -> Coord:
    """Return the delta after turning left."""
    return (-delta[1], delta[0])


def turn_right(delta: Coord, /) -> Coord:
    """Return the delta after turning right."""
    return (delta[1], -delta[0])


def turn_180(delta: Coord, /) -> Coord:
    """Return the delta after turning 180 degrees."""
    return (-delta[0], -delta[1])


class Grid(Generic[T]):
    """A 2D grid of values."""

    __slots__ = ("grid", "rows", "cols")

    def __init__(self, grid: list[list[T]]):
        self.grid: list[list[T]] = grid
        self.rows: int = len(grid)
        self.cols: int = len(grid[0])

    def find(self, value: T, /) -> Coord:
        """Return the coordinate of the first occurrence of the given value in the grid."""
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == value:
                    return (r, c)
        raise ValueError(f"{value} not found in grid")

    def coords(self) -> list[Coord]:
        """Return a list of all coordinates in the grid."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols)]

    def in_bounds(self, row: int, col: int) -> bool:
        """Return whether the given coordinate is in bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __contains__(self, coords: Coord) -> bool:
        return self.in_bounds(*coords)

    def __getitem__(self, coords: Coord) -> T:
        return self.grid[coords[0]][coords[1]]

    def __setitem__(self, coords: Coord, value: T):
        self.grid[coords[0]][coords[1]] = value

    def adj(self, coord: Coord, /, *, delta: Sequence[Coord] = GRID_DELTA) -> Iterator[Coord]:
        """Return an iterator of all adjacent coordinates."""
        orig_r, orig_c = coord
        for dr, dc in delta:
            adj = (orig_r + dr, orig_c + dc)
            if adj in self:
                yield adj

    def is_edge(self, coord: Coord, /) -> bool:
        """Return whether the given coordinate is on the edge of the grid."""
        return coord[0] in (0, self.rows - 1) or coord[1] in (0, self.cols - 1)

    def to_left(self, coord: Coord, /) -> Iterator[Coord]:
        """Return an iterator of all coordinates to the left of the given coordinate."""
        orig_r, orig_c = coord
        for dc in range(orig_c - 1, -1, -1):
            yield (orig_r, dc)

    def to_right(self, coord: Coord, /) -> Iterator[Coord]:
        """Return an iterator of all coordinates to the right of the given coordinate."""
        orig_r, orig_c = coord
        for dc in range(orig_c + 1, self.cols):
            yield (orig_r, dc)

    def to_up(self, coord: Coord, /) -> Iterator[Coord]:
        """Return an iterator of all coordinates above the given coordinate."""
        orig_r, orig_c = coord
        for dr in range(orig_r - 1, -1, -1):
            yield (dr, orig_c)

    def to_down(self, coord: Coord, /) -> Iterator[Coord]:
        """Return an iterator of all coordinates below the given coordinate."""
        orig_r, orig_c = coord
        for dr in range(orig_r + 1, self.rows):
            yield (dr, orig_c)

    def print(self, sep: str = "", end: str = "\n", /):
        for row in self.grid:
            print(*row, sep=sep, end=end)


# endregion
