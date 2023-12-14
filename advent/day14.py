# /usr/bin/env python3
from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution


class Grid(pydantic.BaseModel):
    g: list[str]

    @property
    def T(self) -> Grid:
        return Grid(g=["".join(x) for x in zip(*self.g)])

    def tilt(self) -> Grid:
        g2 = self.T
        out = []
        for row in g2.g:
            next_left_idx = 0
            next_row = []
            for j, char in enumerate(row):
                if char == "#":
                    next_left_idx = j + 1
                    while len(next_row) < j:
                        next_row.append(".")
                elif char == "O":
                    next_row.append("O")
                    next_left_idx += 1
            out.append("".join(next_row))
        return Grid(g=out)

    def load(self) -> int:
        res = 0
        for i, row in enumerate(self.g):
            for char in row:
                if char == "#":
                    res += len(self.g) - i
        return res

    def load(self) -> int:
        g2 = self.T
        res = 0
        # Count how many things are *left*
        for row in g2.g:
            print(f"Process {row}")
            next_left_idx = 0
            for j, char in enumerate(row):
                if char == "#":
                    next_left_idx = j + 1
                elif char == "O":
                    res += len(row) - next_left_idx
                    next_left_idx += 1
        return res

    def cycle(self) -> Grid:
        for i in range(4):
            g = self.T
        g2 = self.


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grid = Grid(g=self.lines)

        res1 = grid.load()

        for _ in range(1000000000):
            grid = grid.cycle()
        res2 = grid.load()

        return Solution(res1, None)


Solver.run()
