# /usr/bin/env python3

import joblib
import pydantic
import tqdm

from advent.base import BaseSolver, Solution


class ProblemLine(pydantic.BaseModel):
    s: str
    nums: list[int]

    def solutions(
        self,
        cache: dict[tuple[int, int, int], int] | None = None,
        nums_idx: int = 0,
        s_idx: int = 0,
        cur_run: int = 0,
        in_run: bool = False,
        choices: str = "",
    ) -> int:
        if cache is None:
            cache = {}

        key = (s_idx, nums_idx, cur_run)

        if key not in cache:
            if s_idx == len(self.s):
                # If we're in a run, check that we finished the last one
                if in_run and self.nums[nums_idx] == cur_run:
                    # Advance
                    nums_idx += 1
                cache[key] = 1 if nums_idx == len(self.nums) else 0
                return cache[key]

            char = self.s[s_idx]
            if char == ".":
                # Just ended the run
                if in_run and self.nums[nums_idx] != cur_run:
                    cache[key] = 0
                else:
                    # Start the next run
                    nums_idx = nums_idx + 1 if in_run else nums_idx
                    cache[key] = self.solutions(
                        cache=cache,
                        nums_idx=nums_idx,
                        s_idx=s_idx + 1,
                        cur_run=0,
                        in_run=False,
                        choices=choices,
                    )
            elif char == "#":
                # Continue the run
                if nums_idx >= len(self.nums) or cur_run + 1 > self.nums[nums_idx]:
                    cache[key] = 0
                else:
                    cache[key] = self.solutions(
                        cache=cache,
                        nums_idx=nums_idx,
                        s_idx=s_idx + 1,
                        cur_run=cur_run + 1,
                        in_run=True,
                        choices=choices,
                    )
            else:
                # Try both options (if either possible)
                res = 0
                if in_run:
                    # Try to end the run
                    if self.nums[nums_idx] == cur_run:
                        # Ending the run would work
                        res += self.solutions(
                            cache=cache,
                            nums_idx=nums_idx + 1,
                            s_idx=s_idx + 1,
                            cur_run=0,
                            in_run=False,
                            choices=choices + ".",
                        )
                    # Try to continue the run
                    if nums_idx < len(self.nums) and cur_run + 1 <= self.nums[nums_idx]:
                        # Continuing the run would work
                        res += self.solutions(
                            cache=cache,
                            nums_idx=nums_idx,
                            s_idx=s_idx + 1,
                            cur_run=cur_run + 1,
                            in_run=True,
                            choices=choices + "#",
                        )
                else:
                    # Try to start a new run
                    if nums_idx < len(self.nums) and cur_run + 1 <= self.nums[nums_idx]:
                        # Starting the run would work
                        res += self.solutions(
                            cache=cache,
                            nums_idx=nums_idx,
                            s_idx=s_idx + 1,
                            cur_run=cur_run + 1,
                            in_run=True,
                            choices=choices + "#",
                        )

                    # Try to continue the drought
                    # This option is *always* possible
                    res += self.solutions(
                        cache=cache,
                        nums_idx=nums_idx,
                        s_idx=s_idx + 1,
                        cur_run=0,
                        in_run=False,
                        choices=choices + ".",
                    )
                cache[key] = res
        return cache[key]

    def interpolate(self, choices: str) -> str:
        res = ""
        choice_idx = 0
        for char in self.s:
            if char == "?" and choice_idx < len(choices):
                res += choices[choice_idx]
                choice_idx += 1
            else:
                res += char
        return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        problems = []
        for line in self.lines:
            g, nums = line.split(" ")
            problems.append(ProblemLine(s=g, nums=[int(x) for x in nums.split(",")]))

        res1 = sum(
            joblib.Parallel(n_jobs=-1)(
                joblib.delayed(problem.solutions)() for problem in tqdm.tqdm(problems)
            )  # type: ignore
        )

        res2 = sum(
            joblib.Parallel(n_jobs=-1)(
                joblib.delayed(
                    ProblemLine(
                        s="?".join(problem.s for _ in range(5)),
                        nums=problem.nums * 5,
                    ).solutions
                )()
                for problem in tqdm.tqdm(problems)
            )  # type: ignore
        )

        return Solution(res1, res2)


Solver.run()
