from functools import cache
from itertools import batched
from typing import Any
from utils import *


tests = [
    test(
        """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
    ),
]


@cache
def priority(s: str, /) -> int:
    if s.lower() == s:
        return ord(s) - ord("a") + 1
    else:
        return ord(s) - ord("A") + 27


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    total = 0
    for line in inp.lines:
        first, second = line[: len(line) // 2], line[len(line) // 2 :]
        total += sum(set(map(priority, first)) & set(map(priority, second)))

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    total = 0
    for first, second, third in batched(inp.lines, 3):
        total += sum(set(map(priority, first)) & set(map(priority, second)) & set(map(priority, third)))

    return total
