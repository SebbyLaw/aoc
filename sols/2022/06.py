from itertools import count
from typing import Any
from utils import *


tests = [
    test(
        """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    buf = inp.raw.strip()
    for i in count():
        if len(set(buf[i : i + 4])) == 4:
            return i + 4


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    buf = inp.raw.strip()
    for i in count():
        if len(set(buf[i : i + 14])) == 14:
            return i + 14
