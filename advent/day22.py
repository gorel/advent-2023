# /usr/bin/env python3
from __future__ import annotations

import dataclasses

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

    def __hash__(self) -> int:
        return hash(self.id)

    def zpos(self) -> int:
        return min(self.point1.z, self.point2.z)

    def fall(self, new_z: int) -> None:
        self.point1 = Point3D(self.point1.x, self.point1.y, new_z)
        self.point2 = Point3D(self.point2.x, self.point2.y, new_z)

    def all_points(self) -> list[Point3D]:
        points = []
        for x in range(self.point1.x, self.point2.x + 1):
            for y in range(self.point1.y, self.point2.y + 1):
                for z in range(self.point1.z, self.point2.z + 1):
                    points.append(Point3D(x, y, z))
        return points

    @classmethod
    def from_str(cls, id: str, s: str) -> Brick:
        point1, point2 = s.split("~")
        x, y, z = point1.split(",")
        x2, y2, z2 = point2.split(",")
        point1 = Point3D(int(x), int(y), int(z))
        point2 = Point3D(int(x2), int(y2), int(z2))
        return cls(id, point1, point2)


class Solver(BaseSolver):
    def idx(self, x: int, y: int, z: int) -> int:
        return x + y * 9 + z * 9 * 9

    def solve(self) -> Solution:
        # Create a 9x9x260 grid filled with None
        grid: list[Brick | None] = [None] * 9 * 9 * 260
        bricks = []
        for i, line in enumerate(self.lines):
            letter = chr(ord("A") + i % 26)
            number = i // 26 + 1
            identifier = f"{letter}{number}"
            bricks.append(Brick.from_str(identifier, line))

        # First make them fall
        for brick in sorted(bricks, key=lambda b: b.zpos()):
            bottom = None
            for x in range(brick.point1.x, brick.point2.x + 1):
                if bottom is not None:
                    break
                for y in range(brick.point1.y, brick.point2.y + 1):
                    if bottom is not None:
                        break
                    for new_z in range(brick.zpos(), 0, -1):
                        if grid[self.idx(x, y, new_z)] is not None:
                            bottom = new_z + 1
                            break

            if bottom is None:
                bottom = 1
            brick.fall(bottom)
            for point in brick.all_points():
                grid[self.idx(point.x, point.y, point.z)] = brick

        # Then see who they're under
        for x in range(9):
            for y in range(9):
                for z in range(2, 256):
                    brick1 = grid[self.idx(x, y, z)]
                    brick2 = grid[self.idx(x, y, z - 1)]
                    if brick1 is not None and brick2 is not None and brick1 != brick2:
                        self.logger.debug(f"{brick1.id} is under {brick2.id}")
                        brick1.bricks_above.add(brick2)
                        brick2.bricks_below.add(brick1)

        # And lastly, see if removing each brick leaves a brick with nothing under it
        non_load_bearing_bricks = {brick.id for brick in bricks}
        for brick in bricks:
            if len(brick.bricks_below) == 1:
                non_load_bearing_bricks.discard(list(brick.bricks_below)[0].id)

        yield len(non_load_bearing_bricks)

        yield None


Solver.run()
