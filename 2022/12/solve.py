import collections
import dataclasses
import heapq
import pathlib

@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Branch:
    pos: complex = dataclasses.field(compare=False, default=0)
    dist: int = 0

def iter_neigh(pos):
    yield from (pos + offset for offset in (1, -1, 1j, -1j))

def can_step(src: str, dest: str) -> bool:
    src = "a" if src == "S" else src
    dest = "z" if dest == "E" else dest
    return ord(src) + 1 >= ord(dest)

def walk(grid, start):
    dists = collections.defaultdict(lambda: float("inf"))
    visited = set()
    branches = [Branch(start)]
    while branches:
        branch = heapq.heappop(branches)
        pos, dist = dataclasses.astuple(branch)

        src = grid[pos]
        if src == "E":
            return dist

        if pos in visited:
            continue
        visited.add(pos)

        ndist = dist + 1
        for npos in iter_neigh(pos):
            if npos in visited:
                continue

            if (dest := grid.get(npos)) is None:
                continue

            if not can_step(src, dest):
                continue

            if ndist > dists[npos]:
                continue
            dists[npos] = ndist
            heapq.heappush(branches, Branch(npos, ndist))
    return float("inf")

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): char
        for y, line in enumerate(inp.splitlines())
        for x, char in enumerate(line)
    }

def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    start = next(pos for pos, char in grid.items() if char == "S")
    return walk(grid, start)

def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return min(walk(grid, start) for start, char in grid.items() if char == "a")

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
