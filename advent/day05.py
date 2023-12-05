# /usr/bin/env python3

import logging
import math

import pydantic
import tqdm

from advent.base import BaseSolver, Solution


class Entry(pydantic.BaseModel):
    source: int
    dest: int
    length: int

    def overlap_from(self, s: int) -> int | None:
        dist = s - self.source
        if 0 <= dist < self.length:
            return self.dest + dist
        return None


class Almanac:
    def __init__(self, data: dict[str, dict[str, list[Entry]]]) -> None:
        self.logger = logging.getLogger()
        self.data = data
        self.memo = {}

    def dfs(self, key: str, target: int) -> int | float:
        # if key in self.memo:
        #    return self.memo[key]

        if key == "location":
            self.memo[key] = target
            return target

        best = float("inf")
        for dst in self.data[key]:
            for entry in self.data[key][dst]:
                new_dest = entry.overlap_from(target)
                if new_dest is not None:
                    best = min(best, self.dfs(dst, new_dest))
            if math.isinf(best):
                best = target

        self.memo[key] = best
        return best


class Solver(BaseSolver):
    def parse(self) -> Almanac:
        lines = self.data.splitlines()
        data = {}
        i = 2
        while i < len(lines):
            from_thing, to_thing = lines[i].split()[0].split("-to-")
            data[from_thing] = {to_thing: []}
            i += 1
            while i < len(lines) and lines[i] != "":
                dst, src, length = [int(x) for x in lines[i].split()]
                m = Entry(source=src, dest=dst, length=length)
                data[from_thing][to_thing].append(m)
                i += 1
            i += 1

        return Almanac(data)

    def solve(self) -> Solution:
        almanac = self.parse()
        seeds = [int(x) for x in self.data.splitlines()[0].split(":")[1].split()]
        self.logger.info("Parsed almanac")

        self.logger.info("Running dfs for part 1")
        res1 = float("inf")
        for seed in seeds:
            res1 = min(res1, almanac.dfs("seed", seed))
        self.logger.info(f"Got {res1} for part 1")

        # Get pairs
        pairs = []
        i = 0
        while i < len(seeds):
            pairs.append((seeds[i], seeds[i + 1]))
            i += 2

        res2 = float("inf")
        self.logger.info(f"Running on {len(pairs)} pairs")
        for lo, length in pairs:
            self.logger.info(f"Find dfs from seed {lo} (range={length})")
            for seed in tqdm.tqdm(range(lo, lo + length)):
                res2 = min(res2, almanac.dfs("seed", seed))

        return Solution(int(res1), int(res2))


Solver.run()
