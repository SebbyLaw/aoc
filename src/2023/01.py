from typing import Any
from utils import *


tests = [
    test(
        """

"""
    ),
]


@runs(
    *tests,
    # submit,
)
def a(inp: Input) -> Any:
    ...


@runs(
    *tests,
    # submit,
)
def b(inp: Input) -> Any:
    ...
