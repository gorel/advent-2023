# /usr/bin/env python3
from __future__ import annotations

import dataclasses

import z3

from advent.base import BaseSolver, Solution


@dataclasses.dataclass
class Point3D:
    x: float
    y: float
    z: float
    vx: int = 0
    vy: int = 0
    vz: int = 0

    @classmethod
    def from_str(cls, line: str) -> Point3D:
        xyz, vxyz = line.split("@")
        x, y, z = xyz.split(",")
        vx, vy, vz = vxyz.split(",")
        return cls(int(x), int(y), int(z), int(vx), int(vy), int(vz))

    def will_reach_point(self, other: Point3D) -> bool:
        match self.vx > 0, self.vy > 0:
            case True, True:
                return other.x >= self.x and other.y >= self.y
            case True, False:
                return other.x >= self.x and other.y <= self.y
            case False, True:
                return other.x <= self.x and other.y >= self.y
            case False, False:
                return other.x <= self.x and other.y <= self.y
        raise ValueError("You have defied the laws of boolean logic")


@dataclasses.dataclass
class Line2D:
    start: Point3D
    slope: float
    intercept: float

    @classmethod
    def from_point3d(cls, p: Point3D) -> Line2D:
        p2 = Point3D(p.x + p.vx, p.y + p.vy, p.z + p.vz)
        slope = (p2.y - p.y) / (p2.x - p.x)
        intercept = p.y - slope * p.x
        return Line2D(p, slope, intercept)

    @classmethod
    def from_str(cls, line: str) -> Line2D:
        return cls.from_point3d(Point3D.from_str(line))

    def will_reach_point(self, p: Point3D) -> bool:
        return self.start.will_reach_point(p)

    def intersection(self, other: Line2D) -> Point3D:
        if self.slope == other.slope:
            return Point3D(-1, -1, -1)

        x = (other.intercept - self.intercept) / (self.slope - other.slope)
        y = self.slope * x + self.intercept

        # Ensure that the intersection is in the "future" for both
        res = Point3D(x, y, 0)
        if self.will_reach_point(res) and other.will_reach_point(res):
            return res
        return Point3D(-1, -1, -1)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        lines = [Line2D.from_str(line) for line in self.lines]
        minx = 7 if self.is_example else 200_000_000_000_000
        maxx = 27 if self.is_example else 400_000_000_000_000
        miny = float("-inf") if self.is_example else minx
        maxy = float("inf") if self.is_example else maxx

        res = 0
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                intersection = lines[i].intersection(lines[j])
                if minx <= intersection.x <= maxx and miny <= intersection.y <= maxy:
                    res += 1
        yield res

        # Part 2 - we need to find a starting position and velocity that will intersect
        # every rock. Let's call our rock Point3D(sx, sy, sz, dx, dy, dz). For each
        # hailstone as Point3D(x, y, z, vx, vy, vz) we need to find t such that
        # sx + dx * t == sx + vx * t
        # sy + dy * t == sy + vy * t
        # sz + dz * t == sz + vz * t
        # This is really hard to solve programatically, so let's just use Z3
        # I never would've figured this out without the help from the reddit post.
        s = z3.Solver()
        sx, sy, sz = z3.BitVec("sx", 64), z3.BitVec("sy", 64), z3.BitVec("sz", 64)
        dx, dy, dz = z3.BitVec("dx", 64), z3.BitVec("dy", 64), z3.BitVec("dz", 64)
        for i, line in enumerate(lines):
            t = z3.BitVec(f"t{i}", 64)
            s.add(
                t >= 0,
                sx + dx * t == line.start.x + line.start.vx * t,
                sy + dy * t == line.start.y + line.start.vy * t,
                sz + dz * t == line.start.z + line.start.vz * t,
            )
        self.logger.info("Asking Z3 to solve")
        assert s.check() == z3.sat
        model = s.model()
        res = model.eval(sx + sy + sz)
        yield int(str(res))


Solver.run()
