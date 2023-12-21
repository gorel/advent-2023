from __future__ import annotations

import dataclasses
import enum
from typing import Generic, Iterator, Tuple, TypeVar

Value = TypeVar("Value")


class Direction(enum.Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    UPLEFT = (-1, -1)
    UPRIGHT = (-1, 1)
    DOWNLEFT = (1, -1)
    DOWNRIGHT = (1, 1)

    @classmethod
    def cardinal(cls) -> list[Direction]:
        return [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

    @classmethod
    def diagonal(cls) -> list[Direction]:
        return [
            Direction.UPLEFT,
            Direction.UPRIGHT,
            Direction.DOWNLEFT,
            Direction.DOWNRIGHT,
        ]

    def __mul__(self, n: int) -> Point:
        return Point(self.value[0] * n, self.value[1] * n)

    def __rmul__(self, n: int) -> Point:
        return self * n

    def ascii(self) -> str:
        match self:
            case Direction.LEFT:
                return "←"
            case Direction.RIGHT:
                return "→"
            case Direction.UP:
                return "↑"
            case Direction.DOWN:
                return "↓"
            case Direction.UPLEFT:
                return "↖"
            case Direction.UPRIGHT:
                return "↗"
            case Direction.DOWNLEFT:
                return "↙"
            case Direction.DOWNRIGHT:
                return "↘"

    @property
    def clockwise(self) -> Direction:
        return self.clockwise45.clockwise45

    @property
    def clockwise45(self) -> Direction:
        match self:
            case Direction.LEFT:
                return Direction.UPLEFT
            case Direction.RIGHT:
                return Direction.DOWNRIGHT
            case Direction.UP:
                return Direction.UPRIGHT
            case Direction.DOWN:
                return Direction.DOWNLEFT
            case Direction.UPLEFT:
                return Direction.UP
            case Direction.UPRIGHT:
                return Direction.RIGHT
            case Direction.DOWNLEFT:
                return Direction.LEFT
            case Direction.DOWNRIGHT:
                return Direction.DOWN

    @property
    def counter_clockwise(self) -> Direction:
        # Two wrongs don't make a right, but three lefts do.
        return self.clockwise.clockwise.clockwise

    @property
    def counter_clockwise45(self) -> Direction:
        match self:
            case Direction.LEFT:
                return Direction.DOWNLEFT
            case Direction.RIGHT:
                return Direction.UPRIGHT
            case Direction.UP:
                return Direction.UPLEFT
            case Direction.DOWN:
                return Direction.DOWNRIGHT
            case Direction.UPLEFT:
                return Direction.LEFT
            case Direction.UPRIGHT:
                return Direction.UP
            case Direction.DOWNLEFT:
                return Direction.DOWN
            case Direction.DOWNRIGHT:
                return Direction.RIGHT

    def turn_left(self) -> Direction:
        return self.counter_clockwise

    def turn_right(self) -> Direction:
        return self.clockwise

    def turn_left45(self) -> Direction:
        return self.counter_clockwise45

    def turn_right45(self) -> Direction:
        return self.clockwise45

    @property
    def opposite(self) -> Direction:
        return self.clockwise.clockwise

    @classmethod
    def from_str(cls, s: str) -> Direction:
        match s.upper():
            case "L" | "W" | "LEFT" | "WEST":
                return Direction.LEFT
            case "R" | "E" | "RIGHT" | "EAST":
                return Direction.RIGHT
            case "U" | "N" | "UP" | "NORTH":
                return Direction.UP
            case "D" | "S" | "DOWN" | "SOUTH":
                return Direction.DOWN
            case "UL" | "NW" | "UPLEFT" | "NORTHWEST":
                return Direction.UPLEFT
            case "UR" | "NE" | "UPRIGHT" | "NORTHEAST":
                return Direction.UPRIGHT
            case "DL" | "SW" | "DOWNLEFT" | "SOUTHWEST":
                return Direction.DOWNLEFT
            case "DR" | "SE" | "DOWNRIGHT" | "SOUTHEAST":
                return Direction.DOWNRIGHT
            case _:
                raise ValueError(f"Invalid direction: {s}")


@dataclasses.dataclass(frozen=True)
class Point:
    row: int
    col: int

    @property
    def x(self) -> int:
        return self.row

    @property
    def y(self) -> int:
        return self.col

    def move(self, direction: Direction) -> Point:
        return self + direction

    def adjacent(self) -> Iterator[Point]:
        for p, _ in self.adjacent_with_dirs():
            yield p

    def adjacent_with_dirs(self) -> Iterator[tuple[Point, Direction]]:
        for d in Direction.cardinal():
            yield (self + d, d)

    def adjacent8(self) -> Iterator[Point]:
        for p, _ in self.adjacent8_with_dirs():
            yield p

    def adjacent8_with_dirs(self) -> Iterator[tuple[Point, Direction]]:
        for d in Direction:
            yield (self + d, d)

    def manhattan_dist(self, other: Point) -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def euclidean_dist(self, other: Point) -> float:
        return ((self.row - other.row) ** 2 + (self.col - other.col) ** 2) ** 0.5

    def __add__(self, other: Point | Direction | Tuple[int, int]) -> Point:
        if isinstance(other, tuple):
            return Point(self.row + other[0], self.col + other[1])
        elif isinstance(other, Direction):
            return Point(self.row + other.value[0], self.col + other.value[1])
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


@dataclasses.dataclass
class Grid(Generic[Value]):
    g: list[list[Value]]

    @property
    def rows(self) -> int:
        return len(self.g)

    @property
    def cols(self) -> int:
        return len(self.g[0])

    @property
    def T(self) -> Grid[Value]:
        return Grid([list(x) for x in zip(*self.g)])

    def inbounds(self, p: Point) -> bool:
        return 0 <= p.row < len(self.g) and 0 <= p.col < len(self.g[0])

    def at(self, p: Point) -> Value:
        return self.g[p.row][p.col]

    def __iter__(self) -> Iterator[tuple[Point, Value]]:
        for row in range(self.rows):
            for col in range(self.cols):
                yield (Point(row, col), self.g[row][col])
