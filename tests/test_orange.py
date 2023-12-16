import pytest
from aoclib import orange


@pytest.mark.parametrize(
    ("o1", "o2", "expected"),
    [
        (orange(0, 10), orange(5, 15), orange(5, 10)),
        (orange(0, 10), orange(15, 20), None),
        (orange(0, 10), orange(0, 10), orange(0, 10)),
        (orange(0, 10), orange(0, 5), orange(0, 5)),
        (orange(14, 15), orange(15, 52), None),
    ],
)
def test_orange_intersection(o1: orange, o2: orange, expected: orange | None):
    assert o1 & o2 == expected


@pytest.mark.parametrize(
    ("o1", "o2", "expected"),
    [
        (orange(0, 10), orange(5, 15), [orange(0, 5)]),
        (orange(0, 10), orange(15, 20), [orange(0, 10)]),
        (orange(0, 10), orange(0, 10), []),
        (orange(0, 10), orange(0, 5), [orange(5, 10)]),
        (orange(0, 10), orange(5, 10), [orange(0, 5)]),
        (orange(0, 10), orange(0, 15), []),
        (orange(0, 10), orange(2, 8), [orange(0, 2), orange(8, 10)]),
        (orange(14, 15), orange(15, 52), [orange(14, 15)]),
    ],
)
def test_orange_difference(o1: orange, o2: orange, expected: list[orange]):
    assert o1 - o2 == expected


@pytest.mark.parametrize(
    ("o1", "o2", "expected"),
    [
        (orange(-1, 10), orange(1, 10), False),
        (orange(0, 10), orange(15, 20), False),
        (orange(0, 10), orange(0, 10), True),
        (orange(0, 10), orange(0, 5), False),
    ],
)
def test_orange_equality(o1: orange, o2: orange, expected: bool):
    assert (o1 == o2) is expected


@pytest.mark.parametrize(
    ("o", "expected"),
    [
        (orange(0, 10), 10),
        (orange(2, 5), 3),
    ],
)
def test_orange_length(o: orange, expected: int):
    assert len(o) == expected


@pytest.mark.parametrize(
    ("o", "n", "expected"),
    [
        (orange(0, 10), 5, True),
        (orange(0, 10), 10, False),
        (orange(0, 10), 15, False),
        (orange(0, 10), -1, False),
        (orange(0, 10), 0, True),
        (orange(-5, 5), -5, True),
    ],
)
def test_orange_contains(o: orange, n: int, expected: bool):
    assert (n in o) is expected


def test_orange_truthiness():
    assert bool(orange(0, 10)) is True
