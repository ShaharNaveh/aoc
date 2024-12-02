import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

grid = INOUT_FILE.read_text().splitlines()

for r_idx, row in enumerate(grid):
  for c_idx, char in enumerate(row):
    if char.isdigit() or char == ".":
      continue
    # No we have a symbol
    for cur_row in (r_idx - 1, r_idx, r_idx + 1):
      for cur_col in (c_idx - 1, c_idx, c_idx + 1):
        # Check if we OOB
        if cur_row < 0 or cur_row >= len(grid):
          continue
        
    
