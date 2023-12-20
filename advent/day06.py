# /usr/bin/env python3

import numpy as np

from advent.base import BaseSolver, Solution


# Inspired by the "WolframAlpha" solution:
# https://old.reddit.com/r/adventofcode/comments/18bwe6t/2023_day_6_solutions/kc6wwxq/
def solve_algebraically(time: int, dist: int) -> int:
    roots = np.roots([1, -time, dist])
    bigger, smaller = max(roots), min(roots)
    res = int(bigger) - int(smaller)
    # We want to strictly *win* and this would be a tie
    if bigger == int(bigger):
        res -= 1
    return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        times = [int(x) for x in self.data.splitlines()[0].split(":")[1].split()]
        dists = [int(x) for x in self.data.splitlines()[1].split(":")[1].split()]

        res1 = 1
        for time, dist in zip(times, dists):
            # Previous solution used brute force counting
            # res1 *= sum(1 for i in range(time - 1) if i * (time - i) > dist)
            res1 *= solve_algebraically(time, dist)
        yield res1

        time = int(self.data.splitlines()[0].split(":")[1].replace(" ", ""))
        dist = int(self.data.splitlines()[1].split(":")[1].replace(" ", ""))
        # res2 = sum(1 for i in range(time - 1) if i * (time - i) > dist)
        yield solve_algebraically(time, dist)


Solver.run()
