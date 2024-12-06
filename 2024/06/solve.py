import enum
import pathlib

class Direction(complex, enum.Enum):
  North = (-1, 0)
  South = (1, 0)
  West = (0, -1)
  East = (0, 1)
  
def parse_puzzle(path):
  inp = path.read_text().strip().lower()
  grid = [list(line) for line in inp.splitlines()]

  cords = {}
  guard = {}
  for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
      cord = complex(row_idx, col_idx)
      cords[cord] = char == "."
      if char in {"^", ">", "<", "v"}:
        cords[cord] = True
        guard["direction"] = char
        guard["cord"] = cord
  return {"guard": guard, "cords": cords}
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
