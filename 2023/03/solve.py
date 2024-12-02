import itertools
import pathlib

def read(path: pathlib.Path):
  yield from map(str.strip, path.read_text().splitlines())

def neighbors(x, y, *, size):
  x_bound, y_bound = size
  for x2 in range(x-1, x+2):
    for y2 in range(y-1, y+2):
      if not (-1 < x <= x_bound):
        continue
        
      if not (-1 < y <= y_bound):
        continue

      if not ((x != x2) or (y != y2)):
        continue
        
      if not (0 <= x2 <= x_bound):
        continue
        
      if not (0 <= y2 <= y_bound):
        continue

      yield (x, y)

      
    

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

schematic = [list(line) for line in read(INPUT_FILE)]
schematic_size = (sum(1 for _ in schematic[0]), len(schematic))

tmp = list(neighbors(5, 5, size=schematic_size))
print(tmp)
