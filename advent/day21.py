# /usr/bin/env python3

from typing import Callable

from advent.base import BaseSolver, Solution
from advent.graph import Point

Graph = list[list[str]]


class Solver(BaseSolver):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.g = [list(line) for line in self.lines]
        self.start = Point(-1, -1)
        for i, row in enumerate(self.g):
            for j, c in enumerate(row):
                if c == "S":
                    self.start = Point(i, j)

    def at(self, p: Point) -> str:
        if 0 <= p.row < len(self.g) and 0 <= p.col < len(self.g[0]):
            return self.g[p.row][p.col]
        return "#"

    def at2(self, p: Point) -> str:
        translated = Point(p.row % len(self.g), p.col % len(self.g[0]))
        return self.at(translated)

    def points_after(
        self,
        steps: int,
        at_func: Callable[[Point], str],
        print_all: bool = False,
    ) -> set[Point]:
        q = {self.start}
        for i in range(steps):
            new_q = set()
            for _ in range(len(q)):
                for n in q.pop().adjacent():
                    if at_func(n) != "#":
                        new_q.add(n)
            q = new_q
            if print_all:
                print(f"({i}, {len(q)})")
        return set(q)

    def solve(self) -> Solution:
        total_steps = 6 if self.is_example else 64
        yield len(self.points_after(total_steps, self.at))

        if self.is_example:
            yield None
        total_steps = 26_501_365
        yield len(self.points_after(total_steps, self.at2, print_all=True))


Solver.run()
