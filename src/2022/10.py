from typing import Any
from utils import *


tests = [
    test(
        """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
    ),
]


@runs(
    # *tests,
    submit,
)
def a(inp: Input) -> Any:
    x: int = 1
    c: int = 0
    ns = []

    def tick():
        nonlocal c
        c += 1
        if (c % 40) == 20:
            ns.append(x * c)

    for line in inp.lines:
        instr, *args = line.split()

        match instr:
            case "noop":
                tick()
            case "addx":
                tick()
                tick()
                x += int(args[0])
            case other:
                raise ValueError(f"Unknown instruction: {other}")

    return sum(ns)


@runs(
    # *tests,
    # submit,
)
def b(inp: Input) -> Any:
    x: int = 1
    c: int = 0

    def tick():
        nonlocal c

        if (c % 40) in range(x - 1, x + 2):
            print(LIT_PIXEL, end="")
        else:
            print(DARK_PIXEL, end="")
        if c % 40 == 39:
            print()

        c += 1

    for line in inp.lines:
        instr, *args = line.split()

        match instr:
            case "noop":
                tick()
            case "addx":
                tick()
                tick()
                x += int(args[0])
            case other:
                raise ValueError(f"Unknown instruction: {other}")
