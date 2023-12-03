import re
import strutils

type Solution = tuple[part1: int, part2: int]

proc extract(s: string, re: Regex, default: int = 0): int =
  var matches: array[1, string]
  if s.find(re, matches) != -1: matches[0].parseInt else: default

proc solve(): Solution =
  var
    res1 = 0
    res2 = 0
    rTotal = 12
    gTotal = 13
    bTotal = 14

  for game in stdin.lines:
    var
      possible = true
      minR = 0
      minG = 0
      minB = 0
    
    let game_and_rest = game.split(re":")
    let game_id = game_and_rest[0].split(re" ")[1].parseInt

    for s in game_and_rest[1].split(";"):
      let
        red = s.extract(re"(\d+) red")
        green = s.extract(re"(\d+) green")
        blue = s.extract(re"(\d+) blue")

      minR = max(minR, red)
      minG = max(minG, green)
      minB = max(minB, blue)
      if red > rTotal or green > gTotal or blue > bTotal:
        possible = false


    if possible:
      res1 += game_id
    res2 += minR * minG * minB

  (res1, res2)

echo solve()
