import enum
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
  Walk until reach obstacle or OOB.
  """
  steps = 0
  cord += direction.value
  while cords.get(cord, False):
    yield cord
    steps += 1
    cord += direction.value
  return steps    
    
def patrol(
  cord: complex, direction: Direction, cords: dict[complex, bool]
) -> "Iterable[complex]":
  seen = set()
  last_steps = None
  while last_steps != 0:
    walk = walk_until(cord, direction, cords)
    while True:
      try:
        step = next(walk)
        print(f"B {step=}")
      except StopIteration as err:
        last_steps = err.value
        break
      print(f"C {step=}")
      yield step
    cord = step
    direction = Direction.rotate(direction)  
  
def p1(path):
  puzzle = parse_puzzle(path)
  guard, cords = puzzle["guard"], puzzle["cords"]
  cord, direction = guard["cord"], guard["direction"]
  locations = set(patrol(cord, direction, cords))
  print(len(locations))
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
