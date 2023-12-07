# /usr/bin/env python3

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

    def cardscore(self, card: str) -> int:
        if card == "T":
            return 10
        if card == "J":
            return 11
        if card == "Q":
            return 12
        if card == "K":
            return 13
        if card == "A":
            return 14
        return int(card)

    def score(self) -> list[int]:
        # Five of a kind
        if self.hand[0] == self.hand[4]:
            return [Score.FIVE_OF_A_KIND, self.cardscore(self.hand[0])]
        # Four of a kind
        if self.hand[0] == self.hand[3]:
            return [
                Score.FOUR_OF_A_KIND,
                self.cardscore(self.hand[0]),
                self.cardscore(self.hand[4]),
            ]
        if self.hand[1] == self.hand[4]:
            return [
                Score.FOUR_OF_A_KIND,
                self.cardscore(self.hand[1]),
                self.cardscore(self.hand[0]),
            ]
        # Full house
        if self.hand[0] == self.hand[2] and self.hand[3] == self.hand[4]:
            return [
                Score.FULL_HOUSE,
                self.cardscore(self.hand[0]),
                self.cardscore(self.hand[3]),
            ]
        if self.hand[0] == self.hand[1] and self.hand[2] == self.hand[4]:
            return [
                Score.FULL_HOUSE,
                self.cardscore(self.hand[2]),
                self.cardscore(self.hand[0]),
            ]

        # Three of a kind
        if self.hand[0] == self.hand[2]:
            others = sorted(
                [self.cardscore(self.hand[3]), self.cardscore(self.hand[4])]
            )
            return [
                Score.THREE_OF_A_KIND,
                self.cardscore(self.hand[0]),
                *others,
            ]
        if self.hand[1] == self.hand[3]:
            others = sorted(
                [self.cardscore(self.hand[0]), self.cardscore(self.hand[4])]
            )
            return [
                Score.THREE_OF_A_KIND,
                self.cardscore(self.hand[1]),
                *others,
            ]

        if self.hand[2] == self.hand[4]:
            others = sorted(
                [self.cardscore(self.hand[0]), self.cardscore(self.hand[1])]
            )
            return [
                Score.THREE_OF_A_KIND,
                self.cardscore(self.hand[2]),
                *others,
            ]

        # Two pair
        for i in range(5):
            for i_pairer in range(i + 1, 5):
                for j in range(i_pairer + 1, 5):
                    for j_pairer in range(j + 1, 5):
                        if (
                            self.hand[i] == self.hand[i_pairer]
                            and self.hand[j] == self.hand[j_pairer]
                        ):
                            pair1 = self.cardscore(self.hand[i])
                            pair2 = self.cardscore(self.hand[j])
                            if pair1 < pair2:
                                pair1, pair2 = pair2, pair1

                            last_card_idx = list(
                                set(range(5)) - set([i, i_pairer, j, j_pairer])
                            )[0]
                            last_card_score = self.cardscore(self.hand[last_card_idx])
                            return [Score.TWO_PAIR, pair1, pair2, last_card_score]

        # One pair
        for i in range(5):
            for i_pairer in range(i + 1, 5):
                if self.hand[i] == self.hand[i_pairer]:
                    pair = self.cardscore(self.hand[i])
                    other_cards = set(range(5)) - set([i, i_pairer])
                    other_scores = [
                        self.cardscore(self.hand[idx]) for idx in other_cards
                    ]
                    return [Score.ONE_PAIR, pair, *other_scores]

        return sorted(self.cardscore(card) for card in self.hand)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        hands = []
        for line in self.data.splitlines():
            hand, bid = line.split(" ")
            hands.append(Hand(hand=sorted(hand), bid=int(bid)))

        hands.sort(key=lambda hand: hand.score())

        res1 = 0
        for rank, hand in enumerate(hands, start=1):
            res1 += rank * hand.bid

        return Solution(res1, None)


Solver.run()
