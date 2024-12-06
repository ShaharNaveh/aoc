import itertools
import pathlib

def parse_puzzle(path):
  inp = path.read_text().strip()
  return {
    (row_idx, col_idx): char
    for row_idx, row in enumerate(inp.splitlines())
    for col_idx, char in enumerate(row)
  }
  
def get_seen(cord, cords):
    dir_iter = itertools.cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    d = next(dir_iter)
    p = cord
    seen = set()
    while p in cords and (p, d) not in seen:
        seen.add((p, d))
        while cords.get((p[0] + d[0], p[1] + d[1])) == '#':
            d = next(dir_iter)
        p = (p[0] + d[0], p[1] + d[1])
    return seen, p in cords
  
def p1(path):
  cords = parse_puzzle(path)
  start_cord = next((cord for cord in cords if cords[cord] == "^"), None)
  seen, _ = get_seen(cord=start_cord, cords=cords)
  print(len(set(pos for pos, _ in seen)))

  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
