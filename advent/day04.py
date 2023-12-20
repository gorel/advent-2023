# /usr/bin/env python3
import collections

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        res1 = 0
        res2_d: dict[int, int] = collections.defaultdict(int)
        for card_id, line in enumerate(self.data.splitlines(), start=1):
            res2_d[card_id] += 1
            winners, mine = line.split(":")[1].split("|")
            power = len(set(winners.split()) & set(mine.split())) - 1

            if power >= 0:
                res1 += 2**power
                # power+2 because if you win 2 cards, power would be 1 but
                # you get scorecards for [n+1, n+2]
                for i in range(1, power + 2):
                    res2_d[card_id + i] += res2_d[card_id]

        # Part2 solution is sum of scorecard counts
        yield res1
        yield sum(res2_d.values())


Solver.run()
