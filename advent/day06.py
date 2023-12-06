# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        times = [int(x) for x in self.data.splitlines()[0].split(":")[1].split()]
        dists = [int(x) for x in self.data.splitlines()[1].split(":")[1].split()]

        res1 = 1
        for time, dist in zip(times, dists):
            res1 *= sum(1 for i in range(time - 1) if i * (time - i) > dist)

        time = int(self.data.splitlines()[0].split(":")[1].replace(" ", ""))
        dist = int(self.data.splitlines()[1].split(":")[1].replace(" ", ""))
        res2 = sum(1 for i in range(time - 1) if i * (time - i) > dist)

        return Solution(res1, res2)


Solver.run()
