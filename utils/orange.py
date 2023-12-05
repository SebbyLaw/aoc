from __future__ import annotations
from typing import Iterator

__all__ = ("orange",)


class orange:
    """Range but it supports intersection and subtraction."""

    __slots__ = ("start", "stop")

    def __init__(self, start: int, stop: int, /):
        self.start: int = start
        self.stop: int = stop

    def __iter__(self) -> Iterator[int]:
        # so you can actually use it as a range if you want
        return iter(range(self.start, self.stop))

    def __contains__(self, value: int, /) -> bool:
        return self.start <= value < self.stop

    def __len__(self) -> int:
        return self.stop - self.start

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, (range, orange)):
            return NotImplemented
        return self.start == other.start and self.stop == other.stop

    def __and__(self, other: orange, /) -> orange | None:
        """Return a list of oranges that are in both self and other."""
        if self.start >= other.stop or self.stop <= other.start:
            return None

        return orange(max(self.start, other.start), min(self.stop, other.stop))

    def __sub__(self, other: orange, /) -> list[orange]:
        """Return a list of oranges that are in self but not in other."""
        if self.start >= other.stop or self.stop <= other.start:
            return [self]
        if self.start < other.start:
            if self.stop > other.stop:
                return [orange(self.start, other.start), orange(other.stop, self.stop)]
            else:
                return [orange(self.start, other.start)]
        if self.stop > other.stop:
            return [orange(other.stop, self.stop)]
        return []

    def __bool__(self) -> bool:
        return self.start < self.stop

    def __repr__(self) -> str:
        return f"orange({self.start}, {self.stop})"


# test

if __name__ == "__main__":
    assert orange(0, 10) == range(0, 10), "equality comparison with range"
    assert orange(0, 10) == orange(0, 10), "equality comparison with orange"

    assert 5 in orange(0, 10), "in operator"
    assert 10 not in orange(0, 10), "not in operator"

    assert len(orange(0, 10)) == 10, "len()"
    assert len(orange(2, 5)) == 3, "len()"

    assert orange(0, 10) & orange(5, 15) == orange(5, 10), "intersection"
    assert orange(0, 10) & orange(15, 20) is None, "intersection"
    assert orange(0, 10) & orange(0, 10) == orange(0, 10), "intersection"
    assert orange(0, 10) & orange(0, 5) == orange(0, 5), "intersection"

    assert orange(0, 10) - orange(5, 15) == [orange(0, 5)], "subtraction"
    assert orange(0, 10) - orange(15, 20) == [orange(0, 10)], "subtraction"
    assert orange(0, 10) - orange(0, 10) == [], "subtraction"
    assert orange(0, 10) - orange(0, 5) == [orange(5, 10)], "subtraction"
    assert orange(0, 10) - orange(5, 10) == [orange(0, 5)], "subtraction"
    assert orange(0, 10) - orange(0, 15) == [], "subtraction"
    assert orange(0, 10) - orange(2, 8) == [orange(0, 2), orange(8, 10)], "subtraction"

    assert orange(14, 15) - orange(15, 52) == [orange(14, 15)], "subtraction"
    assert orange(14, 15) & orange(15, 52) is None, "intersection"

    assert orange(0, 10) and True, "truthiness"

    print("all tests passed")
