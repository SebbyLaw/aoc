import collections
from typing import Any
from utils import *


tests = [
    test(
        """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    total = 0
    for line in inp.lines:
        points = 0
        winning, have = lmap(ints, line.split(":")[-1].split("|"))
        for _card in set(winning).intersection(have):
            if points == 0:
                points = 1
            else:
                points *= 2

        total += points

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    cards: dict[int, int] = {}

    for line in inp.lines:
        card, nums = line.split(":")
        winning, have = lmap(ints, nums.split("|"))
        card_number = ints(card)[0]
        cards[card_number] = len(set(winning).intersection(have))

    counts = collections.Counter(cards.keys())

    for card, wins in cards.items():
        copies = [card + i for i in range(1, wins + 1)]
        for copy in copies:
            counts[copy] += counts[card]

    return sum(counts.values())
