# /usr/bin/env python3

import collections
import enum

import pydantic

from advent.base import BaseSolver, Solution


class Score(enum.IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand(pydantic.BaseModel):
    hand: list[str]
    bid: int

    def cardscore(self, card: str, jokers_wild: bool = False) -> int:
        scores = {
            "T": 10,
            "J": 11 if jokers_wild else 1,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        return scores.get(card) or int(card)

    def score(self, jokers_wild: bool = False) -> list[int]:
        default = [self.cardscore(card, jokers_wild=jokers_wild) for card in self.hand]
        counter = collections.Counter(self.hand)

        if jokers_wild:
            num_jokers = counter["J"]
            if num_jokers > 0:
                del counter["J"]
                # Find the most common thing and give it num_jokers more
                most_common = counter.most_common(1)
                if len(most_common) == 0:
                    # Must be 5 jokers
                    return [Score.FIVE_OF_A_KIND, *default]
                counter[most_common[0][0]] += num_jokers

        most_common = counter.most_common(2)
        if len(most_common) == 1:
            # Must be 5 of a kind
            return [Score.FIVE_OF_A_KIND, *default]

        max_count = most_common[0][1]
        second_count = most_common[1][1]

        if max_count == 4:
            return [Score.FOUR_OF_A_KIND, *default]
        elif max_count == 3:
            if second_count == 2:
                return [Score.FULL_HOUSE, *default]
            else:
                return [Score.THREE_OF_A_KIND, *default]
        elif max_count == 2:
            if second_count == 2:
                return [Score.TWO_PAIR, *default]
            else:
                return [Score.ONE_PAIR, *default]
        return [Score.HIGH_CARD, *default]


class Solver(BaseSolver):
    def solve(self) -> Solution:
        hands = []
        for line in self.data.splitlines():
            hand_str, bid = line.split(" ")
            hands.append(Hand(hand=list(hand_str), bid=int(bid)))

        hands.sort(key=lambda hand: hand.score())

        res1 = 0
        for rank, hand in enumerate(hands, start=1):
            res1 += rank * hand.bid
        yield res1

        res2 = 0
        hands.sort(key=lambda hand: hand.score(jokers_wild=True))
        for rank, hand in enumerate(hands, start=1):
            res2 += rank * hand.bid
        yield res2


Solver.run()
