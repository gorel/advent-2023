# /usr/bin/env python3
import argparse
import dataclasses
import logging
import pathlib

import aocd

from advent.log import ColoredLogFormatter, green


@dataclasses.dataclass
class Solution:
    part1: str | int | None
    part2: str | int | None


NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class Solver:
    def __init__(self, data: str) -> None:
        self.logger = logging.getLogger()
        self.data = data

    def solve1(self) -> int:
        res = 0
        for line in self.data.splitlines():
            num1 = None
            num2 = None
            for c in line:
                if num1 is not None:
                    break

                if c.isdigit():
                    num1 = c
                    break

            for c in line[::-1]:
                if c.isdigit():
                    num2 = c
                    break

            if num1 is None or num2 is None:
                self.logger.warning(f"Could not find two numbers in {line}")
                continue
            num = int(num1 + num2)
            res += num
        return res

    def solve2(self) -> int:
        res = 0
        for line in self.data.splitlines():
            num1 = None
            num2 = None
            for i, c in enumerate(line):
                if num1 is not None:
                    break

                if c.isdigit():
                    num1 = c
                    break

                for n in NUMS:
                    if line[i:].startswith(n):
                        num1 = str(NUMS.index(n) + 1)
                        break

            for i, c in enumerate(line[::-1]):
                if num2 is not None:
                    break

                i = len(line) - i - 1
                if c.isdigit():
                    num2 = c
                    break
                for n in NUMS:
                    if line[i:].startswith(n):
                        num2 = str(NUMS.index(n) + 1)
                        break

            if num1 is None or num2 is None:
                self.logger.warning(f"Could not find two numbers in {line}")
                continue
            num = int(num1 + num2)
            res += num
        return res

    def solve(self) -> Solution:
        return Solution(self.solve1(), self.solve2())


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.handlers[0].setFormatter(ColoredLogFormatter())

    # Parse input
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example_path", type=pathlib.Path)
    parser.add_argument("--part1", help="Part 1 example solution", type=int)
    parser.add_argument("--part2", help="Part 2 example solution", type=int)
    args = parser.parse_args()

    # Run example
    if args.example_path is not None:
        logger.info(f"Reading example input from {args.example_path}")
        with open(args.example_path) as f:
            example_input = f.read()
        logger.debug("Read example input")

        example_solver = Solver(example_input)
        example_solution = example_solver.solve()
        if args.part1 is not None and example_solution.part1 != args.part1:
            logger.fatal(f"Expected {args.part1}, but got {example_solution.part1}")
        if args.part2 is not None and example_solution.part2 != args.part2:
            logger.fatal(f"Expected {args.part2}, but got {example_solution.part2}")
        logger.info("Example solution matches expected")

    # Run solution
    logger.info("Reading input")
    day = int(pathlib.Path(__file__).stem.split("day")[1])
    data = aocd.get_data(day=day, year=2023)
    logger.debug(f"Read input for day {day}")

    logger.info("Running solver")
    solver = Solver(data)
    solution = solver.solve()
    print(green(f"Solution 1: {solution.part1}"))
    aocd.post.submit(solution.part1, part="a", day=day, year=2023)
    if solution.part2 is not None:
        print(green(f"Solution 2: {solution.part2}"))
        aocd.post.submit(solution.part2, part="b", day=day, year=2023)
