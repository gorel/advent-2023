# /usr/bin/env python3
from __future__ import annotations

import dataclasses

import matplotlib.pyplot as plt
import numpy as np

from advent.base import BaseSolver, Solution


@dataclasses.dataclass
class Point3D:
    x: int
    y: int
    z: int


@dataclasses.dataclass
class Brick:
    id: str
    point1: Point3D
    point2: Point3D
    bricks_below: set[Brick] = dataclasses.field(default_factory=set)
    bricks_above: set[Brick] = dataclasses.field(default_factory=set)
    below_ids: set[str] = dataclasses.field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.id)

    def minz(self) -> int:
        return min(self.point1.z, self.point2.z)

    def maxz(self) -> int:
        return max(self.point1.z, self.point2.z)

    def fall(self, new_z: int) -> None:
        fall_distance = self.minz() - new_z
        self.point1 = Point3D(
            self.point1.x, self.point1.y, self.point1.z - fall_distance
        )
        self.point2 = Point3D(
            self.point2.x, self.point2.y, self.point2.z - fall_distance
        )

    def all_points(self) -> list[Point3D]:
        points = []
        for x in range(self.point1.x, self.point2.x + 1):
            for y in range(self.point1.y, self.point2.y + 1):
                for z in range(self.point1.z, self.point2.z + 1):
                    points.append(Point3D(x, y, z))
        return points

    def bottom_surface(self) -> list[Point3D]:
        points = []
        for x in range(self.point1.x, self.point2.x + 1):
            for y in range(self.point1.y, self.point2.y + 1):
                points.append(Point3D(x, y, self.minz()))
        return points

    def top_surface(self) -> list[Point3D]:
        points = []
        for x in range(self.point1.x, self.point2.x + 1):
            for y in range(self.point1.y, self.point2.y + 1):
                points.append(Point3D(x, y, self.maxz()))
        return points

    def vertices(self) -> list[Point3D]:
        return [
            Point3D(self.point1.x, self.point1.y, self.point1.z),
            Point3D(self.point2.x, self.point1.y, self.point1.z),
            Point3D(self.point1.x, self.point2.y, self.point1.z),
            Point3D(self.point2.x, self.point2.y, self.point1.z),
            Point3D(self.point1.x, self.point1.y, self.point2.z),
            Point3D(self.point2.x, self.point1.y, self.point2.z),
            Point3D(self.point1.x, self.point2.y, self.point2.z),
            Point3D(self.point2.x, self.point2.y, self.point2.z),
        ]

    @classmethod
    def from_str(cls, id: str, s: str) -> Brick:
        point1, point2 = s.split("~")
        x, y, z = point1.split(",")
        x2, y2, z2 = point2.split(",")
        point1 = Point3D(int(x), int(y), int(z))
        point2 = Point3D(int(x2), int(y2), int(z2))
        return cls(id, point1, point2)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        # grid stores at [x][y], (zpos, brick_id)
        grid = [[(0, "")] * 9 for _ in range(9)]
        bricks = []
        for i, line in enumerate(self.lines):
            letter = chr(ord("A") + i % 26)
            number = i // 26 + 1
            identifier = f"{letter}{number}"
            bricks.append(Brick.from_str(identifier, line))

        for brick in sorted(bricks, key=lambda b: b.minz()):
            # Make them fall
            fall_to_zidx = 1
            for point in brick.bottom_surface():
                fall_to_zidx = min(fall_to_zidx, grid[point.x][point.y][0] + 1)
            brick.fall(fall_to_zidx)

            # Then see what's below
            for point in brick.bottom_surface():
                below_zidx, below_id = grid[point.x][point.y]
                if below_zidx == point.z - 1 and below_id != "":
                    brick.below_ids.add(below_id)

            # Then update grid2
            for point in brick.top_surface():
                grid[point.x][point.y] = (point.z, brick.id)

        # And now find the dependent bricks
        load_bearing_bricks = set()
        for brick in bricks:
            if len(brick.below_ids) == 1:
                # That's a load bearing brick
                load_bearing_bricks.add(list(brick.below_ids)[0])
        yield len(bricks) - len(load_bearing_bricks)

        yield None


Solver.run()
