import pathlib

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

def p1(path):
  inp = path.read_text().strip().lower()
  grid = [line.split() for line in inp.splitlines()]
  for col_idx, col in enumerate(grid):
    for row_idx, char in enumerate(col):
      if char == "x":
        print((col_idx, row_idx))
      

p1(input_file)
