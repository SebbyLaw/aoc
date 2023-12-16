from collections import defaultdict
import math
from typing import Any
from utils import *


tests = [
    test(
        """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
    ),
]


def ehash(s: str, /) -> int:
    t = 0
    for c in s:
        t += ord(c)
        t *= 17
        t %= 256
    return t


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    return sum(ehash(s) for s in inp.raw.split(","))


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    arr: dict[int, dict[str, int]] = defaultdict(dict)

    for s in inp.raw.split(","):
        if s.endswith("-"):
            b = s[:-1]
            arr[ehash(b)].pop(b, None)
        else:
            b, n = s.split("=")
            arr[ehash(b)][b] = int(n)

    return sum(
        math.prod([i + 1, slot, fl]) for i in range(256) for slot, (_, fl) in enumerate(arr[i].items(), start=1) if fl
    )
