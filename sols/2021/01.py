from utils import *


tests = [
    test(
        """
199
200
208
210
200
207
240
269
260
263
"""
    )
]


@runs(
    *tests,
    submit,
)
def a(inp: Input):
    ns = inp.ints

    total = 0

    for i, n in enumerate(ns[1:], start=1):
        if n > ns[i - 1]:
            total += 1

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input):
    def sums(*nums: int) -> int:
        return sum(nums)

    ns = lmap(sums, inp.ints, inp.ints[1:], inp.ints[2:])

    total = 0
    for i, n in enumerate(ns[1:], start=1):
        if n > ns[i - 1]:
            total += 1

    return total
