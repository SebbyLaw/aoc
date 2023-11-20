from typing import Any, Callable, TypeAlias

from aocd import _impartial_submit, get_data
from typing_extensions import Self

__all__ = (
    "run",
    "submit",
)


# region: auto run and submit
Solution: TypeAlias = Callable[[str], str | int]
DecoratesSolution: TypeAlias = Callable[[Solution], Solution]


class Runner:
    __slots__ = ("calls",)

    def __init__(self):
        self.calls: list[DecoratesSolution] = []

    @staticmethod
    def _actual_runner(func: Solution, /):
        answer = func(get_data(year=2023))
        print(f"Result for {func.__name__}: {answer}")

    def __call__(self, func: Solution, /) -> Solution:
        if self.calls:
            for fn in self.calls:
                func = fn(func)
        else:
            self._actual_runner(func)

        return func

    # do a little trolling
    def __and__(self, other: Callable[[Solution], Any], /) -> Self:
        self.calls.append(other)
        return self


run = Runner()


def submit(func: Solution, /) -> Solution:
    part = func.__name__[0]

    answer = func(get_data(year=2023))

    _impartial_submit(
        answer,
        part=part,
        reopen=True,
        quiet=False,
    )

    return func


# endregion
