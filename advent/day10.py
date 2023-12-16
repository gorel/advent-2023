# /usr/bin/env python3
from __future__ import annotations

import collections

import pydantic

from advent.base import BaseSolver, Solution
from advent.graph import Point


class Node(pydantic.BaseModel):
    p: Point
    val: str

    @property
    def neighbors(self) -> list[Point]:
        m = {
            "|": [(-1, 0), (1, 0)],
            "-": [(0, -1), (0, 1)],
            "L": [(-1, 0), (0, 1)],
            "J": [(-1, 0), (0, -1)],
            "7": [(0, -1), (1, 0)],
            "F": [(0, 1), (1, 0)],
            "S": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        }
        if self.val == ".":
            return []
        return [Point(self.p.row + x, self.p.col + y) for x, y in m[self.val]]


class Graph(pydantic.BaseModel):
    nodes: dict[Point, Node]
    rows: int
    cols: int
    start: Point

    def neighbors(self, p: Point) -> list[Point]:
        if p not in self.nodes:
            return []
        return self.nodes[p].neighbors

    def set_start(self) -> None:
        # First discover what kind of point S is
        possible = set()
        # Check up
        up = Point(self.start.row - 1, self.start.col)
        if self.start in self.neighbors(up):
            if len(possible) > 0:
                possible &= {"|", "7", "F"}
            else:
                possible = {"|", "7", "F"}
        # Check left
        left = Point(self.start.row, self.start.col - 1)
        if self.start in self.neighbors(left):
            if len(possible) > 0:
                possible &= {"-", "J", "7"}
            else:
                possible = {"-", "J", "7"}
        # Check right
        right = Point(self.start.row, self.start.col + 1)
        if self.start in self.neighbors(right):
            if len(possible) > 0:
                possible &= {"-", "L", "F"}
            else:
                possible = {"-", "L", "F"}
        # Check down
        down = Point(self.start.row + 1, self.start.col)
        if self.start in self.neighbors(down):
            if len(possible) > 0:
                possible &= {"|", "7", "F"}
            else:
                possible = {"|", "7", "F"}

        self.nodes[self.start].val = possible.pop()

    def part1(self) -> int:
        # Now fill outwards to find farthest point
        visited = set()
        res = 0
        queue: collections.deque[tuple[Point, int]] = collections.deque()
        queue.append((self.start, 0))
        while queue:
            p, dist = queue.popleft()
            if p in visited:
                continue
            visited.add(p)
            if dist > res:
                res = dist
            for neighbor in self.nodes[p].neighbors:
                queue.append((neighbor, dist + 1))
        return res

    def _ENHANCE(self) -> Graph:
        # Double the resolution of the graph so we can see "between" pipes
        nodes = {}
        start = Point(row=-1, col=-1)
        for row in range(self.rows):
            for col in range(self.cols):
                topleft = Point(row * 2, col * 2)
                topright = Point(row * 2, col * 2 + 1)
                bottomleft = Point(row * 2 + 1, col * 2)
                bottomright = Point(row * 2 + 1, col * 2 + 1)

                if self.start == Point(row, col):
                    start = topleft

                if self.nodes[Point(row, col)].val == ".":
                    nodes[topleft] = Node(p=topleft, val=".")
                    nodes[topright] = Node(p=topright, val=".")
                    nodes[bottomleft] = Node(p=bottomleft, val=".")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "L":
                    nodes[topleft] = Node(p=topleft, val="L")
                    nodes[topright] = Node(p=topright, val="-")
                    nodes[bottomleft] = Node(p=bottomleft, val=".")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "J":
                    nodes[topleft] = Node(p=topleft, val="J")
                    nodes[topright] = Node(p=topright, val=".")
                    nodes[bottomleft] = Node(p=bottomleft, val=".")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "7":
                    nodes[topleft] = Node(p=topleft, val="7")
                    nodes[topright] = Node(p=topright, val=".")
                    nodes[bottomleft] = Node(p=bottomleft, val="|")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "F":
                    nodes[topleft] = Node(p=topleft, val="F")
                    nodes[topright] = Node(p=topright, val="-")
                    nodes[bottomleft] = Node(p=bottomleft, val="|")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "|":
                    nodes[topleft] = Node(p=topleft, val="|")
                    nodes[topright] = Node(p=topright, val=".")
                    nodes[bottomleft] = Node(p=bottomleft, val="|")
                    nodes[bottomright] = Node(p=bottomright, val=".")
                elif self.nodes[Point(row, col)].val == "-":
                    nodes[topleft] = Node(p=topleft, val="-")
                    nodes[topright] = Node(p=topright, val="-")
                    nodes[bottomleft] = Node(p=bottomleft, val=".")
                    nodes[bottomright] = Node(p=bottomright, val=".")
        return Graph(nodes=nodes, rows=self.rows * 2, cols=self.cols * 2, start=start)

    def part2(self) -> int:
        g2 = self._ENHANCE()

        hull = set()
        queue: collections.deque[tuple[Point, int]] = collections.deque()
        queue.append((g2.start, 0))
        while queue:
            p, dist = queue.popleft()
            if p in hull:
                continue
            hull.add(p)
            for neighbor in g2.nodes[p].neighbors:
                queue.append((neighbor, dist + 1))

        internal = set()
        external = set()
        for row in range(g2.rows):
            for col in range(g2.cols):
                p = Point(row, col)
                if p in hull or p in internal or p in external:
                    continue

                new_visited, is_internal = g2._bfs(p, hull)
                if is_internal:
                    internal |= new_visited
                else:
                    external |= new_visited

        # Only count values that were part of the unenhanced grid.
        # Which is the "topleft" node in our 2x2 enhancement.
        # Everything else is a "false" node.
        res = 0
        for p in internal:
            if p.x % 2 == 0 and p.y % 2 == 0:
                res += 1
        return res

    def _bfs(self, p: Point, hull: set[Point]) -> tuple[set[Point], bool]:
        ok = True
        visited: set[Point] = set()
        q = collections.deque()
        q.append(p)
        while q:
            p = q.popleft()
            if p in visited:
                continue
            visited.add(p)
            for dxdy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_p = p + dxdy
                if new_p in hull:
                    # Hit a stopping point!
                    continue
                elif new_p not in self.nodes:
                    # Not enclosed!
                    ok = False
                    continue

                # Not a stopping point, keep going
                q.append(new_p)
        return visited, ok

    def display(self) -> None:
        m = {"L": "∟", "J": "┘", "7": "⏋", "F": "⌐"}
        for row in range(self.rows):
            for col in range(self.cols):
                orig = self.nodes[Point(row, col)].val
                val = m.get(orig, orig)
                print(val, end="")
            print()


class Solver(BaseSolver):
    def solve(self) -> Solution:
        nodes = {}
        start = Point(row=-1, col=-1)
        lines = self.data.splitlines()
        rows = len(lines)
        cols = len(lines[0]) if rows > 0 else 0
        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                p = Point(row=row, col=col)
                node = Node(p=p, val=c)
                nodes[p] = node
                if c == "S":
                    start = p

        g = Graph(nodes=nodes, rows=rows, cols=cols, start=start)
        g.set_start()
        g.display()
        res1 = g.part1()
        res2 = g.part2()

        return Solution(res1, res2)


Solver.run()
