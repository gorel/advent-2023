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


class Solver:
    def __init__(self, data: str) -> None:
        self.logger = logging.getLogger()
        self.data = data

    def solve(self) -> Solution:
        return Solution(None, None)


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.handlers[0].setFormatter(ColoredLogFormatter())

    # Parse input
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example_path", type=pathlib.Path)
    parser.add_argument("--part1", help="Part 1 example solution")
    parser.add_argument("--part2", help="Part 2 example solution")
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
