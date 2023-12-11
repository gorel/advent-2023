from __future__ import annotations

import dataclasses
from typing import Iterator, Tuple


@dataclasses.dataclass(frozen=True)
class Point:
    DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    x: int
    y: int

    @property
    def row(self) -> int:
        return self.x

    @property
    def col(self) -> int:
        return self.y

    def adjacent(self) -> Iterator[Point]:
        for d in self.DIRS:
            yield self + Point(d[0], d[1])

    def adjacent8(self) -> Iterator[Point]:
        for d in self.DIRS_8:
            yield self + Point(d[0], d[1])

    def manhattan_dist(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_dist(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other: Point | Tuple[int, int]) -> Point:
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: Point) -> bool:
        return (self.x, self.y) < (other.x, other.y)


@dataclasses.dataclass
class Line:
    start: Point
    end: Point

    def __iter__(self) -> Iterator[Point]:
        if self.start.x == self.end.x:
            if self.start.y < self.end.y:
                for yy in range(self.start.y, self.end.y + 1):
                    yield Point(self.start.x, yy)
            else:
                for yy in range(self.end.y, self.start.y + 1):
                    yield Point(self.start.x, yy)
        else:
            if self.start.x < self.end.x:
                for xx in range(self.start.x, self.end.x + 1):
                    yield Point(xx, self.start.y)
            else:
                for xx in range(self.end.x, self.start.x + 1):
                    yield Point(xx, self.start.y)
