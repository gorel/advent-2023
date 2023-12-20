# /usr/bin/env python3
from __future__ import annotations

import math

import pydantic

from advent.base import BaseSolver, Solution


class Transition(pydantic.BaseModel):
    left: str
    right: str


class TransitionTable(pydantic.BaseModel):
    transitions: dict[str, Transition]
    actions: str

    @property
    def a_starts(self) -> list[str]:
        return [key for key in self.transitions if key[-1] == "A"]

    def zdist(self, cur: str, last_only: bool = False) -> int:
        res = 0
        while cur != "ZZZ":
            if last_only and cur[-1] == "Z":
                break
            action = self.actions[res % len(self.actions)]
            res += 1
            if action == "L":
                cur = self.transitions[cur].left
            else:
                cur = self.transitions[cur].right
        return res

    @classmethod
    def from_lines(cls, lines: list[str]) -> TransitionTable:
        actions = lines[0]
        transitions = {}
        for line in lines[2:]:
            key, value = line.split(" = ")
            left, right = value[1:-1].split(",")
            transitions[key.strip()] = Transition(
                left=left.strip(), right=right.strip()
            )
        return TransitionTable(transitions=transitions, actions=actions)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        tbl = TransitionTable.from_lines(self.data.splitlines())

        yield tbl.zdist("AAA")
        yield math.lcm(*[tbl.zdist(node, last_only=True) for node in tbl.a_starts])


Solver.run()
