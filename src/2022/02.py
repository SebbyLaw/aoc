from typing import Any
from utils import *


tests = [
    test(
        """
A Y
B X
C Z
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    # rock = 1, paper = 2, scissors = 3
    RPSMAP = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    total = 0
    for line in inp.lines:
        opp, mine = line.split()
        opp = RPSMAP[opp]
        mine = RPSMAP[mine]

        if opp == mine:
            total += 3
        elif (mine - opp) % 3 == 1:
            # win
            total += 6

        total += mine

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    # rock = 1, paper = 2, scissors = 3
    RPSMAP = {"A": 1, "B": 2, "C": 3}
    total = 0
    for line in inp.lines:
        opp, res = line.split()
        opp = RPSMAP[opp]

        if res == "X":  # lose
            mine = (opp - 1) % 3
            if mine == 0:
                mine = 3
            total += mine
        elif res == "Y":  # tie
            mine = opp
            total += 3 + mine
        else:  # win
            mine = (opp + 1) % 3
            if mine == 0:
                mine = 3
            total += 6 + mine

    return total
