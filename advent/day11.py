# /usr/bin/env python3
from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Point


def dist(
    empty_rows: set[int], empty_cols: set[int], p1: Point, p2: Point, factor: int = 2
) -> int:
    new_dist = 0
    low_row = min(p1.row, p2.row)
    high_row = max(p1.row, p2.row)
    for i in range(low_row, high_row):
        new_dist += factor if i in empty_rows else 1
    low_col = min(p1.col, p2.col)
    high_col = max(p1.col, p2.col)
    for i in range(low_col, high_col):
        new_dist += factor if i in empty_cols else 1
    return new_dist


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

        # Find the shortest path visiting all galaxies
        pair_dists = []
        for g1_idx in range(len(galaxies) - 1):
            for g2_idx in range(g1_idx + 1, len(galaxies)):
                pair_dists.append(
                    dist(empty_rows, empty_cols, galaxies[g1_idx], galaxies[g2_idx])
                )

        res1 = sum(pair_dists)

        return Solution(res1, None)


Solver.run()
