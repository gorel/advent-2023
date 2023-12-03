import std/tables
import std/sets
import std/strutils
import std/enumerate

type Solution = tuple[part1: int, part2: int]

proc parseInt(c: char): int = c.int - '0'.int

type Point = tuple[row: int, col: int]
type Node = tuple[value: int, adj: HashSet[Point]]
type Graph = tuple
  symbols: Table[Point, char]
  nodes: seq[Node]

proc adjacent8(p: Point): seq[Point] =
  for row in p.row - 1 .. p.row + 1:
    for col in p.col - 1 .. p.col + 1:
      if row != p.row or col != p.col:
        result.add((row, col))

proc parseGraph(input: string): Graph =
  var
    symbols = initTable[Point, char]()
    nodes: seq[Node] = @[]

  let lines = input.splitLines()
  for (row, line) in enumerate(lines):
    var
      inNum = false
      cur = 0
      curAdj: HashSet[Point]

    for (col, c) in enumerate(line):
      # First record the point of interest
      if not c.isDigit and c != '.':
        symbols[(row, col)] = c

      # Then record the numbers
      if c.isDigit:
        inNum = true
        cur = cur*10 + c.parseInt
        for point in (row, col).adjacent8():
          curAdj.incl(point)
      elif inNum:
        inNum = false
        nodes.add((cur, curAdj))
        cur = 0
        curAdj = initHashSet[Point]()

    if inNum:
      nodes.add((cur, curAdj))

  (symbols, nodes)


proc solve(): Solution =
  var
    res1 = 0
    res2 = 0
    gears: Table[Point, int]

  let g = parseGraph(stdin.readAll())
  for node in g.nodes:
    var
      added = false

    for adj in node.adj:
      if adj in g.symbols:
        if not added:
          res1 += node.value
          added = true
        if g.symbols[adj] == '*':
          if adj in gears:
            res2 +=  node.value * gears[adj]
          gears[adj] = node.value

  (res1, res2)

echo solve()
