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


"""
Here be dragons. I was seeing how crazy I could make it by doing silly things like inlining the hash function.
class GolfedSolver(BaseSolver):
    def solve(self) -> Solution:
        B = [""] * 256
        m = {}
        for c in self.data.strip().split(","):
            if "=" in c:
                m[c.split("=")[0]] = int(c.split("=")[1])
                if f"{c.split('=')[0]}," not in B[(lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c.split("=")[0])]:
                    B[(lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c.split("=")[0])] += f"{c.split('=')[0]},"
            else:
                if f"{c.split('-')[0]}," in B[(lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c.split("-")[0])]:
                    B[(lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c.split("-")[0])] = B[(lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c.split("-")[0])].replace(
                        f"{c.split('-')[0]},", ""
                    )
                    del m[c.split("-")[0]]

        return Solution(
            sum((lambda s: (lambda r, s: [r := (r + ord(c)) * 17 % 256 for c in s][-1])(0, s))(c) for c in self.data.strip().split(",")),
            sum(
                i * j * m.get(l, 0)
                for i, box in enumerate(B, start=1)
                for j, l in enumerate(box[:-1].split(","), start=1)
            ),
        )
"""  # noqa


Solver.run()
