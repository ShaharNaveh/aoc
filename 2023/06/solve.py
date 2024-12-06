import pathlib


def parse(path) -> set[complex]:
  puzzle = path.read_text().strip()
  #time_line, distance_line = puzzle.splitlines()
  _, times, _, distances = puzzle.split(":")
  times = map(int, times.split())
  distances = map(int, distances.split())
  races = {complex(time, distance) for time, distance in zip(times, distances)}
  return races

def p1(path):
  races = parse(path)
  print(races)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
