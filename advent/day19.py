# /usr/bin/env python3
from __future__ import annotations

import re

import pydantic

from advent.base import BaseSolver, Solution


class Rule(pydantic.BaseModel):
    next_state: str
    cond_key: str | None
    interval: tuple[int | float, int | float]

    @classmethod
    def from_str(cls, s: str) -> Rule:
        # a<2006:qkq
        interval = (-float("inf"), float("inf"))
        if ":" not in s:
            return cls(next_state=s, cond_key=None, interval=interval)
        condition, next_state = s.split(":")
        # Split on < or >
        if "<" in condition:
            cond_key, interval = condition.split("<")
            interval = (-float("inf"), int(interval))
        else:
            cond_key, interval = condition.split(">")
            interval = (int(interval) + 1, float("inf"))
        return cls(next_state=next_state, cond_key=cond_key, interval=interval)


class Workflow(pydantic.BaseModel):
    name: str
    rules: list[Rule]

    def evaluate(self, r: RatingRange) -> list[tuple[str, RatingRange]]:
        res = []
        for rule in self.rules:
            if rule.cond_key is None:
                # Everything passes
                res.append((rule.next_state, r))
                return res
            else:
                lo, hi = r.for_key(rule.cond_key)
                intersection_start = int(max(lo, rule.interval[0]))
                intersection_end = int(min(hi, rule.interval[1]))
                if intersection_start <= intersection_end:
                    res.append(
                        (
                            rule.next_state,
                            r.with_updated_key(
                                rule.cond_key, (intersection_start, intersection_end)
                            ),
                        )
                    )
                    if lo < rule.interval[0]:
                        r = r.with_updated_key(rule.cond_key, (lo, intersection_start))
                    elif rule.interval[1] < hi:
                        r = r.with_updated_key(rule.cond_key, (intersection_end, hi))
                    else:
                        # Full intersection, nothing else to do
                        return res
        return res

    @classmethod
    def from_str(cls, s: str) -> Workflow:
        # px{a<2006:qkq,m>2090:A,rfg}
        match = re.match(r"(\w+){(.+)}", s)
        if not match:
            raise ValueError(f"Failed to parse workflow: {s}")
        name, rules_str = match.groups()
        rules = [Rule.from_str(r) for r in rules_str.split(",")]
        return cls(name=name, rules=rules)


class Rating(pydantic.BaseModel):
    x: int
    m: int
    a: int
    s: int

    def total(self) -> int:
        return self.x + self.m + self.a + self.s

    @classmethod
    def from_str(cls, s: str) -> Rating:
        # {x=787,m=2655,a=1222,s=2876}
        match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", s)
        if not match:
            raise ValueError(f"Failed to parse rating: {s}")
        x, m, a, s = match.groups()
        return cls(x=int(x), m=int(m), a=int(a), s=int(s))


class RatingRange(pydantic.BaseModel):
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def part1_score(self) -> int:
        return self.x[0] + self.m[0] + self.a[0] + self.s[0]

    def part2_score(self) -> int:
        x = int(self.x[1] - self.x[0])
        m = int(self.m[1] - self.m[0])
        a = int(self.a[1] - self.a[0])
        s = int(self.s[1] - self.s[0])
        return x * m * a * s

    def for_key(self, key: str) -> tuple[int, int]:
        return getattr(self, key)

    def with_updated_key(self, key: str, value: tuple[int, int]) -> RatingRange:
        return RatingRange(**{**self.dict(), key: value})


class Solver(BaseSolver):
    def solve(self) -> Solution:
        workflow_str, rating_str = self.data.strip().split("\n\n")
        workflows = {}
        for w in workflow_str.split("\n"):
            w = Workflow.from_str(w)
            workflows[w.name] = w
        ratings = [Rating.from_str(r) for r in rating_str.split("\n")]

        res1 = 0
        for rating in ratings:
            start = RatingRange(
                x=(rating.x, rating.x + 1),
                m=(rating.m, rating.m + 1),
                a=(rating.a, rating.a + 1),
                s=(rating.s, rating.s + 1),
            )
            to_check = [("in", start)]
            while len(to_check) > 0:
                node, cur_range = to_check.pop()
                next_states = workflows[node].evaluate(cur_range)
                for (next_node, next_range) in next_states:
                    if next_node == "A":
                        res1 += next_range.part1_score()
                    elif next_node != "R":
                        to_check.append((next_node, next_range))

        start = RatingRange(x=(1, 4001), m=(1, 4001), a=(1, 4001), s=(1, 4001))
        to_check = [("in", start)]
        res2 = 0
        while len(to_check) > 0:
            node, cur_range = to_check.pop(0)
            next_states = workflows[node].evaluate(cur_range)
            for (next_node, next_range) in next_states:
                self.logger.info(f"{node} -> {next_node} ({next_range})")
                if next_node == "A":
                    res2 += next_range.part2_score()
                elif next_node != "R":
                    to_check.append((next_node, next_range))

        return Solution(res1, res2)


Solver.run()
