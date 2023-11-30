from __future__ import annotations

import dataclasses
from typing import Iterator


@dataclasses.dataclass(frozen=True)
class Point:
    DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    x: int
    y: int

    def adjacent(self) -> Iterator[Point]:
        for d in self.DIRS:
            yield self + d

    def adjacent8(self) -> Iterator[Point]:
        for d in self.DIRS_8:
            yield self + d

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


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


class CoordinateGraph:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height
