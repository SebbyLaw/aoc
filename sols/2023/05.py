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
    seeds: list[int] = ints(chunks[0])
    maps: list[list[tuple[orange, int]]] = []

    for chunk in chunks[1:]:
        m = []
        maps.append(m)
        for line in chunk.splitlines()[1:]:
            dest, src, length = ints(line)
            m.append((orange(src, src + length), dest - src))

    def apply_maps(seed: int, /) -> int:
        for m in maps:
            for rng, dt in m:
                if seed in rng:
                    seed += dt
                    break
        return seed

    return min(apply_maps(seed) for seed in seeds)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    chunks = inp.raw.split("\n\n")
    seeds = [orange(a, a + b) for a, b in batched(ints(chunks[0]), 2)]
    maps: list[list[tuple[orange, int]]] = []

    for chunk in chunks[1:]:
        m = []
        maps.append(m)
        for line in chunk.splitlines()[1:]:
            dest, src, length = ints(line)
            m.append((orange(src, src + length), dest - src))

    def apply_map(mapping: list[tuple[orange, int]], seeds: list[orange], /):
        unmapped = seeds
        new_ranges = []
        for dst, dt in mapping:
            new_unmapped = []
            for rng in unmapped:
                ist = rng & dst
                if ist:
                    new_ranges.append(orange(ist.start + dt, ist.stop + dt))
                    new_unmapped.extend(rng - dst)
                else:
                    new_unmapped.append(rng)
            unmapped = new_unmapped
        return unmapped + new_ranges

    applied = seeds
    for m in maps:
        applied = apply_map(m, seeds)

    return min(s.start for s in applied)
