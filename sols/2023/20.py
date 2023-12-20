from collections import deque
from itertools import count
import math
from sys import intern
from typing import Any, Literal
from utils import *


tests = [
    test(
        r"""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
    ),
    test(
        r"""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
    ),
]


LOW = 0
HIGH = 1

type Signal = Literal[0, 1]
type Pulse = tuple[str, Signal]


class Module:
    __slots__ = ("name", "destinations")

    def __init__(self, name: str, destinations: tuple[str, ...], /):
        self.name = name
        self.destinations = destinations

    def pulse(self, Q: deque[tuple[str, Pulse]], v: Pulse, /) -> None:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.destinations=})"


class FlipFlop(Module):
    __slots__ = ("on",)

    def __init__(self, *args):
        super().__init__(*args)
        self.on: bool = False

    def pulse(self, Q: deque[tuple[str, Pulse]], v: Pulse, /) -> None:
        if v[1] is LOW:
            self.on = not self.on
            p = HIGH if self.on else LOW
            for dest in self.destinations:
                Q.append((dest, (self.name, p)))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.on=}, {self.destinations=})"


class Conjunction(Module):
    __slots__ = ("last_recv",)

    def __init__(self, *args):
        super().__init__(*args)
        self.last_recv: dict[str, Signal] = {}

    def pulse(self, Q: deque[tuple[str, Pulse]], v: Pulse, /) -> None:
        src, value = v
        self.last_recv[src] = value
        for val in self.last_recv.values():
            if val == LOW:
                p = HIGH
                break
        else:
            p = LOW

        for dest in self.destinations:
            Q.append((dest, (self.name, p)))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.last_recv=}, {self.destinations=})"


class Broadcaster(Module):
    def pulse(self, Q: deque[tuple[str, Pulse]], v: Pulse, /) -> None:
        for dest in self.destinations:
            Q.append((dest, (self.name, v[1])))


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    mods: dict[str, Module] = {}

    for line in inp.lines:
        lhs, rhs = line.split(" -> ")
        name = intern(lhs[1:].strip())
        destinations = tuple(intern(s) for s in rhs.split(", "))
        if line.startswith("%"):
            mods[name] = FlipFlop(name, destinations)
        elif line.startswith("&"):
            mods[name] = Conjunction(name, destinations)
        else:
            # broadcaster
            mods["broadcaster"] = Broadcaster("broadcaster", destinations)

    to_add: set[str] = set()
    for mname, mod in mods.items():
        for dst in mod.destinations:
            try:
                dest = mods[dst]
            except KeyError:
                to_add.add(dst)
            else:
                if isinstance(dest, Conjunction):
                    dest.last_recv[mname] = LOW

    for name in to_add:
        mods[name] = Module(name, ())

    lowp = 0
    highp = 0

    bc = mods["broadcaster"]
    q = deque()
    for _ in range(1000):
        bc.pulse(q, ("button", LOW))
        lowp += 1
        while q:
            name, p = q.popleft()
            mods[name].pulse(q, p)
            if p[1] is LOW:
                lowp += 1
            else:
                highp += 1

    return lowp * highp


@runs(
    # tests will never finish
    # *tests,
    submit,
)
def b(inp: Input) -> Any:
    mods: dict[str, Module] = {}

    for line in inp.lines:
        lhs, rhs = line.split(" -> ")
        name = intern(lhs[1:].strip())
        destinations = tuple(intern(s) for s in rhs.split(", "))
        if line.startswith("%"):
            mods[name] = FlipFlop(name, destinations)
        elif line.startswith("&"):
            mods[name] = Conjunction(name, destinations)
        else:
            # broadcaster
            mods["broadcaster"] = Broadcaster("broadcaster", destinations)

    to_add: set[str] = set()
    for mname, mod in mods.items():
        for dst in mod.destinations:
            try:
                dest = mods[dst]
            except KeyError:
                to_add.add(dst)
            else:
                if isinstance(dest, Conjunction):
                    dest.last_recv[mname] = LOW

    for name in to_add:
        mods[name] = Module(name, ())

    bc = mods["broadcaster"]
    q: deque[tuple[str, Pulse]] = deque()
    rxgpvals = []
    for step in count(1):
        bc.pulse(q, ("button", LOW))
        while q:
            name, p = q.popleft()
            mods[name].pulse(q, p)
            if name == "zh" and p[1] is HIGH:
                rxgpvals.append(step)
                print(p[0], step)
                if len(rxgpvals) == 4:
                    return math.lcm(*rxgpvals)
