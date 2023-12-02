# /usr/bin/env python3

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def solve(self) -> Solution:
        res1 = 0
        res2 = 0
        for line in self.data.splitlines():
            nums1 = []
            nums2 = []
            for i, c in enumerate(line):
                if c.isdigit():
                    nums1.append(c)
                    nums2.append(c)

                for n in self.NUMS:
                    if line[i:].startswith(n):
                        nums2.append(str(self.NUMS.index(n) + 1))
            res1 += int(nums1[0] + nums1[-1])
            res2 += int(nums2[0] + nums2[-1])
        return Solution(res1, res2)


Solver.run()
