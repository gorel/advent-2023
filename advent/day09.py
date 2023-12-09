# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        res1 = 0
        res2 = 0
        for line in self.data.splitlines():
            vals = [int(x) for x in line.split()]

            res1 += vals[-1]
            remember = [vals[0]]

            diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
            while not all(d == 0 for d in diffs):
                res1 += diffs[-1]
                remember.append(diffs[0])
                diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]

            cur = 0
            for value in reversed(remember):
                cur = value - cur
            res2 += cur

        return Solution(res1, res2)


Solver.run()
