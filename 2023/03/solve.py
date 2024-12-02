import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

grid = INOUT_FILE.read_text().splitlines()

for r_idx, row in enumerate(grid):
  for c_idx, char in enumerate(row):
    if char.isdigit() or char == ".":
      continue
    
