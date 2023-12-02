from collections import Counter
import itertools
from typing import Any
from utils import *


tests = [
    test(
        """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    possible: list[int] = []

    for line in inp.lines:
        game_n = ints(line)[0]
        sets = line.split(":")[-1].split(";")

        for s in sets:
            ccount = Counter()
            colors = s.split(",")
            colors = [c.strip() for c in colors]
            for c in colors:
                n, color = c.split()
                ccount[color] += int(n)

            if ccount["red"] > 12 or ccount["green"] > 13 or ccount["blue"] > 14:
                break
        else:
            possible.append(game_n)

    return sum(possible)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    total = 0

    for line in inp.lines:
        game_n = ints(line)[0]
        sets = line.split(":")[-1].split(";")

        maxes = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        for s in sets:
            ccount = Counter()
            colors = s.split(",")
            colors = [c.strip() for c in colors]
            for c in colors:
                n, color = c.split()
                ccount[color] += int(n)

            for color, count in ccount.items():
                maxes[color] = max(maxes[color], count)

        power = maxes["red"] * maxes["blue"] * maxes["green"]
        print(game_n, power)
        total += power

    return total
