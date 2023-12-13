# /usr/bin/env python3
from __future__ import annotations

import pydantic

from advent.base import BaseSolver, Solution


class Grid(pydantic.BaseModel):
    data: list[str]

    @property
    def T(self) -> Grid:
        return Grid(data=["".join(col) for col in zip(*self.data)])

    def reflection(self, expected_diffs: int = 0) -> tuple[int, int]:
        row_reflection = self._row_reflection(expected_diffs=expected_diffs)
        col_reflection = self.T._row_reflection(expected_diffs=expected_diffs)
        return row_reflection, col_reflection

    def _row_reflection(self, expected_diffs: int = 0) -> int:
        for split_point in range(1, len(self.data)):
            lines_above = self.data[:split_point]
            lines_below = self.data[split_point:]
            length = min(len(lines_above), len(lines_below))
            above = lines_above[::-1][:length]
            below = lines_below[:length]
            diffs = sum(self._diff(up, down) for up, down in zip(above, below))
            if diffs == expected_diffs:
                return split_point
        return 0

    def _diff(self, row1: str, row2: str) -> int:
        return sum(1 for c1, c2 in zip(row1, row2) if c1 != c2)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grids = [Grid(data=group.split("\n")) for group in self.data.split("\n\n")]

        res1 = 0
        res2 = 0
        for grid in grids:
            row, col = grid.reflection()
            res1 += 100 * row + col
            row2, col2 = grid.reflection(expected_diffs=1)
            res2 += 100 * row2 + col2

        return Solution(res1, res2)


Solver.run()
