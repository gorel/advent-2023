from __future__ import annotations

import pydantic


class OverlapResult(pydantic.BaseModel):
    intersected: list[Interval]
    carried: list[Interval]


class Interval(pydantic.BaseModel):
    """Represents a half-open interval [lo, hi) of integers."""

    lo: int
    hi: int

    @property
    def empty(self) -> bool:
        return self.lo >= self.hi

    def __and__(self, other: Interval) -> Interval:
        return Interval(
            lo=max(self.lo, other.lo),
            hi=min(self.hi, other.hi),
        )

    def overlap(self, interval: Interval) -> OverlapResult:
        intersected = []
        carried = []

        intersection_start = max(self.lo, interval.lo)
        intersection_end = min(self.hi, interval.hi)
        if intersection_start <= intersection_end:
            intersected.append(Interval(lo=intersection_start, hi=intersection_end))

            if interval.lo < self.lo:
                carried.append(Interval(lo=interval.lo, hi=intersection_start))
            if self.hi < interval.hi:
                carried.append(Interval(lo=intersection_end, hi=interval.hi))
        else:
            carried.append(interval)
        return OverlapResult(intersected=intersected, carried=carried)


class IntervalSet(pydantic.BaseModel):
    intervals: list[Interval] = pydantic.Field(default_factory=list)

    def overlap_all(self, intervals: list[Interval]) -> OverlapResult:
        intersected = []
        for my_interval in self.intervals:
            new_working_intervals = []
            for interval in intervals:
                this_result = my_interval.overlap(interval)
                intersected.extend(this_result.intersected)
                new_working_intervals.extend(this_result.carried)
            intervals = new_working_intervals
        return OverlapResult(intersected=intersected, carried=intervals)
