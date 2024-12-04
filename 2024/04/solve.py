import pathlib
from typing import NamedTuple

class Cord(NamedTuple):
  x: int
  y: int


def is_xmas_in_direction(
  x_cord: Cord, 
  direction: Cord, 
  grid: list[list[str]], 
  bounds: Cord,
  char_map: dict[int, str],
) -> bool:
  x_bound, y_bound = bounds
  cord = x_cord
  for idx in range(len(char_map)):
    cord = Cord(*tuple(map(sum,zip(cord,direction))))
    x, y = cord
    
    if (x >= x_bound) or (y >= y_bound):
      return False
      
    if 0 > min(x, y):
      return False
      
    if char_map[idx] != grid[x][y]:
      return False
      
  return True
  
def p1(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]
  
  start_cords = set()  
  for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
      if char != "x":
        continue
      cord = Cord(x=row_idx, y=col_idx)
      start_cords.add(cord)

  bounds = Cord(x=len(grid[0]), y=len(grid))
  directions = {
      (-1, 0), # North
      (1, 0), # South
      (0, -1), # West
      (0, 1), # East
      (-1, -1), # Northwest
      (-1, 1), # Northeast
      (1, -1), # Southwest
      (1, 1), # Southeast
  }
  directions = set(map(lambda x: Cord(*x), directions))
  char_map = {idx: char for idx, char in enumerate(list("mas"))}
  res = 0
  for start_cord in start_cords:
    for direction in directions:
      res += int(
        is_xmas_in_direction(
          x_cord=start_cord,
          direction=direction,
          grid=grid,
          bounds=bounds,
          char_map=char_map,
        )
      )
  print(res)
      
input_file = pathlib.Path(__file__).parent / "input.txt"
#input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
