# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        for line in self.lines:
            print(line)
        res1 = 0
        yield res1

        res2 = 0
        yield res2


Solver.run()
