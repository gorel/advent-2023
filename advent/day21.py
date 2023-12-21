# /usr/bin/env python3

import numpy as np
import tqdm

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
        translated = Point(p.row % len(self.g), p.col % len(self.g[0]))
        return self.g[translated.row][translated.col]

    def points_after(self, to_find: list[int]) -> dict[int, int]:
        res = {}
        q = {self.start}
        for i in tqdm.tqdm(range(1, max(to_find) + 1)):
            new_q = set()
            for _ in range(len(q)):
                for n in q.pop().adjacent():
                    if self.at(n) != "#":
                        new_q.add(n)
            q = new_q
            if i in to_find:
                self.logger.debug(f"Found {i} => {len(q)}")
                res[i] = len(q)
        return res

    def solve(self) -> Solution:
        # The points are (x, y) and we're asking for the y at point x=target
        target = 6 if self.is_example else 64
        yield self.points_after(to_find=[target])[target]

        if self.is_example:
            yield None

        # total_steps = 26_501_365 = 65 + 131 * 202300
        # We can solve with points [(65, y1), (65+131, y2), (65+131+131, y3)]
        # Shout out to https://old.reddit.com/r/adventofcode/comments/18nevo3/2023_day_21_solutions/keaiiq7/  # noqa
        # which helped me understand how/why this logic works.
        targets = [65, 65 + 131, 65 + 131 + 131]
        res = self.points_after(to_find=targets)
        indices, values = zip(*enumerate(res.values()))
        coef = np.polyfit(indices, values, 2)
        # Let's turn that coef into a one-liner
        yield round(np.polyval(coef, 202300))  # type: ignore


Solver.run()
