from collections import Counter
from typing import Any
from utils import *


tests = [
    test(
        """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    twos = threes = 0
    for line in inp.lines:
        counts = Counter(line)
        twos += 2 in counts.values()
        threes += 3 in counts.values()

    print(twos, threes)
    return twos * threes


@runs(
    test(
        """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""
    ),
    submit,
)
def b(inp: Input) -> Any:
    lines = inp.lines
    for i, line in enumerate(lines):
        for other in lines[i + 1 :]:
            diff = 0
            for a, b in zip(line, other):
                if a != b:
                    diff += 1
                    if diff > 1:
                        break
            else:
                return "".join(a for a, b in zip(line, other) if a == b)
