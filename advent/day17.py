# /usr/bin/env python3
from __future__ import annotations

import heapq

import pydantic

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Point
from advent.log import gray, green, yellow


class State(pydantic.BaseModel):
    cost: int
    p: Point
    heading: Direction
    sequential: int
    prev: Point | None = None

    def __lt__(self, other: State) -> bool:
        return self.cost < other.cost

    def __hash__(self):
        return hash((self.p, self.heading, self.sequential, self.cost))


class Grid(pydantic.BaseModel):
    g: list[list[int]]

    @property
    def rows(self) -> int:
        return len(self.g)

    @property
    def cols(self) -> int:
        return len(self.g[0])

    def inbounds(self, p: Point) -> bool:
        return 0 <= p.row < self.rows and 0 <= p.col < self.cols

    def at(self, p: Point) -> int:
        return self.g[p.row][p.col]

    def get_cache(self, start: Point) -> dict[Point, int]:
        best = {start: 0}
        to_see = {
            Point(row, col) for row in range(self.rows) for col in range(self.cols)
        }

        while len(to_see) > 0:
            p = min(to_see, key=lambda x: best.get(x, float("inf")))
            to_see.remove(p)
            for d in Direction:
                neighbor = p.move(d)
                if self.inbounds(neighbor):
                    new_cost = best[p] + self.at(neighbor)
                    if new_cost < best.get(neighbor, float("inf")):
                        best[neighbor] = new_cost
        return best

    def print_path(self, prev: dict[State, State | None], final_state: State) -> None:
        res = []
        res_points = {}
        cur = final_state
        while cur is not None:
            res.append(cur)
            res_points[cur.p] = cur
            cur = prev[cur]
        print(" => ".join(f"({s.p.row}, {s.p.col})" for s in reversed(res)))
        i = 1
        for row in range(self.rows):
            for col in range(self.cols):
                p = Point(row, col)
                if p == final_state.p:
                    print(green("O"), end="")
                elif p in res_points:
                    print(yellow(res[-i - 1].heading.ascii()), end="")
                    i += 1
                else:
                    print(gray(str(self.at(p))), end="")
            print()

    def get_upper_bound_path(self) -> int:
        i = 0
        total = 0
        cur = Point(0, 0)
        while cur != Point(self.rows - 1, self.cols - 1) and self.inbounds(cur):
            cur = cur.move([Direction.RIGHT, Direction.DOWN][i % 2])
            total += self.at(cur)
            i += 1
        return total

    def search_3(self, ultra: bool = False) -> int:
        min_sequential = 4 if ultra else 1
        max_sequential = 10 if ultra else 3
        p = Point(0, 0)
        target = Point(self.rows - 1, self.cols - 1)
        # We want to initially be able to turn either down or right into the grid.
        # Since we encode the current heading instead of "valid turns", we create these
        # two different starts since the first will allow us to turn right, and the
        # second will allow us to turn down. It's definitely possible to clean this up,
        # but after spending so much time here, it's good enough.
        start = State(cost=0, p=p, heading=Direction.DOWN, sequential=1)
        start2 = State(cost=0, p=p, heading=Direction.RIGHT, sequential=1)
        heap = [start, start2]
        visited = set()
        prev: dict[State, State | None] = {start: None, start2: None}

        while len(heap) > 0:
            state = heapq.heappop(heap)
            if state.p == target:
                self.print_path(prev, state)
                return state.cost
            elif (state.p, state.heading) in visited:
                continue

            visited.add((state.p, state.heading))

            for d2 in [state.heading.turn_left(), state.heading.turn_right()]:
                # Move [min, max] spaces in that direction now
                next_pos = state.p
                cur_cost = state.cost
                for seq in range(1, max_sequential + 1):
                    next_pos = next_pos.move(d2)
                    if self.inbounds(next_pos):
                        cur_cost += self.at(next_pos)
                        if seq >= min_sequential:
                            new_state = State(
                                cost=cur_cost, p=next_pos, heading=d2, sequential=seq
                            )
                            prev[new_state] = state
                            heapq.heappush(heap, new_state)

        return -1

    def search_dfs(self, ultra: bool = False) -> int:
        p = Point(0, 0)
        start = State(p=p, heading=Direction.RIGHT, sequential=1, cost=0)
        target = Point(self.rows - 1, self.cols - 1)
        upper_bound = self.get_upper_bound_path()
        upper_bound = min(upper_bound, 1021 if ultra else 755)
        print(f"Upper bound: {upper_bound}")
        cache = self.get_cache(target)
        print(f"Computed cache (cache size = {len(cache)})")
        prev: dict[State, State | None] = {start: None}

        stack = [start]
        visited = {start}
        res = upper_bound
        best_state = start
        i = 0
        while len(stack) > 0:
            i += 1
            if i % 1_000_000 == 0:
                print(f"Stack size (after {i//1_000_000}M iterations): {len(stack)}")
            state = stack.pop()
            if state.p == target:
                if state.cost < res:
                    print(f"New best: {state.cost}")
                    res = state.cost
                    best_state = state
                continue
            elif state.cost > res:
                continue

            # Continue forward, turn left, turn right
            # In ultra mode, we must move forward a minimum of 4 moves
            possible_turns = (0, 1, 3) if state.sequential >= 3 or not ultra else (0,)
            for turns in possible_turns:
                sequential = state.sequential + 1 if turns == 0 else 1
                d2 = state.heading
                for _ in range(turns):
                    d2 = d2.clockwise
                neighbor = state.p.move(d2)
                if not self.inbounds(neighbor):
                    continue

                s = State(
                    p=neighbor,
                    heading=d2,
                    sequential=sequential,
                    cost=state.cost + self.at(neighbor),
                )

                max_sequential = 10 if ultra else 3
                if (
                    s.sequential <= max_sequential
                    and s not in visited
                    # and s.cost + target.manhattan_dist(s.p) <= res
                    and s.cost + cache[s.p] - self.at(s.p) <= res
                ):
                    prev[s] = state
                    visited.add(s)
                    stack.append(s)

        self.print_path(prev, best_state)
        return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = Grid(g=[[int(x) for x in line] for line in self.lines])
        res1 = g.search_3()
        res2 = g.search_3(ultra=True)
        return Solution(res1, res2)


Solver.run()
