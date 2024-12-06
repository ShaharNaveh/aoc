import enum
import itertools
import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from collections.abc import Iterable

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

def walked_cords(cord, cords):
  directions = itertools.cycle(Direction)
  direction = next(directions)
  seen = set()
  while (cord in cords) and (cord, direction) not in seen:
    yield cord
    seen.add((cord, direction))
    
    while cords.get(cord + direction.value) == "#":
      direction = next(directions)
      
    cord = cord + direction.value
  
def p1(path):
  puzzle = parse_puzzle(path)
  cord, cords = puzzle["guard"], puzzle["cords"]
  locations = set(walked_cords(cord, cords))
  print(len(locations))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
