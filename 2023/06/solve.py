import pathlib

def possible_race_ways(race: complex):
  race_time, distance_rec = int(race.real), int(race.imag)

  prev_distance = 0
  for hold in range(1, race_time):
    distance = hold * (race_time - hold)
    if distance_rec >= distance:
      if prev_distance > distance:
        break
      continue
    yield hold
    prev_distance = distance
      
def parse(path) -> set[complex]:
  puzzle = path.read_text().strip()
  time_line, distance_line = puzzle.splitlines()
  times = map(int, time_line.split(":")[1].strip().split())
  distances = map(int, distance_line.split(":")[1].strip().split())
  races = {complex(time, distance) for time, distance in zip(times, distances)}
  return races

def p1(path):
  races = parse(path)
  res = 1
  for race in races:
    res *= sum(1 for _ in possible_race_ways(race))
  print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
