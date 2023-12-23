# /usr/bin/env python3

import sys

from advent.base import BaseSolver, Solution
from advent.graph import Point

sys.setrecursionlimit(10000)


class Solver(BaseSolver):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.g = [[c for c in line] for line in self.lines]

    @property
    def rows(self) -> int:
        return len(self.g)

    @property
    def cols(self) -> int:
        return len(self.g[0])

    def at(self, p: Point) -> str:
        return self.g[p.row][p.col]

    def can_walk_between(self, src: Point, dst: Point) -> bool:
        match self.at(dst):
            case "#":
                return False
            case ">":
                return src.col < dst.col
            case "<":
                return src.col > dst.col
            case "^":
                return src.row > dst.row
            case "v":
                return src.row < dst.row
            case _:
                return True

    def dfs(
        self,
        start: Point | None = None,
        dest: Point | None = None,
        visited: set[Point] | None = None,
    ) -> int:
        start = start or Point(0, 1)
        dest = dest or Point(self.rows - 1, self.cols - 2)
        visited = visited or set()

        if start == dest:
            return 0

        visited.add(start)
        longest_path = 0
        for adj in start.adjacent():
            if self.can_walk_between(start, adj) and adj not in visited:
                longest_path = max(longest_path, self.dfs(adj, dest, visited) + 1)
        visited.remove(start)

        return longest_path

    def solve(self) -> Solution:
        yield self.dfs()
        yield None


Solver.run()
