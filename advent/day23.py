# /usr/bin/env python3

from advent.base import BaseSolver, Solution
from advent.graph import Point


class Solver(BaseSolver):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger.info("Precomputing graph edges")
        self.g = [[c for c in line] for line in self.lines]
        self.g_short_part1 = self.simplify_graph(part2=False)
        self.g_short_part2 = self.simplify_graph(part2=True)
        self.logger.info("Done precomputing graph edges")

    @property
    def rows(self) -> int:
        return len(self.g)

    @property
    def cols(self) -> int:
        return len(self.g[0])

    def at(self, p: Point) -> str:
        if 0 <= p.row < self.rows and 0 <= p.col < self.cols:
            return self.g[p.row][p.col]
        return "#"

    def valid_adj(self, p: Point, part2: bool = False) -> list[Point]:
        return [
            adj for adj in p.adjacent() if self.can_walk_between(p, adj, part2=part2)
        ]

    def simplify_graph(self, part2: bool = False) -> dict[Point, dict[Point, int]]:
        # Special case - the start and destination points are interesting
        g2: dict[Point, dict[Point, int]] = {}
        src = Point(0, 1)
        dst = Point(self.rows - 1, self.cols - 2)
        junctions = {src, dst}
        for row in range(self.rows):
            for col in range(self.cols):
                p = Point(row, col)
                # We hard-code part2=True to consider all possible adjacencies
                # Otherwise, imagine the following:
                #   0123456
                # 0 #v#####
                # 1 #.>...#
                # 2 #v###.#
                # 3 #.###..
                #
                # At point (1, 1), valid_adj == 2 since we can't travel "up"
                # the slope, but in fact, this *is* a junction.
                if len(self.valid_adj(p, part2=True)) > 2:
                    junctions.add(p)

        for junction in junctions:
            adj = self.get_adjacent_junctions(junctions, junction, part2)
            g2[junction] = adj
            # Optimization: if the junction has the destination in its adjacencies,
            # then it's *only* valid to travel to the destination from this junction.
            # Otherwise, traveling elsewhere will block our only path to the exit.
            if dst in adj:
                g2[junction] = {dst: adj[dst]}
        return g2

    def get_adjacent_junctions(
        self, junctions: set[Point], junction: Point, part2: bool = False
    ) -> dict[Point, int]:
        res = {}
        visited = {junction}
        for adj in self.valid_adj(junction, part2=part2):
            j2, dist = self.find_next_junction(adj, junctions, visited, part2)
            if dist != -1:
                res[j2] = dist + 1
        return res

    def find_next_junction(
        self,
        start: Point,
        dests: set[Point],
        visited: set[Point],
        part2: bool = False,
    ) -> tuple[Point, int]:
        if start in dests:
            return start, 0

        visited.add(start)
        for adj in self.valid_adj(start, part2=part2):
            if adj not in visited:
                junction, dist = self.find_next_junction(adj, dests, visited, part2)
                if dist != -1:
                    visited.remove(start)
                    return junction, dist + 1
        visited.remove(start)

        return Point(-1, -1), -1

    def can_walk_between(self, src: Point, dst: Point, part2: bool = False) -> bool:
        match self.at(dst):
            case "#":
                return False
            case ">":
                return part2 or src.col < dst.col
            case "<":
                return part2 or src.col > dst.col
            case "^":
                return part2 or src.row > dst.row
            case "v":
                return part2 or src.row < dst.row
            case _:
                return True

    def dfs(self, part2: bool = False) -> int:
        g = self.g_short_part2 if part2 else self.g_short_part1
        src = Point(0, 1)
        dst = Point(self.rows - 1, self.cols - 2)
        visited = set()
        return self._dfs_helper(g, src, dst, visited)

    def _dfs_helper(
        self,
        g: dict[Point, dict[Point, int]],
        src: Point,
        dst: Point,
        visited: set[Point],
    ) -> int:
        if src == dst:
            return 0

        node = g[src]
        visited.add(src)
        longest_path = -1
        for adj, dist in node.items():
            if adj not in visited:
                adj_path = self._dfs_helper(g, adj, dst, visited)
                if adj_path != -1:
                    longest_path = max(longest_path, adj_path + dist)
        visited.remove(src)

        return longest_path

    def solve(self) -> Solution:
        yield self.dfs()
        yield self.dfs(part2=True)


Solver.run()
