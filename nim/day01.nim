import strutils
import tables

type Solution = tuple[part1: int, part2: int]

let NUMS = {
  "one": '1', 
  "two": '2',
  "three": '3',
  "four": '4',
  "five": '5',
  "six": '6',
  "seven": '7',
  "eight": '8',
  "nine": '9',
}.toTable

proc solve(): Solution =
  var
    res1 = 0
    res2 = 0

  for line in stdin.lines:
    var
      nums1: seq[char] = @[]
      nums2: seq[char] = @[]

    for i, c in line:
      if c.isDigit():
        nums1.add(c)
        nums2.add(c)

      for s, c in NUMS:
        if line[i ..< line.len].startsWith(s):
          nums2.add(c)
    res1 += (nums1[0] & nums1[^1]).parseInt
    res2 += (nums2[0] & nums2[^1]).parseInt

  (res1, res2)

echo solve()
