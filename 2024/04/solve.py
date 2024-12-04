import pathlib
from typing import NamedTuple

class Cord(NamedTuple):
  x: int
  y: int

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

is_xmas_in_direction
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
    Cord(*direction) for direction in {
      (-1, 0), # North
      (1, 0), # South
      (0, -1), # West
      (0, 1), # East
      (-1, -1), # Northwest
      (-1, 1), # Northeast
      (1, -1), # Southwest
      (1, 1), # Southeast
    }
  }
  
  res = 0
  for start_cord in start_cords:
    for direction in directions:
      res += int(
        is_xmas_in_direction(
          x_cord=start_cord,
          direction=direction,
          grid=grid,
          bounds=bounds,
        )
      )
  print(res)
      

p1(input_file)
