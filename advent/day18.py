# /usr/bin/env python3
from __future__ import annotations

import numpy as np
import pydantic

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Point


class Action(pydantic.BaseModel):
    direction: Direction
    num: int
    code: str

    def invert(self) -> Action:
        m = {0: Direction.RIGHT, 1: Direction.DOWN, 2: Direction.LEFT, 3: Direction.UP}
        num = int(self.code[:5], 16)
        direction = m[int(self.code[-1], 16)]
        return Action(direction=direction, num=num, code=self.code)


class Grid:
    def __init__(self, actions: list[Action], origin: Point = Point(0, 0)) -> None:
        self.vertices = []
        self.perimeter = 0
        for action in actions:
            self.vertices.append(origin)
            self.perimeter += action.num
            origin += {
                Direction.LEFT: (-action.num, 0),
                Direction.RIGHT: (action.num, 0),
                Direction.UP: (0, -action.num),
                Direction.DOWN: (0, action.num),
            }[action.direction]

    def area(self) -> int:
        x = np.array([p.col for p in self.vertices])
        y = np.array([p.row for p in self.vertices])
        # Shoelace only gives us internal count
        interior = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        # We need to also add the points from the perimeter... but there's a catch.
        # Total area = internal points + perimeter
        # But, imagine this:
        #   0 1 2
        # 0 # # #
        # 1 # . #
        # 2 # # #
        # Shoelace gives us area=4 (2x2 square), but we need to add the perimeter
        # If we just naively add it (perimeter=8), we get 12. The true answer is 9
        # Which we get from interior (4) + half perimeter (4) + 1 = 9. Geometrically,
        # you can think of it like this where S = point that shoelace covers.
        #
        #   0 1 2
        # 0 S S #
        # 1 S S #
        # 2 # # #
        # So you can see we need the other "half" of the perimeter plus the corner point
        return int(interior + self.perimeter // 2 + 1)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        actions = []
        for line in self.lines:
            direction, num, code = line.split()
            direction = Direction.from_short(direction.upper())
            actions.append(Action(direction=direction, num=int(num), code=code[2:-1]))

        res1 = Grid(actions).area()
        res2 = Grid([a.invert() for a in actions]).area()
        return Solution(res1, res2)


Solver.run()
