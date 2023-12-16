from collections import defaultdict
import pathlib
from typing import Any
from utils import *


tests = [
    test(
        """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    ),
]


def build_fs(lines: list[str]) -> dict[str, int]:
    curr: pathlib.PurePosixPath = pathlib.PurePosixPath("/")

    sizes = defaultdict(int)
    ldx = 0

    while ldx < len(lines):
        line = lines[ldx]
        ldx += 1

        if line.startswith("$ cd "):
            if line == "$ cd ..":
                curr = curr.parent
            elif line == "$ cd /":
                curr = pathlib.PurePosixPath("/")
            else:
                curr /= line[5:]
        elif line == "$ ls":
            while ldx < len(lines) and not lines[ldx].startswith("$"):
                f = lines[ldx]
                ldx += 1
                if not f.startswith("dir "):
                    size, _name = f.split(" ", 1)
                    part = curr
                    while True:
                        sizes[str(part)] += int(size)
                        if part == pathlib.PurePosixPath("/"):
                            break
                        part = part.parent
    return sizes


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    sizes = build_fs(inp.lines)
    return sum(s for s in sizes.values() if s < 100000)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    sizes = build_fs(inp.lines)
    total = 70000000
    needed = 30000000
    have = total - sizes[str(pathlib.PurePosixPath("/"))]
    need_free = needed - have

    print(min(s for s in sizes.values() if s >= need_free))
    return min(s for s in sizes.values() if s >= need_free)
