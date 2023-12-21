# /usr/bin/env python3

import abc
import argparse
import inspect
import logging
import pathlib
import time
from typing import Generator

import aocd
from rich.console import RenderableType
from rich.live import Live

from advent.colors import blue, green
from advent.log import ColoredLogFormatter

Result = str | int
Solution = Generator[Result | None, None, None]


class BaseSolver(abc.ABC):
    def __init__(self, data: str, is_example: bool = False) -> None:
        self.logger = logging.getLogger()
        self.data = data
        self.is_example = is_example
        self.is_real = not is_example
        self.live = Live()

    @classmethod
    def day(cls) -> int:
        filepath = pathlib.Path(inspect.getfile(cls))
        return int(filepath.stem.split("day")[1])

    @classmethod
    def example_path(cls) -> pathlib.Path:
        filepath = pathlib.Path(inspect.getfile(cls))
        return filepath.parent / "resources" / f"{filepath.stem}.txt"

    def submit(self, part1: Result | None, part2: Result | None) -> None:
        self.logger.info("Submitting answers to Advent of Code")
        if part1 is not None:
            aocd.post.submit(part1, part="a", day=self.day(), year=2023)
        if part2 is not None:
            aocd.post.submit(part2, part="b", day=self.day(), year=2023)

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
        example_path = cls.example_path()
        if example_path.exists():
            logger.info(f"Reading example input from {example_path}")
            with open(example_path) as f:
                example_input = f.read()
            logger.debug("Read example input")

            start = time.time()
            example_solution = cls(example_input, is_example=True).solve()
            part1 = next(example_solution)
            elapsed = time.time() - start
            if args.part1 is not None and str(part1) != args.part1:
                logger.fatal(f"Expected {args.part1}, but got {part1}")
                exit(1)

            part2 = next(example_solution)
            if args.part2 is not None and str(part2) != args.part2:
                logger.fatal(f"Expected {args.part2}, but got {part2}")
                exit(1)
            if args.part1 is not None or args.part2 is not None:
                logger.info(f"Example solution matches expected (took {elapsed:.2f}s)")
        else:
            logger.warning("No example input found")

        data = aocd.get_data(day=cls.day(), year=2023)
        solver = cls(data)
        start = time.time()
        solution = solver.solve()
        part1 = next(solution)
        elapsed = time.time() - start
        s = green(f"Solution 1: {part1}") + blue(f" (took {elapsed:.2f}s)")
        logger.info(s)

        start = time.time()
        part2 = next(solution)
        if part2 is not None:
            elapsed = time.time() - start
            s = green(f"Solution 2: {part2}") + blue(f" (took {elapsed:.2f}s)")
            logger.info(s)
        print("-------------------------")

        if not args.no_submit:
            solver.submit(part1, part2)

    def show_state(self, state: RenderableType) -> None:
        self.live.update(state)

    @property
    def lines(self) -> list[str]:
        return self.data.splitlines()

    @abc.abstractmethod
    def solve(self) -> Solution:
        ...
