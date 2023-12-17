# /usr/bin/env python3

import abc
import argparse
import dataclasses
import inspect
import logging
import pathlib
import time

import aocd

from advent.log import ColoredLogFormatter, green

Result = str | int


@dataclasses.dataclass
class Solution:
    part1: Result | None
    part2: Result | None


class BaseSolver(abc.ABC):
    def __init__(self, data: str, is_example: bool = False) -> None:
        self.logger = logging.getLogger()
        self.data = data
        self.is_example = is_example
        self.is_real = not is_example

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

    @classmethod
    def submit(cls, solution: Solution) -> None:
        if solution.part1 is not None:
            aocd.post.submit(solution.part1, part="a", day=cls.day, year=2023)
        if solution.part2 is not None:
            aocd.post.submit(solution.part2, part="b", day=cls.day, year=2023)

    @classmethod
    def run(cls) -> None:
        # Parse input
        parser = argparse.ArgumentParser()
        parser.add_argument("--part1", help="Part 1 example solution")
        parser.add_argument("--part2", help="Part 2 example solution")
        parser.add_argument("--no-submit", action="store_true", help="Don't submit")
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

            start = time.time()
            example_solution = cls(example_input, is_example=True).solve()
            elapsed = time.time() - start
            if args.part1 is not None and str(example_solution.part1) != args.part1:
                logger.fatal(f"Expected {args.part1}, but got {example_solution.part1}")
                exit(1)
            if args.part2 is not None and str(example_solution.part2) != args.part2:
                logger.fatal(f"Expected {args.part2}, but got {example_solution.part2}")
                exit(1)
            if args.part1 is not None or args.part2 is not None:
                logger.info(f"Example solution matches expected (took {elapsed:.2f}s)")
        else:
            logger.warning("No example input found")

        data = aocd.get_data(day=cls.day, year=2023)
        solver = cls(data)
        start = time.time()
        solution = solver.solve()
        elapsed = time.time() - start
        logger.info(green(f"Solution 1: {solution.part1}"))
        if solution.part2 is not None:
            logger.info(green(f"Solution 2: {solution.part2}"))
        logger.info(green(f"Took {elapsed:.2f}s"))
        print(green("-------------------------"))

        if not args.no_submit:
            solver.submit(solution)

    @property
    def lines(self) -> list[str]:
        return self.data.splitlines()

    @abc.abstractmethod
    def solve(self) -> Solution:
        ...
