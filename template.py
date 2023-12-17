# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        for line in self.lines:
            print(line)
        return Solution(None, None)


Solver.run()
