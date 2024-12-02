import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

grid = INPUT_FILE.read_text().splitlines()

symbol_pos = set()

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

        if cur_col < 0 or cur_col >= len(grid[cur_row]):
          continue

        if not grid[cur_row][cur_col].isdigit():
          continue

        while cur_col > 0 and grid[cur_row][cur_col - 1].isdigit():
          cur_col -= 1

        symbol_pos.add((cur_row, cur_col))
 
    
print(symbol_pos)
