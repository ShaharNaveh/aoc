import functools
import pathlib

def parse_puzzle(path):
  inp = path.read_text().strip()
  return {
    (row_idx, col_idx): char
    for row_idx, row in enumerate(inp.splitlines())
    for col_idx, char in enumerate(row)
  }
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
