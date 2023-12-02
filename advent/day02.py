# /usr/bin/env python3
import argparse
import dataclasses
import logging
import pathlib
import re

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
        res1 = 0
        res2 = 0
        r, g, b = 12, 13, 14
        for game in self.data.splitlines():
            possible = True
            minr, ming, minb = 0, 0, 0
            game_str, rest = game.split(":")
            game_id = int(game_str.split(" ")[1])

            for s in rest.split(";"):
                red = int((re.findall(r"(\d+) red", s) or [0])[0])
                green = int((re.findall(r"(\d+) green", s) or [0])[0])
                blue = int((re.findall(r"(\d+) blue", s) or [0])[0])

                if red > r or green > g or blue > b:
                    possible = False

                minr = max(minr, red)
                ming = max(ming, green)
                minb = max(minb, blue)

            if possible:
                res1 += game_id
            res2 += minr * ming * minb

        return Solution(res1, res2)


def submit(solution: Solution, day: int) -> None:
    if solution.part1 is not None:
        aocd.post.submit(solution.part1, part="a", day=day, year=2023)
    if solution.part2 is not None:
        aocd.post.submit(solution.part2, part="b", day=day, year=2023)


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
        if args.part1 is not None and str(example_solution.part1) != args.part1:
            logger.fatal(f"Expected {args.part1}, but got {example_solution.part1}")
            exit(1)
        if args.part2 is not None and str(example_solution.part2) != args.part2:
            logger.fatal(f"Expected {args.part2}, but got {example_solution.part2}")
            exit(1)
        logger.info("Example solution matches expected")

    # Run solution
    logger.info("Reading input")
    day = int(pathlib.Path(__file__).stem.split("day")[1])
    data = aocd.get_data(day=day, year=2023)
    logger.debug(f"Read input for day {day}")

    logger.info("Running solver")
    solver = Solver(data)
    solution = solver.solve()
    logger.info(green(f"Solution 1: {solution.part1}"))
    if solution.part2 is not None:
        logger.info(green(f"Solution 2: {solution.part2}"))
    print(green("-------------------------"))

    submit(solution, day)
