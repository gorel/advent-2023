# /usr/bin/env python3

from advent.base import BaseSolver, Solution
from advent.graph import Point


class Solver(BaseSolver):
    def solve(self) -> Solution:
        galaxies = {}
        empty_rows = set()
        empty_cols = set()
        for row, line in enumerate(self.lines):
            if all(c == "." for c in line):
                empty_rows.add(row)

        for col in range(len(self.lines[0])):
            if all(line[col] == "." for line in self.lines):
                empty_cols.add(col)

        newg = []
        for row, line in enumerate(self.lines):
            r = []
            for col, char in enumerate(line):
                if col in empty_cols:
                    r.append(char)
                r.append(char)
            if row in empty_rows:
                newg.append(r)
            newg.append(r)

        galaxies = []
        for row, line in enumerate(newg):
            for col, char in enumerate(line):
                if char == "#":
                    galaxies.append(Point(row, col))

        # Find the shortest path visiting all galaxies
        pair_dists = []
        for g1_idx in range(len(galaxies) - 1):
            for g2_idx in range(g1_idx + 1, len(galaxies)):
                g1 = galaxies[g1_idx]
                g2 = galaxies[g2_idx]
                pair_dists.append(g1.manhattan(g2))

        res1 = sum(pair_dists)

        return Solution(res1, None)


Solver.run()
