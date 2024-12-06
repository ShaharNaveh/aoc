import pathlib


def parse_puzzle(path):
  inp = path.read_text().strip()
  grid = [list(line) for line in inp.splitlines()]
  
  for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
      if char != "x":
        continue
      cord = Cord(x=row_idx, y=col_idx)
      start_cords.add(cord)
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
