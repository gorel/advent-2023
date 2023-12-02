# /usr/bin/env python3
import re

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
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


Solver.run()
