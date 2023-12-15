# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class LensSet:
    def __init__(self) -> None:
        self.boxes = [[] for _ in range(256)]

    def hash(self, s: str) -> int:
        res = 0
        for char in s:
            res += ord(char)
            res *= 17
            res %= 256
        return res

    def apply(self, code: str) -> None:
        if "=" in code:
            self.set(code.split("=")[0], int(code.split("=")[1]))
        else:
            self.pop(code.split("-")[0])

    def set(self, label: str, focal_length: int) -> None:
        for i, (lab, _) in enumerate(self.boxes[self.hash(label)]):
            if lab == label:
                self.boxes[self.hash(label)][i] = (label, focal_length)
                return
        self.boxes[self.hash(label)].append((label, focal_length))

    def pop(self, label: str) -> None:
        for i, (l, _) in enumerate(self.boxes[self.hash(label)]):
            if l == label:
                self.boxes[self.hash(label)].pop(i)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        res1 = 0
        ls = LensSet()
        for code in self.data.strip().split(","):
            ls.apply(code)
            res1 += ls.hash(code)

        res2 = sum(
            i * j * focal_length
            for i, bucket in enumerate(ls.boxes, start=1)
            for j, (_, focal_length) in enumerate(bucket, start=1)
        )

        return Solution(res1, res2)


Solver.run()
