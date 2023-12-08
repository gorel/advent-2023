# /usr/bin/env python3

import math

import pydantic

from advent.base import BaseSolver, Solution


class Transition(pydantic.BaseModel):
    left: str
    right: str


def get_dist_to_z(
    transitions: dict[str, Transition], actions: str, cur: str, last_only: bool = False
) -> int:
    res = 0
    while cur != "ZZZ":
        if last_only and cur[-1] == "Z":
            break
        action = actions[res % len(actions)]
        res += 1
        if action == "L":
            cur = transitions[cur].left
        else:
            cur = transitions[cur].right
    return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        lines = self.data.splitlines()
        actions = lines[0]
        transitions = {}
        for line in lines[2:]:
            key, value = line.split(" = ")
            left, right = value[1:-1].split(",")
            transitions[key.strip()] = Transition(
                left=left.strip(), right=right.strip()
            )

        res1 = get_dist_to_z(transitions, actions, "AAA")
        cur = {node for node in transitions if node[-1] == "A"}
        lcms = []

        for start_node in cur:
            print(f"Starting from {start_node}")
            entry = get_dist_to_z(transitions, actions, start_node, last_only=True)
            print(f"Dist for {start_node}: {entry}")
            lcms.append(entry)

        res2 = math.lcm(*lcms)

        return Solution(res1, res2)


Solver.run()
