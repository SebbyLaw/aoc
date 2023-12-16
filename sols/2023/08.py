from itertools import batched, cycle
import math
from typing import Any
from utils import *


tests = [
    test(
        """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    insts, *nodes = inp.words_alpha

    nmap: dict[str, tuple[str, str]] = {node: (left, right) for node, left, right in batched(nodes, 3)}
    curr = nmap["AAA"]
    for step, inst in enumerate(cycle(insts), start=1):
        k = curr["LR".index(inst)]
        curr = nmap[k]

        if k == "ZZZ":
            return step


@runs(
    test(
        """
LR
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    ),
    submit,
)
def b(inp: Input) -> Any:
    insts, *nodes = inp.words_alphanum

    nmap: dict[str, tuple[str, str]] = {node: (left, right) for node, left, right in batched(nodes, 3)}
    starts = [nmap[k] for k in nmap if k.endswith("A")]
    steps: list[int] = []
    for start in starts:
        curr = start
        for step, inst in enumerate(cycle(insts), start=1):
            k = curr["LR".index(inst)]
            curr = nmap[k]

            if k.endswith("Z"):
                steps.append(step)
                break

    return math.lcm(*steps)
