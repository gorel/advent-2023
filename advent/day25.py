# /usr/bin/env python3

from __future__ import annotations

import collections
from dataclasses import dataclass

import tqdm
from z3 import copy

from advent.base import BaseSolver, Solution


@dataclass
class WireSolution:
    splits: list[tuple[str, str]]
    components: list[set[str]]


class Solver(BaseSolver):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.g = collections.defaultdict(set)
        for line in self.lines:
            comp, rest = line.split(":")
            for other in rest.split():
                self.g[comp].add(other.strip())
                self.g[other.strip()].add(comp)

    def components(self, g: dict[str, set[str]]) -> list[set[str]]:
        visited = set()
        components = []

        for comp in g:
            if comp in visited:
                continue
            this_component = set()
            visited.add(comp)
            stack = [comp]
            while stack:
                cur = stack.pop()
                this_component.add(cur)
                for other in g[cur]:
                    if other not in visited:
                        visited.add(other)
                        stack.append(other)
            components.append(this_component)
        return components

    def get_split(self, g: dict[str, set[str]]) -> WireSolution:
        all_pairs = set()
        for comp in self.g:
            for other in self.g[comp]:
                all_pairs.add(((min(comp, other), max(comp, other))))

        if self.is_real:
            # Found by visualization in networkx
            cuts = [("fts", "nvb"), ("jff", "zns"), ("kzx", "qmr")]
            g = copy.deepcopy(self.g)
            for cut in cuts:
                g[cut[0]].remove(cut[1])
                g[cut[1]].remove(cut[0])
            comps = self.components(g)
            if len(comps) == 2:
                return WireSolution(cuts, comps)
        else:
            pbar = tqdm.tqdm(total=len(all_pairs) ** 3)
            pairs = sorted(all_pairs, key=lambda p: len(self.g[p[0]]))
            for pair1 in pairs:
                for pair2 in pairs:
                    if pair1 == pair2:
                        continue
                    for pair3 in pairs:
                        pbar.update(1)
                        if pair1 == pair3 or pair2 == pair3:
                            continue

                        # Try cutting these wires
                        g = copy.deepcopy(self.g)
                        remove_pairs = [pair1, pair2, pair3]
                        self.logger.debug(f"Cutting {remove_pairs}")
                        for pair in remove_pairs:
                            g[pair[0]].remove(pair[1])
                            g[pair[1]].remove(pair[0])

                        # And see if there are now two components
                        comps = self.components(g)
                        if len(comps) == 2:
                            return WireSolution(pairs, comps)
        raise ValueError("No split found")

    def solve(self) -> Solution:
        # Now get all triplets in the pairs
        part1 = self.get_split(self.g)
        yield len(part1.components[0]) * len(part1.components[1])
        yield None


Solver.run()
