"""Core utilities for Advent of Code."""

from __future__ import annotations

import re
import sys
from typing import Callable, Iterable, SupportsIndex, Type, TypeVar

from .grid import Grid
from .view import StringView


T = TypeVar("T")
U = TypeVar("U")

# :tf:
sys.setrecursionlimit(100000)


__all__ = (
    "DARK_PIXEL",
    "LIT_PIXEL",
    "lmap",
    "lzip",
    "ints",
    "floats",
    "positive_ints",
    "positive_floats",
    "words_alpha",
    "words_alphanum",
    "Input",
    "norm",
)


# region: misc

DARK_PIXEL: str = "\u2588"
LIT_PIXEL: str = "\u2591"

# endregion


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
        self.__raw = raw.rstrip().lstrip("\n")

    def __repr__(self) -> str:
        return self.__raw

    def __str__(self) -> str:
        return self.__raw

    def __hash__(self) -> int:
        return hash(self.__raw)

    def into_grid(self, t: Callable[[str], T] = str, cls: Type[Grid] = Grid) -> Grid[T]:
        return cls([lmap(t, line.strip()) for line in self.lines])

    def split(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[Input]:
        """
        Return a list of the substrings in the string, using sep as the separator string.

        sep
            The separator used to split the string.

            When set to None (the default value), will split on any whitespace character (including \n \r \t \f and spaces) and will discard empty strings from the result.
        maxsplit
            Maximum number of splits (starting from the left). -1 (the default value) means no limit.
        """
        return [Input(part) for part in self.__raw.split(sep, maxsplit)]

    @property
    def view(self) -> StringView:
        return StringView(self.__raw)

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

# region: "vectors"


def norm(scalar: int | float, /) -> int:
    """Return the norm of the given scalar."""
    return int(scalar and scalar // abs(scalar))


# endregion
