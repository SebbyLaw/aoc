import functools
from typing import Any, Literal
from utils import *


tests = [
    test(
        """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    ),
]


@functools.cache
def check(springs: str, needed: tuple[int, ...], curr: int, /) -> int:
    # springs: string
    # needed: tuple of ints needed
    # curr: current group length or None if not in a group
    if not springs:  # end of string
        match curr, len(needed):
            case 0, 0:  # no current group and no more groups needed, this is valid
                return 1
            case n, 1 if n == needed[0]:  # current group done consuming and is the last needed group, this is valid
                return 1
            case _:
                return 0  # anything else is invalid

    consume: Literal["?", ".", "#"] = springs[0]  # pyright: ignore [reportGeneralTypeIssues]
    rest: str = springs[1:]

    if curr:
        if curr == needed[0] and consume in "?.":
            # terminate the current group
            return check(rest.lstrip("."), needed[1:], 0)
        elif consume in "?#":
            # keep consuming the current group
            return check(rest, needed, curr + 1)
    else:
        match consume:  # pyright: ignore [reportMatchNotExhaustive]
            case "?":
                if not needed:
                    return "#" not in rest
                return check(rest, needed, 1) + check(rest.lstrip("."), needed, 0)
            case ".":  # keep going
                return check(rest.lstrip("."), needed, 0)
            case "#" if needed:
                return check(rest, needed, 1)
    return 0


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    total = 0
    for line in inp.lines:
        springs, needed = line.split()
        needed = tuple(map(int, needed.split(",")))
        total += check(springs, needed, 0)

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    total = 0
    for line in inp.lines:
        springs, needed = line.split()
        springs = "?".join([springs] * 5)
        needed = tuple(map(int, needed.split(","))) * 5
        total += check(springs, needed, None)

    return total
