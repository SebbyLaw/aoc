from typing import Any
from utils import *


tests = [
    test(
        """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    lines = lmap(ints, inp.lines)
    diffs: list[list[list[int]]] = []
    for line in lines:
        ld: list[list[int]] = [line]
        while any(line):
            ld.append([line[i + 1] - line[i] for i in range(len(line) - 1)])
            line = ld[-1]
        diffs.append(ld)

    for line in diffs:
        line[-1].append(0)
        line.reverse()
        for k, row in enumerate(line[1:]):
            row.append(row[-1] + line[k][-1])

    return sum(diff[-1][-1] for diff in diffs)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    lines = lmap(ints, inp.lines)
    diffs: list[list[list[int]]] = []
    for line in lines:
        ld: list[list[int]] = [line]
        while any(line):
            ld.append([line[i + 1] - line[i] for i in range(len(line) - 1)])
            line = ld[-1]
        diffs.append(ld)

    for line in diffs:
        line[-1].append(0)
        line.reverse()
        for k, row in enumerate(line[1:]):
            row.insert(0, row[0] - line[k][0])

    return sum(diff[-1][0] for diff in diffs)
