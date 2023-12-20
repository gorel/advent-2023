# /usr/bin/env python3
from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution
from advent.intervals import Interval


class OverlapResult(pydantic.BaseModel):
    changed: list[Interval]
    carried: list[Interval]


class EntrySet(pydantic.BaseModel):
    name: str
    entries: list[Entry] = pydantic.Field(default_factory=list)

    def transform_intervals(self, intervals: list[Interval]) -> OverlapResult:
        changed = []
        for entry in self.entries:
            new_working_intervals = []
            for interval in intervals:
                this_result = entry.get_overlap(interval)
                changed.extend(this_result.changed)
                new_working_intervals.extend(this_result.carried)
            intervals = new_working_intervals
        return OverlapResult(changed=changed, carried=intervals)


class Entry(pydantic.BaseModel):
    source: int
    dest: int
    length: int

    def get_overlap(self, interval: Interval) -> OverlapResult:
        changed = []
        carried = []

        intersection_start = max(self.source, interval.lo)
        intersection_end = min(self.source + self.length, interval.hi)
        if intersection_start <= intersection_end:
            new_lo = self.dest - self.source + intersection_start
            new_hi = self.dest - self.source + intersection_end
            changed.append(Interval(lo=new_lo, hi=new_hi))

            if interval.lo < self.source:
                carried.append(Interval(lo=interval.lo, hi=intersection_start))
            if self.source + self.length < interval.hi:
                carried.append(Interval(lo=intersection_end, hi=interval.hi))
        else:
            carried.append(interval)
        return OverlapResult(changed=changed, carried=carried)


class Almanac(pydantic.BaseModel):
    seeds: list[int]
    transformations: list[EntrySet]

    def part1_ranges(self) -> list[Interval]:
        return [Interval(lo=seed, hi=seed + 1) for seed in self.seeds]

    def part2_ranges(self) -> list[Interval]:
        return [
            Interval(lo=lo, hi=lo + length)
            for lo, length in zip(self.seeds[::2], self.seeds[1::2])
        ]


class Solver(BaseSolver):
    def parse(self) -> Almanac:
        lines = self.data.splitlines()
        seeds = [int(x) for x in lines[0].split(":")[1].split()]
        transformations = []
        i = 2
        while i < len(lines):
            name = lines[i].split(" ")[0]
            self.logger.debug(f"Parsing {lines[i]}")
            transformations.append(EntrySet(name=name))
            i += 1
            while i < len(lines) and lines[i] != "":
                dst, src, length = [int(x) for x in lines[i].split()]
                m = Entry(source=src, dest=dst, length=length)
                transformations[-1].entries.append(m)
                i += 1
            i += 1

        return Almanac(seeds=seeds, transformations=transformations)

    def solve(self) -> Solution:
        self.logger.info("Parsing almanac")
        almanac = self.parse()

        self.logger.info("Running part 1")
        intervals = almanac.part1_ranges()
        for transformation in almanac.transformations:
            self.logger.info(f"Applying transformation {transformation.name}")
            self.logger.info(f"Have intervals: {intervals}")
            next_result = transformation.transform_intervals(intervals)
            intervals = next_result.changed + next_result.carried

        yield min(interval.lo for interval in intervals)

        self.logger.info("Running part 2")
        intervals = almanac.part2_ranges()
        for transformation in almanac.transformations:
            self.logger.info(f"Applying transformation {transformation.name}")
            next_result = transformation.transform_intervals(intervals)
            intervals = next_result.changed + next_result.carried

        yield min(interval.lo for interval in intervals)


Solver.run()
