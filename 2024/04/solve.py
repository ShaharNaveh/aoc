import pathlib
from typing import NamedTuple

class Pos(NamedTuple):
  x: int
  y: int

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

def p1(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]
  bounds = Pos(x=len(grid[0]), y=len(grid))
  start_poses = set()
  
  for col_idx, col in enumerate(grid):
    for row_idx, char in enumerate(col):
      if char != "x":
        continue
      pos = Pos(x=col_idx, y=row_idx)
      start_poses.add(pos)

  print(start_poses)
      

p1(input_file)
