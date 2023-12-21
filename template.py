# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        for line in self.lines:
            print(line)

        yield None
        yield None


Solver.run()
