# /usr/bin/env python3
from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution


class Grid(pydantic.BaseModel):
    data: list[str]

    @property
    def T(self) -> Grid:
        return Grid(data=["".join(col) for col in zip(*self.data)])

    def reflection_value(self, expected_diffs: int = 0) -> int:
        row_reflection = self._row_reflection(expected_diffs=expected_diffs)
        col_reflection = self.T._row_reflection(expected_diffs=expected_diffs)
        return 100 * row_reflection + col_reflection

    def _row_reflection(self, expected_diffs: int = 0) -> int:
        for split_point in range(1, len(self.data)):
            above = self.data[:split_point][::-1]
            below = self.data[split_point:]
            diffs = sum(self._diff(up, down) for up, down in zip(above, below))
            if diffs == expected_diffs:
                return split_point
        return 0

    def _diff(self, row1: str, row2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(row1, row2))


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grids = [Grid(data=group.split("\n")) for group in self.data.split("\n\n")]
        yield sum(grid.reflection_value() for grid in grids)
        yield sum(grid.reflection_value(expected_diffs=1) for grid in grids)


Solver.run()
