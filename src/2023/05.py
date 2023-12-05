from itertools import batched
from typing import Any
from utils import *


tests = [
    test(
        """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    chunks = inp.raw.split("\n\n")
    seeds = ints(chunks.pop(0))
    maps: dict[str, dict[range, range]] = {}

    for chunk in chunks:
        lines = chunk.splitlines()
        name = lines.pop(0).split(" ")[0]
        maps[name] = m = {}
        for line in lines:
            dest, src, length = ints(line)
            m[range(src, src + length)] = range(dest, dest + length)

    minloc = 126783432158674  # lol

    for seed in seeds:
        val = seed
        for m in [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]:
            for r in maps[m]:
                if val in r:
                    val = maps[m][r].start + (val - r.start)
                    break
        if val < minloc:
            minloc = val

    return minloc


@runs(
    # *tests,
    submit,
)
def b(inp: Input) -> Any:
    chunks = inp.raw.split("\n\n")
    seeds = ints(chunks.pop(0))

    seedranges = [range(a, a + b) for a, b in batched(seeds, 2)]
    maps: dict[str, dict[range, range]] = {}

    for chunk in chunks:
        lines = chunk.splitlines()
        name = lines.pop(0).split(" ")[0]
        maps[name] = m = {}
        for line in lines:
            dest, src, length = ints(line)
            m[range(src, src + length)] = range(dest, dest + length)

    # reverse of each map
    for m in maps:
        maps[m] = {v: k for k, v in maps[m].items()}

    # solution is slow, idc
    def seedloc(seed: int, /) -> int:
        val = seed
        for m in [
            "humidity-to-location",
            "temperature-to-humidity",
            "light-to-temperature",
            "water-to-light",
            "fertilizer-to-water",
            "soil-to-fertilizer",
            "seed-to-soil",
        ]:
            for r in maps[m]:
                if val in r:
                    val = maps[m][r].start + (val - r.start)
                    break

        return val

    # start at the smallest possible seed location and keep going until we find one that maps to an input seed
    for lr in sorted(maps["humidity-to-location"], key=lambda r: r.start):
        for i in lr:
            sd = seedloc(i)
            if any(sd in r for r in seedranges):
                return i
