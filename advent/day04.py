# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        res1 = 0
        res2_d = {}
        for line in self.data.splitlines():
            game, rest = line.split(":")
            card_id = int(game.split(" ")[-1])
            if card_id not in res2_d:
                res2_d[card_id] = 1
            winners, mine = rest.split("|")
            # Too lazy to properly split
            winning_cards = [x for x in winners.split(" ") if len(x) != 0]
            my_cards = [x for x in mine.split(" ") if len(x) != 0]

            power = -1
            any_match = False
            for card in my_cards:
                if card in winning_cards:
                    any_match = True
                    power += 1

            if any_match:
                res1 += 2**power
                # power+2 because if you win 2 cards, power would be 1 but
                # you get scorecards for [n+1, n+2]
                for i in range(1, power + 2):
                    if card_id + i not in res2_d:
                        res2_d[card_id + i] = 1
                    res2_d[card_id + i] += res2_d[card_id]

        # Part2 solution is sum of scorecard counts
        return Solution(res1, sum(res2_d.values()))


Solver.run()
