from collections import Counter
from dataclasses import dataclass
import math
from typing import Any, Callable
from utils import *


tests = [
    test(
        """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
    ),
]


@dataclass(slots=True)
class Monkey:
    num: int
    items: list[int]
    op: str
    div_: int
    test: Callable[[int], int]


def parse_monkey(m: str, /):
    monkey, starting, op, testd, iftrue, else_ = m.strip().splitlines()
    num = ints(monkey)[0]
    items = ints(starting)
    op = op.split(":")[1].split("=")[1].strip()
    divisible = ints(testd)[0]
    iftrue = ints(iftrue)[0]
    else_ = ints(else_)[0]

    def fn(x: int, /) -> int:
        if x % divisible == 0:
            return iftrue
        return else_

    return Monkey(num, items, op, divisible, fn)


@runs(
    # *tests,
    submit,
)
def a(inp: Input) -> Any:
    monkeys = lmap(parse_monkey, inp.raw.split("\n\n"))
    throws = Counter()

    for _ in range(20):  # 20 rounds
        for monkey in monkeys:
            for item in monkey.items:
                val = eval(monkey.op, {"old": item}) // 3
                dst = monkey.test(val)
                monkeys[dst].items.append(val)
            throws[monkey.num] += len(monkey.items)
            monkey.items.clear()

    return math.prod(v for _m, v in throws.most_common(2))


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    monkeys = lmap(parse_monkey, inp.raw.split("\n\n"))
    g = math.prod(m.div_ for m in monkeys)
    throws = Counter()

    for _ in range(10000):  # 10000 rounds
        for monkey in monkeys:
            for item in monkey.items:
                val = eval(monkey.op, {"old": item}) % g
                dst = monkey.test(val)
                monkeys[dst].items.append(val)
            throws[monkey.num] += len(monkey.items)
            monkey.items.clear()

    return math.prod(v for _m, v in throws.most_common(2))
