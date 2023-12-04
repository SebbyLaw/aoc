from typing import Any
from utils import *


tests = [
    test(
        """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    ),
]


def parse_cargo(cargo_string: str) -> list[list[str]]:
    lines = cargo_string.splitlines()
    cargo = [[] for _ in lines.pop().split()]

    for line in reversed(lines):
        view = StringView(line.rstrip())
        for i in range(len(cargo)):
            view.get()  # [
            crate = view.get()  # crate
            view.read(2)  # ] and space
            if crate and crate != " ":
                cargo[i].append(crate)

    return cargo


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    c, m = inp.split("\n\n")
    cargo = parse_cargo(c.raw)
    cargo.insert(0, [])  # cargo is 1-indexed lol

    for move in m.lines:
        num, src, dest = ints(move)
        for _ in range(num):
            cargo[dest].append(cargo[src].pop())

    return "".join(t.pop() for t in cargo[1:])


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    c, m = inp.split("\n\n")
    cargo = parse_cargo(c.raw)
    cargo.insert(0, [])  # cargo is 1-indexed lol

    for move in m.lines:
        num, src, dest = ints(move)
        moving = cargo[src][-num:]
        cargo[src] = cargo[src][:-num]
        cargo[dest].extend(moving)

    return "".join(t.pop() for t in cargo[1:])
