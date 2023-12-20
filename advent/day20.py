# /usr/bin/env python3
from __future__ import annotations

import collections
import math

import pydantic

from advent.base import BaseSolver, Solution


class Module(pydantic.BaseModel):
    mtype: str
    name: str
    dests: list[str]
    sources: list[str] = pydantic.Field(default_factory=list)
    my_state: int = 0

    last_pulses: dict[str, int] = pydantic.Field(default_factory=dict)

    def process(self, mmap: dict[str, Module], pulse: int) -> list[tuple[str, int]]:
        match self.mtype:
            case "inv":
                if pulse == 1:
                    return []
                else:
                    self.my_state = 1 - self.my_state
                    for dst in self.dests:
                        if dst in mmap:
                            mmap[dst].last_pulses[self.name] = self.my_state
                    return [(dst, self.my_state) for dst in self.dests]
            case "cnj":
                all_high = all(self.last_pulses.get(s) == 1 for s in self.sources)
                if all_high:
                    self.my_state = 0
                    for dst in self.dests:
                        if dst in mmap:
                            mmap[dst].last_pulses[self.name] = 0
                    return [(dst, 0) for dst in self.dests]
                else:
                    self.my_state = 1
                    for dst in self.dests:
                        if dst in mmap:
                            mmap[dst].last_pulses[self.name] = 1
                    return [(dst, 1) for dst in self.dests]
            case _:
                for dst in self.dests:
                    if dst in mmap:
                        mmap[dst].last_pulses[self.name] = pulse
                return [(dst, pulse) for dst in self.dests]

    def __hash__(self) -> int:
        return hash(self.name)

    @classmethod
    def from_str(cls, line: str) -> Module:
        name, dests_str = line.split("->")
        mtype = {"&": "cnj", "%": "inv"}.get(name[0], "_")
        name = name.lstrip("&%")
        dests = [x.strip() for x in dests_str.split(",")]
        return cls(name=name.strip(), mtype=mtype, dests=dests)


class Solver(BaseSolver):
    def parse(self) -> dict[str, Module]:
        m = [Module.from_str(line) for line in self.lines]
        innodes = collections.defaultdict(list)
        innodes["broadcaster"].append("button")
        for mod in m:
            for dest in mod.dests:
                innodes[dest].append(mod.name)
        for mod in m:
            mod.sources = innodes[mod.name]
        return {mod.name: mod for mod in m}

    def broadcast(
        self,
        graph: dict[str, Module],
        pushes: int | None = None,
        target: str | None = None,
    ) -> int:
        res = {0: 0, 1: 0}
        i = 0
        special_inputs: dict[str, int | None] = {}
        if target is not None:
            special_inputs = {src: None for src in graph[target].sources}

        while pushes is None or i < pushes:
            i += 1
            q: collections.deque[tuple[str, int]] = collections.deque(
                [("broadcaster", 0)]
            )
            while q:
                tonode, pulse = q.popleft()
                res[pulse] += 1
                if tonode not in graph:
                    continue
                node = graph[tonode]
                for dest, pulse in node.process(graph, pulse):
                    q.append((dest, pulse))
                    if dest == target and pulse == 1:
                        special_inputs[tonode] = i

            # For part 2
            if len(special_inputs) > 0 and all(
                x is not None for x in special_inputs.values()
            ):
                vals = [x for x in special_inputs.values() if x is not None]
                return math.lcm(*vals)

        # For part 1
        return res[0] * res[1]

    def solve(self) -> Solution:
        yield self.broadcast(self.parse(), 1000)
        if self.is_example:
            self.logger.info("Skipping part2 for example")
            yield None

        yield self.broadcast(self.parse(), target="th")


Solver.run()
