import pathlib

input_file = pathlib.Path(__file__).parent / "puzzle.txt"
inp = input_file.read_text().strip()

grid = {
  i + j * 1j: c
  for i, r in enumerate(inp)
  for j, c in enumerate(r.strip())
}

start = min(p for p in grid if grid[p] == "^")

def walk(grid):
    pos, direction, seen = start, -1, set()
    while pos in grid and (pos, direction) not in seen:
        seen |= {(pos, direction)}
        if grid.get(pos + direction) == "#":
            direction *= -1j
        else:
          pos += direction
    return {p for p, _ in seen}, (pos, direction) in seen

path = walk(grid)[0]
print(
  len(path), sum(
    walk(grid | {o: "#"})[1]
    for o in path
  )
)
