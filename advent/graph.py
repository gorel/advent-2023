from __future__ import annotations

import dataclasses
import enum
from typing import Iterator, Tuple


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    def ascii(self) -> str:
        match self:
            case Direction.LEFT:
                return "<"
            case Direction.RIGHT:
                return ">"
            case Direction.UP:
                return "^"
            case Direction.DOWN:
                return "v"

    @property
    def clockwise(self) -> Direction:
        match self:
            case Direction.LEFT:
                return Direction.UP
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.UP:
                return Direction.RIGHT
            case Direction.DOWN:
                return Direction.LEFT

    @property
    def counter_clockwise(self) -> Direction:
        # Two wrongs don't make a right, but three lefts do.
        return self.clockwise.clockwise.clockwise


@dataclasses.dataclass(frozen=True)
class Point:
    DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    row: int
    col: int

    def move(self, direction: Direction) -> Point:
        match direction:
            case Direction.LEFT:
                return Point(self.row, self.col - 1)
            case Direction.RIGHT:
                return Point(self.row, self.col + 1)
            case Direction.UP:
                return Point(self.row - 1, self.col)
            case Direction.DOWN:
                return Point(self.row + 1, self.col)

    def adjacent(self) -> Iterator[Point]:
        for d in self.DIRS:
            yield self + Point(d[0], d[1])

    def adjacent8(self) -> Iterator[Point]:
        for d in self.DIRS_8:
            yield self + Point(d[0], d[1])

    def manhattan_dist(self, other: Point) -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def euclidean_dist(self, other: Point) -> float:
        return ((self.row - other.row) ** 2 + (self.col - other.col) ** 2) ** 0.5

    def __add__(self, other: Point | Tuple[int, int]) -> Point:
        if isinstance(other, tuple):
            return Point(self.row + other[0], self.col + other[1])
        return Point(self.row + other.row, self.col + other.col)

    def __lt__(self, other: Point) -> bool:
        return (self.row, self.col) < (other.row, other.col)


@dataclasses.dataclass
class Line:
    start: Point
    end: Point

    def __iter__(self) -> Iterator[Point]:
        if self.start.row == self.end.row:
            if self.start.col < self.end.col:
                for yy in range(self.start.col, self.end.col + 1):
                    yield Point(self.start.row, yy)
            else:
                for yy in range(self.end.col, self.start.col + 1):
                    yield Point(self.start.row, yy)
        else:
            if self.start.row < self.end.row:
                for xx in range(self.start.row, self.end.row + 1):
                    yield Point(xx, self.start.col)
            else:
                for xx in range(self.end.row, self.start.row + 1):
                    yield Point(xx, self.start.col)
