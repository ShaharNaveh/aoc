import enum
import itertools
import operator
import pathlib

@enum.unique
class Direction(complex, enum.Enum):
  North = (-1, 0)
  East = (0, 1)
  South = (1, 0)
  West = (0, -1)

  @classmethod
  def from_string(cls, char):
    mapping = {
      "^": cls.North,
      ">": cls.East,
      "<": cls.West,
      "v": cls.South,
    }
    return mapping[char.lower()]
  
def parse_puzzle(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]

  cords = {}
  guard = {}
  for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
      cord = complex(row_idx, col_idx)
      cords[cord] = char
      if char not in {".", "#"}:
        cords[cord] = "." # If there's a guard there, it's walkable
        guard = cord
  return {"guard": guard, "cords": cords}

def walked_cords(cord: complex, cords: dict[complex, str]) -> tuple[set[tuple[complex, Direction]], bool]:
  directions = itertools.cycle(Direction)
  #direction = next(directions)
  direction = -1
  seen = set()
  while (cord in cords) and (cord, direction) not in seen:
    seen |= {(cord, direction)}
    if cords.get(cord + direction) == "#":
      direction *= -1j
    else:
      cord += direction

    '''
    while cords.get(cord + direction.value) == "#":
      direction = next(directions)
      
    cord = cord + direction.value
    '''
  return set(map(operator.itemgetter(0), seen)), (cord, direction) in seen
  
def p1(path):
  puzzle = parse_puzzle(path)
  cord, cords = puzzle["guard"], puzzle["cords"]
  seen, _ = walked_cords(cord, cords)
  print(len(seen))

def p2(path):
  puzzle = parse_puzzle(path)
  cord, cords = puzzle["guard"], puzzle["cords"]
  seen, _ = walked_cords(cord, cords)
  print(
    sum(
      walked_cords(cord, cords | {pos: "#"})[1]
      for pos in seen
    )
  )
  '''
  res = sum(
    map(
      operator.itemgetter(1),
      (
        walked_cords(cord, cords | {loc: "#"})
        for loc in locs
      )
    )
  )
  print(res)
  '''
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
