import pathlib
from typing import NamedTuple

class Cord(NamedTuple):
  x: int
  y: int

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

def p1(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]
  
  start_cords = set()  
  for col_idx, col in enumerate(grid):
    for row_idx, char in enumerate(col):
      if char != "x":
        continue
      cord = Cord(x=col_idx, y=row_idx)
      start_cords.add(cord)

  bounds = Cord(x=len(grid[0]), y=len(grid))
  directions = {
    (-1, 0), # West
    (1, 0), # East
  }
  res = 0
  for start_cord in start_cords:
    for direction in directions:
      pass
      

p1(input_file)
