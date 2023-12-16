# /usr/bin/env python3

import collections

import joblib
import pydantic
import tqdm

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Point

Beam = tuple[Point, Direction]


class Grid(pydantic.BaseModel):
    g: list[str]

    def inbounds(self, p: Point) -> bool:
        return 0 <= p.row < len(self.g) and 0 <= p.col < len(self.g[0])

    def calculate_energized(
        self, starting_transition: Beam | None = None
    ) -> set[Point]:
        if starting_transition is None:
            starting_transition = (Point(0, 0), Direction.RIGHT)

        q: collections.deque[Beam] = collections.deque([starting_transition])
        visited: set[Beam] = {q[0]}

        while q:
            cur_point, cur_dir = q.popleft()
            for transition in self.next_dirs(cur_point, cur_dir):
                if transition in visited or not self.inbounds(transition[0]):
                    continue
                visited.add(transition)
                q.append(transition)
        return {p for p, _ in visited}

    def next_dirs(self, cur_point: Point, cur_dir: Direction) -> list[Beam]:
        deflector = self.g[cur_point.row][cur_point.col]
        dirs = []
        match deflector, cur_dir:
            case "/", Direction.LEFT | Direction.RIGHT:
                dirs = [cur_dir.counter_clockwise]
            case "/", Direction.UP | Direction.DOWN:
                dirs = [cur_dir.clockwise]
            case "\\", Direction.LEFT | Direction.RIGHT:
                dirs = [cur_dir.clockwise]
            case "\\", Direction.UP | Direction.DOWN:
                dirs = [cur_dir.counter_clockwise]
            case "|", Direction.LEFT | Direction.RIGHT:
                dirs = [Direction.UP, Direction.DOWN]
            case "-", Direction.UP | Direction.DOWN:
                dirs = [Direction.LEFT, Direction.RIGHT]
            case _:
                dirs = [cur_dir]
        return [(cur_point.move(d), d) for d in dirs]

    def starting_transitions(self) -> list[Beam]:
        rows = len(self.g)
        cols = len(self.g[0])
        res = []
        # Along the top
        res += [(Point(0, yy), Direction.DOWN) for yy in range(cols)]
        # Along the bottom
        res += [(Point(len(self.g) - 1, yy), Direction.UP) for yy in range(cols)]
        # Along the left side
        res += [(Point(xx, 0), Direction.RIGHT) for xx in range(rows)]
        # Along the right side
        res += [(Point(xx, len(self.g[0]) - 1), Direction.LEFT) for xx in range(rows)]
        return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grid = Grid(g=self.lines)
        res1 = len(grid.calculate_energized())

        results: list[set[Point]] = joblib.Parallel(n_jobs=-1)(
            joblib.delayed(grid.calculate_energized)(pos)
            for pos in tqdm.tqdm(grid.starting_transitions())
        )
        res2 = max(len(r) for r in results)

        return Solution(res1, res2)


Solver.run()
