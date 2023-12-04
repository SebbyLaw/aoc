"""Core utilities for Advent of Code."""

from __future__ import annotations

import re
import sys
from typing import Callable, Generic, Iterable, Iterator, Sequence, TypeAlias, TypeVar


T = TypeVar("T")
U = TypeVar("U")

# :tf:
sys.setrecursionlimit(100000)


__all__ = (
    "lmap",
    "lzip",
    "ints",
    "floats",
    "positive_ints",
    "positive_floats",
    "words_alpha",
    "words_alphanum",
    "Input",
    "Coord",
    "Grid",
    "GRID_DELTA",
    "OCTO_DELTA",
    "CHAR_TO_DELTA",
    "DELTA_TO_UDLR",
    "DELTA_TO_NESW",
    "turn_left",
    "turn_right",
    "turn_180",
    "NumberT",
    "Vec",
    "LVec",
    "vadd",
    "vneg",
    "vsub",
    "vmul",
    "vdiv",
    "vdot",
)


def lmap(func: Callable[[T], U], /, *iterables: Iterable[T]) -> list[U]:
    return list(map(func, *iterables))


def lzip(*iterables: Iterable[T]) -> list[tuple[T, ...]]:
    return list(zip(*iterables))


# region: input/parsing
def ints(s: str, /) -> list[int]:
    """Return a list of integers in the given string."""
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))


def floats(s: str, /) -> list[float]:
    """Return a list of floats in the given string."""
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_ints(s: str, /) -> list[int]:
    """Return a list of positive integers in the given string."""
    return lmap(int, re.findall(r"\d+", s))


def positive_floats(s: str, /) -> list[float]:
    """Return a list of positive floats in the given string."""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words_alpha(s: str, /) -> list[str]:
    """Return a list of regex-matched words in the given string. Matches only alphabetic characters."""
    return re.findall(r"[A-Za-z]+", s)


def words_alphanum(s: str, /) -> list[str]:
    """Return a list of regex-matched words in the given string. Matches alphanumeric characters and underscores."""
    return re.findall(r"\w+", s)


class Input:
    __slots__ = ("__raw",)

    def __init__(self, raw: str, /):
        self.__raw = raw.strip()

    def __repr__(self) -> str:
        return self.__raw

    def __str__(self) -> str:
        return self.__raw

    def __hash__(self) -> int:
        return hash(self.__raw)

    def into_grid(self, t: Callable[[str], T] = str) -> Grid[T]:
        return Grid([lmap(t, line.strip()) for line in self.lines])

    @property
    def raw(self) -> str:
        """Return the raw input."""
        return self.__raw

    @property
    def lines(self) -> list[str]:
        """Return a list of lines in the input."""
        return self.__raw.splitlines()

    @property
    def words_alpha(self) -> list[str]:
        """Return a list of regex-matched words in the input. Matches only alphabetic characters."""
        return words_alpha(self.__raw)

    @property
    def words_alphanum(self) -> list[str]:
        """Return a list of regex-matched words in the input. Matches alphanumeric characters and underscores."""
        return words_alphanum(self.__raw)

    @property
    def ints(self) -> list[int]:
        """Return a list of regex-matched integers in the input."""
        return ints(self.__raw)

    @property
    def floats(self) -> list[float]:
        """Return a list of regex-matched floats in the input."""
        return floats(self.__raw)

    @property
    def positive_ints(self) -> list[int]:
        """Return a list of regex-matched positive integers in the input."""
        return positive_ints(self.__raw)

    @property
    def positive_floats(self) -> list[float]:
        """Return a list of regex-matched positive floats in the input."""
        return positive_floats(self.__raw)


# endregion

# region: grid
Coord: TypeAlias = tuple[int, int]
"""A coordinate in a 2D grid. Tuple of (row, col)."""


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

    def print(self, sep: str = "", end: str = "\n", /):
        for row in self.grid:
            print(*row, sep=sep, end=end)


# endregion

# region: "vectors"

NumberT: TypeAlias = int | float | complex
Vec: TypeAlias = Iterable[NumberT]
LVec: TypeAlias = list[NumberT]


def vadd(*vecs) -> LVec:
    return list(map(sum, zip(*vecs)))


def vneg(vec: Vec, /) -> LVec:
    return [-x for x in vec]


def vsub(vec1: Vec, vec2: Vec, /) -> LVec:
    return [x - y for x, y in zip(vec1, vec2)]


def vmul(vec: Vec, scalar: NumberT, /) -> LVec:
    return [x * scalar for x in vec]


def vdiv(vec: Vec, scalar: NumberT, /) -> LVec:
    return [x / scalar for x in vec]


def vdot(vec1: Vec, vec2: Vec, /) -> NumberT:
    return sum(x * y for x, y in zip(vec1, vec2))


# endregion
