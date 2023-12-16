# /usr/bin/env python3

import collections

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
            case "/", Direction.LEFT:
                dirs = [Direction.DOWN]
            case "/", Direction.RIGHT:
                dirs = [Direction.UP]
            case "/", Direction.UP:
                dirs = [Direction.RIGHT]
            case "/", Direction.DOWN:
                dirs = [Direction.LEFT]
            case "\\", Direction.LEFT:
                dirs = [Direction.UP]
            case "\\", Direction.RIGHT:
                dirs = [Direction.DOWN]
            case "\\", Direction.UP:
                dirs = [Direction.LEFT]
            case "\\", Direction.DOWN:
                dirs = [Direction.RIGHT]
            case "|", Direction.LEFT:
                dirs = [Direction.UP, Direction.DOWN]
            case "|", Direction.RIGHT:
                dirs = [Direction.UP, Direction.DOWN]
            case "-", Direction.UP:
                dirs = [Direction.LEFT, Direction.RIGHT]
            case "-", Direction.DOWN:
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

        res2 = 0
        for starting_transition in tqdm.tqdm(grid.starting_transitions()):
            energized = grid.calculate_energized(starting_transition)
            res2 = max(res2, len(energized))

        return Solution(res1, res2)


Solver.run()
