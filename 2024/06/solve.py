import pathlib


def parse_puzzle(path):
  inp = path.read_text().strip()
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
