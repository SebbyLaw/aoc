from collections import deque
from dataclasses import dataclass
import math
import re
from typing import Any, Literal
from utils import *


tests = [
    test(
        """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
    ),
]


@dataclass(slots=True, frozen=True)
class Part:
    x: int  # x
    m: int  # m
    a: int  # a
    s: int  # s

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass(slots=True, frozen=True)
class Condition:
    attr: str
    op: Literal[">", "<"]
    val: int
    res: Literal["A", "R"] | str


@dataclass(slots=True, frozen=True)
class Workflow:
    name: str
    conditions: list[Condition]
    default: Literal["A", "R"] | str

    def check(self, part: Part, /) -> str:
        for c in self.conditions:
            if c.op == ">" and getattr(part, c.attr) > c.val or c.op == "<" and getattr(part, c.attr) < c.val:
                return c.res
        else:
            return self.default


def make_workflows(inp: Input, /) -> dict[str, Workflow]:
    workflows: dict[str, Workflow] = {}

    for line in inp.lines:
        name, _, conditions = line.rstrip("}").partition("{")

        conditions = conditions.split(",")
        cmps: list[tuple[str, Literal[">", "<"], int, str]] = []
        for c in conditions[:-1]:
            cmp, res = c.split(":")
            attr, op, val = re.fullmatch(r"([a-z])([<>])(\d+)", cmp).groups()  # type: ignore
            cmps.append((attr, op, int(val), res))  # type: ignore

        default = conditions[-1]
        workflows[name] = Workflow(
            name,
            [Condition(attr, op, val, res) for attr, op, val, res in cmps],
            default,
        )

    return workflows


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    rworkflows, rparts = inp.split("\n\n")
    parts = [Part(*ints(line)) for line in rparts.lines]
    workflows = make_workflows(rworkflows)

    accepted: int = 0
    for part in parts:
        wf = "in"
        while True:
            res = workflows[wf].check(part)
            if res == "A":
                accepted += part.value
                break
            elif res == "R":
                break
            wf = res

    return accepted


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    rworkflows, _ = inp.split("\n\n")
    workflows = make_workflows(rworkflows)
    unknown: deque[tuple[str, list[orange]]] = deque(
        [("in", [orange(1, 4001), orange(1, 4001), orange(1, 4001), orange(1, 4001)])]
    )

    accepted: int = 0

    while unknown:
        wf, oranges = unknown.popleft()
        workflow = workflows[wf]
        for condition in workflow.conditions:
            idx = "xmas".index(condition.attr)
            this = oranges[idx]
            if condition.op == ">":
                other = orange(condition.val + 1, 4001)
            else:
                other = orange(1, condition.val)

            acc = this & other
            diff = this - other

            pcp = oranges.copy()
            pcp[idx] = acc

            match condition.res:
                case "A":
                    accepted += math.prod(map(len, pcp))
                case "R":
                    pass
                case nwf:
                    unknown.append((nwf, pcp))

            if diff:  # the diff can only be zero or one orange
                oranges[idx] = diff[0]
            else:
                break
        else:
            match workflow.default:
                case "A":
                    accepted += math.prod(map(len, oranges))
                case "R":
                    pass
                case nwf:
                    unknown.append((nwf, oranges))

    return accepted
