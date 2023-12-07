from collections import Counter
from typing import Any

from utils import *


tests = [
    test(
        """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    ),
]


def score_hand(hand: str, /) -> int:
    match [b for _, b in Counter(hand).most_common()]:
        case 5, *_:
            return 7
        case 4, *_:
            return 6
        case 3, 2, *_:
            return 5
        case 3, *_:
            return 4
        case 2, 2, *_:
            return 3
        case 2, *_:
            return 2
        case _:
            return 1


@runs(
    # *tests,
    # submit,
)
def a(inp: Input) -> Any:
    hands = []
    for line in inp.lines:
        hand, bid = line.split()
        bid = int(bid)
        hands.append((hand, bid))

    def hk(hand: str, /) -> int:
        k = score_hand(hand) * 13**6
        for i, c in enumerate(reversed(hand)):
            k += "23456789TJQKA".index(c) * (13**i)
        return k

    hands.sort(key=lambda h: hk(h[0]))
    return sum((r * bid for r, (_h, bid) in enumerate(hands, start=1)))


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    hands = []
    for line in inp.lines:
        hand, bid = line.split()
        bid = int(bid)
        hands.append((hand, bid))

    def hk(hand: str, /) -> int:
        ch = Counter(hand)
        ch.pop("J", None)
        try:
            repl = ch.most_common(1)[0][0]
        except IndexError:
            repl = "A"
        k = score_hand(hand.replace("J", repl)) * 13**6
        for i, c in enumerate(reversed(hand)):
            k += "J23456789TQKA".index(c) * (13**i)
        return k

    hands.sort(key=lambda h: hk(h[0]))
    return sum((r * bid for r, (_h, bid) in enumerate(hands, start=1)))
