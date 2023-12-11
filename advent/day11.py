# /usr/bin/env python3
from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution
from advent.graph import Point


class GalaxyMap(pydantic.BaseModel):
    galaxies: list[Point]
    empty_rows: set[int]
    empty_cols: set[int]

    def dist(self, p1: Point, p2: Point, factor: int = 2) -> int:
        new_dist = 0
        low_row = min(p1.row, p2.row)
        high_row = max(p1.row, p2.row)
        for i in range(low_row, high_row):
            new_dist += factor if i in self.empty_rows else 1
        low_col = min(p1.col, p2.col)
        high_col = max(p1.col, p2.col)
        for i in range(low_col, high_col):
            new_dist += factor if i in self.empty_cols else 1
        return new_dist

    def pairwise_dists(self, factor: int = 2) -> dict[tuple[Point, Point], int]:
        res = {}
        for g1_idx in range(len(self.galaxies) - 1):
            for g2_idx in range(g1_idx + 1, len(self.galaxies)):
                p1 = self.galaxies[g1_idx]
                p2 = self.galaxies[g2_idx]
                res[(p1, p2)] = self.dist(p1, p2, factor)
        return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        galaxies = []
        empty_rows = set()
        empty_cols = set()
        for row, line in enumerate(self.lines):
            if all(c == "." for c in line):
                empty_rows.add(row)
            for col, char in enumerate(line):
                if char == "#":
                    galaxies.append(Point(row, col))

        for col in range(len(self.lines[0])):
            if all(line[col] == "." for line in self.lines):
                empty_cols.add(col)

        g = GalaxyMap(galaxies=galaxies, empty_rows=empty_rows, empty_cols=empty_cols)

        res1 = sum(g.pairwise_dists(factor=2).values())
        res2 = sum(g.pairwise_dists(factor=1_000_000).values())
        return Solution(res1, res2)


Solver.run()
