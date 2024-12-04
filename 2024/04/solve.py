import enum
import pathlib
from typing import NamedTuple

class Cord(NamedTuple):
  x: int
  y: int

class Direction(Cord ,enum.Enum):
  North = (-1, 0)
  South = (1, 0)
  West = (0, -1)
  East = (0, 1)
  Northwest = (-1, -1)
  Northeast = (-1, 1)
  Southwest = (1, -1)
  Southeast = (1, 1)
  
def is_xmas_in_direction(
  x_cord: Cord, 
  direction: Direction, 
  grid: list[list[str]], 
  bounds: Cord,
  char_map: dict[int, str],
) -> bool:
  x_bound, y_bound = bounds
  cord = x_cord
  for idx in range(len(char_map)):
    x, y = (cord.x + direction.value.x, cord.y + direction.value.y)
    
    if (x >= x_bound) or (y >= y_bound):
      return False
      
    if 0 > min(x, y):
      return False
      
    if char_map[idx] != grid[x][y]:
      return False
      
    cord = Cord(x=x, y=y)
      
  return True

def is_xmas(
  cord: Cord,  
  grid: list[list[str]], 
  bounds: Cord,
  chars: set[str],
  direction_pairs: list[tuple[Direction, Direction]],
) -> bool:
  x_bound, y_bound = bounds
  for dir1, dir2 in direction_pairs:
    x1, y1 = (cord.x + dir1.value.x, cord.y + dir1.value.y)
    x2, y2 = (cord.x + dir2.value.x, cord.y + dir2.value.y)

    if max(x1, x2) >= x_bound:
      return False
      
    if max(y1, y2) >= y_bound:
      return False

    if 0 > min(x1, y1, x2, y2):
      return False

    char1 = grid[x1][y1]
    char2 = grid[x2][y2]

    if char1 == char2:
      return False
      
    if not all(char in chars for char in {char1, char2}):
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
  char_map = {idx: char for idx, char in enumerate(list("mas"))}
  res = 0
  for start_cord in start_cords:
    for direction in Direction:
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

def p2(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]
  
  start_cords = set()  
  for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
      if char != "a":
        continue
      cord = Cord(x=row_idx, y=col_idx)
      start_cords.add(cord)

  bounds = Cord(x=len(grid[0]), y=len(grid))
  chars = {"m", "s"}
  direction_pairs = [
   (
     Direction.Northwest,
     Direction.Southeast,
   ),
   (
     Direction.Northeast,
     Direction.Southwest,
   ),
  ]
  res = 0
  for start_cord in start_cords:
    res += int(
      is_xmas(
        cord=start_cord,
        grid=grid,
        bounds=bounds,
        chars=chars,
        direction_pairs=direction_pairs,
      )
    )
  print(res)
      
input_file = pathlib.Path(__file__).parent / "input.txt"
#input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
p2(input_file)
