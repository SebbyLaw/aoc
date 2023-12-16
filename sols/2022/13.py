from __future__ import annotations
from functools import cmp_to_key
from typing import Any, Union
from utils import *


tests = [
    test(
        """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
    ),
]

PI = Union[int, list[Union["P", int]], list[int], "P"]
P = list[PI]


def cmp(left: PI, right: PI, /) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, list) and isinstance(right, list):
        for idx in range(max(len(left), len(right))):
            try:
                litem = left[idx]
            except IndexError:
                return True
            try:
                ritem = right[idx]
            except IndexError:
                return False

            check = cmp(litem, ritem)
            if check is None:
                continue
            else:
                return check
        else:
            return None
    else:
        # one is list, the other is int
        if isinstance(left, int):
            return cmp([left], right)
        else:
            return cmp(left, [right])


@runs(
    # *tests,
    submit,
)
def a(inp: Input) -> Any:
    pairs = inp.raw.split("\n\n")

    packets: list[P] = []
    for p in pairs:
        packets.append(lmap(eval, p.split("\n")))

    ordered = []
    for idx, (left, right) in enumerate(packets, start=1):
        if cmp(left, right):
            ordered.append(idx)

    return sum(ordered)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    lines = inp.raw.replace("\n\n", "\n").splitlines()
    packets = lmap(eval, lines) + [[[2]], [[6]]]

    def key(left, right):
        chk = cmp(left, right)
        if chk is None:
            raise Exception("Cannot compare")
        return 1 if not chk else -1

    packets.sort(key=cmp_to_key(key))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
