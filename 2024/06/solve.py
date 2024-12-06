import enum
import operator
import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from collections.abc import Iterable

@enum.unique
class Direction(complex, enum.Enum):
  North = (-1, 0)
  South = (1, 0)
  West = (0, -1)
  East = (0, 1)

  @classmethod
  def rotate(cls, direction):
    """
    Rotate 90 degrees.
    """
    mapping = {
      cls.North: cls.East,
      cls.East: cls.South,
      cls.South: cls.West,
      cls.West: cls.North,
    }
    return mapping[direction]

  @classmethod
  def from_char(cls, char):
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
      cords[cord] = char == "."
      if char not in {".", "#"}:
        cords[cord] = True # If there's a guard there, it's walkable
        guard["direction"] = Direction.from_char(char)
        guard["cord"] = cord
  return {"guard": guard, "cords": cords}

def walk_until(
  cord: complex, direction: Direction, cords: dict[complex, bool]
) -> "Iterable[complex]":
  """
  Walk until reach obstacle or OOB
  """
  cord += direction.value
  while cords.get(cord, False):
    yield cord
    cord += direction.value
    
def patrol(
  cord: complex, direction: Direction, cords: dict[complex, bool]
) -> "Iterable[complex]":
  
  
  
def p1(path):
  puzzle = parse_puzzle(path)
  guard, cords = puzzle["guard"], puzzle["cords"]
  cord, direction = guard["cord"], guard["direction"]
  for idx, cord in enumerate(walk_until(**guard, cords=cords)):
    print(idx)
    print(cord)
    
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
