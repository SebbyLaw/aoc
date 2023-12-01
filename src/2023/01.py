import re
from typing import Any
from utils import *


tests = [
    test(
        """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    ),
    test(
        """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
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
        ns = re.findall(r"\d", line)
        total += int(f"{ns[0]}{ns[-1]}")

    return total


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    nums = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    total = 0
    for line in inp.lines:
        ns = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", line)
        first = ns[0]

        l2 = line[-1]
        line = line[:-1]
        while True:
            ns = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", l2)
            if not ns:
                l2 = line[-1] + l2
                line = line[:-1]
            else:
                second = ns[-1]
                break

        try:
            first = nums[first]
        except KeyError:
            pass

        try:
            second = nums[second]
        except KeyError:
            pass

        total += int(f"{first}{second}")

    return total
