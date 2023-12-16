from typing import Any

from utils import *


tests = [
    test(
        """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    ),
    test(
        """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    seen: set[complex] = {complex()}
    head = tail = complex()

    for line in inp.lines:
        d, n = line.split()
        delta = complex(*CHAR_TO_DELTA[d])
        for _ in range(int(n)):
            head += delta
            dh = head - tail
            if max(abs(dh.real), abs(dh.imag)) > 1:
                tail = head - delta

            seen.add(tail)
    return len(seen)


@runs(
    *tests,
    submit,
)
def b(inp: Input) -> Any:
    seen: set[complex] = {complex()}
    # tail is idx -1
    # head is idx 0
    snake: list[complex] = [complex() for _ in range(10)]

    def move_snake(idx: int, delta: complex, /):
        snake[idx] += delta
        try:
            next_segment = snake[idx + 1]
        except IndexError:
            return
        dh = snake[idx] - next_segment
        if abs(dh.real) + abs(dh.imag) == 3:
            move_snake(idx + 1, complex(norm(dh.real), norm(dh.imag)))
        elif 2 in (abs(dh.real), abs(dh.imag)):
            move_snake(idx + 1, complex(dh.real // 2, dh.imag // 2))

    for line in inp.lines:
        d, n = line.split()
        for _ in range(int(n)):
            move_snake(0, complex(*CHAR_TO_DELTA[d]))
            seen.add(snake[-1])

    return len(seen)
