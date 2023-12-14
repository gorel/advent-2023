# /usr/bin/env python3
from __future__ import annotations

import pydantic
import tqdm

from advent.base import BaseSolver, Solution

TARGET = 1000000000 - 1


class Grid(pydantic.BaseModel):
    g: list[str]

    @property
    def T(self) -> Grid:
        return Grid(g=["".join(x) for x in zip(*self.g)])

    @property
    def Tinv(self) -> Grid:
        return Grid(g=["".join(x) for x in zip(*self.g[::-1])])

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
                    next_row.append("#")
                elif char == "O":
                    next_row.append("O")
                    next_left_idx += 1
            while len(next_row) < len(row):
                next_row.append(".")
            out.append("".join(next_row))
        return Grid(g=out).T

    def load(self) -> int:
        res = 0
        for i, row in enumerate(self.g):
            for char in row:
                if char == "O":
                    res += len(self.g) - i
        return res

    def display(self) -> None:
        for row in self.g:
            print(row)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grid = Grid(g=self.lines)
        grid = grid.tilt()
        res1 = grid.load()

        loads = []
        last_load = -1
        load = -1
        min_loads = 1_000
        self.logger.info("Progress bar shows estimate...")
        for _ in tqdm.tqdm(range(TARGET), total=int(min_loads * 1.05)):
            last_load = load
            # Do 4 tilts
            for _ in range(4):
                grid = grid.tilt()
                grid = grid.Tinv
                load = grid.load()
            if (
                len(loads) > min_loads
                and load == loads[min_loads]
                and last_load == loads[min_loads - 1]
            ):
                loads = loads[min_loads:]
                break
            loads.append(load)

        # Find the cycle index corresponding to the last load
        self.logger.info(f"Found cycle length of {len(loads)}")
        res2 = loads[(TARGET - min_loads) % len(loads)]

        return Solution(res1, res2)


Solver.run()
