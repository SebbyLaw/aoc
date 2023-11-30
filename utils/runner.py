from functools import cache
import logging

from pathlib import Path
import textwrap
from typing import Any, Callable, TypeAlias

from aocd import _impartial_submit, get_data
from typing_extensions import Self

from utils.core import Input

__all__ = (
    "runs",
    "submit",
    "test",
    "cout",
    "endl",
)


# thanks danny
class _ColorFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]

    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            "%H:%M:%S",
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


level = logging.DEBUG
handler = logging.StreamHandler()

log = logging.getLogger()
log.setLevel(level)
handler.setFormatter(_ColorFormatter())
log.handlers = [handler]


class _Endl:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "endl"


endl = _Endl()


class _Cout:
    __slots__ = ("_buffer",)

    def __init__(self):
        self._buffer: list[Any] = []

    def flush(self):
        if self._buffer:
            log.debug(" ".join(map(str, self._buffer)))
            self._buffer.clear()

    def __lshift__(self, msg: Any | _Endl, /) -> Self:
        if msg is endl:
            self.flush()
        else:
            self._buffer.append(msg)
        return self


cout = _Cout()


# region: auto run and submit
class RunnerLog:
    __slots__ = ("name", "part", "log", "solution")

    def __init__(self, name: str, part: str, /):
        self.name = name
        self.part = part
        self.log = logging.getLogger(f"{name}.{part}")
        self.solution: Any = None

    def set_solution(self, solution: Any, /) -> None:
        self.solution = solution

    def log_input(self, inp: Input, /) -> None:
        self.log.info("====================")
        self.log.info(f"{self.name.title()} input:\n\x1b[0;34m{inp}")

    def __enter__(self):
        self.log.info("====================")
        self.log.info("Running...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.log.exception("Ignoring Exception:", exc_info=exc_val)
        if self.solution is not None:
            self.log.info("Result: %s", self.solution)


Solution: TypeAlias = Callable[[Input], str | int]
DecoratesSolution: TypeAlias = Callable[[Solution, RunnerLog], Solution]


@cache
def get_day_and_year(func: Solution, /) -> tuple[int, int]:
    path = Path(func.__code__.co_filename)
    year = int(path.parent.name)
    day = int(path.parts[-1][:-3])
    return day, year


@cache
def get_input(day: int, year: int, /) -> Input:
    return Input(get_data(day=day, year=year))


def submit(func: Solution, log: RunnerLog, /) -> Solution:
    part = func.__name__[0]

    day, year = get_day_and_year(func)

    inp = get_input(day, year)
    answer = func(inp)
    log.set_solution(answer)

    # set ansii color to green for submitter
    print("                  \x1b[35m_impartial_submit(): \x1b[32m", end="")
    _impartial_submit(
        answer,
        part=part,
        reopen=True,
        quiet=False,
        day=day,
        year=year,
    )

    return func


class runs:
    __slots__ = ("calls",)

    def __init__(self, *calls: DecoratesSolution):
        self.calls: list[DecoratesSolution] = [*calls]

        if submit not in self.calls:
            self.calls.append(self.runner)

    @staticmethod
    def runner(func: Solution, log: RunnerLog, /) -> Solution:
        day, year = get_day_and_year(func)
        inp = get_input(day, year)
        answer = func(inp)
        log.set_solution(answer)
        return func

    def __call__(self, func: Solution, /) -> Solution:
        for fn in self.calls:
            with RunnerLog(fn.__name__, func.__name__) as _log:
                func = fn(func, _log)

        return func


def test(ex: str, /) -> DecoratesSolution:
    inp = Input(textwrap.dedent(ex.strip()))

    def _tester(func: Solution, log: RunnerLog, /) -> Solution:
        log.log_input(inp)
        answer = func(inp)
        log.set_solution(answer)

        return func

    _tester.__name__ = "test"
    return _tester


# endregion
