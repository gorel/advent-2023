# /usr/bin/env python3

from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution
from advent.graph import Point


class Node(pydantic.BaseModel):
    value: int
    adj: list[Point]


class Solver(BaseSolver):
    def solve(self) -> Solution:
        points_of_interest = {}
        nodes = []

        for r, line in enumerate(self.data.splitlines()):
            in_number = False
            cur = []
            cur_adj = set()
            for c, s in enumerate(line):
                # First record the point of interest
                if not s.isdigit() and s != ".":
                    points_of_interest[Point(r, c)] = s

                # Then handle numbers
                if s.isdigit():
                    in_number = True
                    cur.append(s)
                    for point in Point(r, c).adjacent8():
                        cur_adj.add(point)
                elif in_number:
                    nodes.append(Node(value=int("".join(cur)), adj=list(cur_adj)))
                    cur = []
                    cur_adj = set()
                    in_number = False
            if in_number:
                nodes.append(Node(value=int("".join(cur)), adj=list(cur_adj)))

        # Now we go through all the nodes (numbers) and if they're adjacent to a
        # point of interest, we add them to the result.
        # For part2, we check if the PoI is a gear and if so either store it in our
        # "gears" dict or multiply it by the previously stored node's value.
        # This relies on each gear being adjacent to no more than two nodes.
        res1 = 0
        res2 = 0
        gears: dict[Point, int] = {}
        for node in nodes:
            added = False
            for adj in node.adj:
                if adj in points_of_interest:
                    if not added:
                        res1 += node.value
                        added = True
                    if points_of_interest[adj] == "*":
                        if adj in gears:
                            res2 += node.value * gears[adj]
                        gears[adj] = node.value

        yield res1
        yield res2


Solver.run()
