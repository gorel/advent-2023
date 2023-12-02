# /usr/bin/env python3

import abc
import argparse
import dataclasses
import inspect
import logging
import pathlib

import aocd

from advent.log import ColoredLogFormatter, green

Result = str | int


@dataclasses.dataclass
class Solution:
    part1: Result | None
    part2: Result | None


class BaseSolver(abc.ABC):
    def __init__(self, data: str) -> None:
        self.logger = logging.getLogger()
        self.data = data

    @classmethod
    @property
    def day(cls) -> int:
        filepath = pathlib.Path(inspect.getfile(cls))
        return int(filepath.stem.split("day")[1])

    @classmethod
    @property
    def example_path(cls) -> pathlib.Path:
        filepath = pathlib.Path(inspect.getfile(cls))
        return filepath.parent / "resources" / f"{filepath.stem}.txt"

    def submit(self, solution: Solution) -> None:
        if solution.part1 is not None:
            aocd.post.submit(solution.part1, part="a", day=self.day, year=2023)
        if solution.part2 is not None:
            aocd.post.submit(solution.part2, part="b", day=self.day, year=2023)

    @classmethod
    def run(cls) -> None:
        # Parse input
        parser = argparse.ArgumentParser()
        parser.add_argument("--part1", help="Part 1 example solution")
        parser.add_argument("--part2", help="Part 2 example solution")
        parser.add_argument(
            "-v", "--verbose", action="store_true", help="Verbose logging"
        )
        args = parser.parse_args()

        # Set up logging
        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
        logger = logging.getLogger()
        logger.handlers[0].setFormatter(ColoredLogFormatter())

        # Run example if it exists
        if cls.example_path.exists():
            logger.info(f"Reading example input from {cls.example_path}")
            with open(cls.example_path) as f:
                example_input = f.read()
            logger.debug("Read example input")

            example_solution = cls(example_input).solve()
            if args.part1 is not None and str(example_solution.part1) != args.part1:
                logger.fatal(f"Expected {args.part1}, but got {example_solution.part1}")
            if args.part2 is not None and str(example_solution.part2) != args.part2:
                logger.fatal(f"Expected {args.part2}, but got {example_solution.part2}")
            if args.part1 is not None or args.part2 is not None:
                logger.info("Example solution matches expected")
        else:
            logger.warning("No example input found")

        data = aocd.get_data(day=cls.day, year=2023)
        solver = cls(data)
        solution = solver.solve()
        logger.info(green(f"Solution 1: {solution.part1}"))
        if solution.part2 is not None:
            logger.info(green(f"Solution 2: {solution.part2}"))
        print(green("-------------------------"))

        solver.submit(solution)

    @abc.abstractmethod
    def solve(self) -> Solution:
        ...
        return Solution(None, None)
