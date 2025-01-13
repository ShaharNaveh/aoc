import dataclasses
import heapq
import itertools
import pathlib

@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Branch:
    pos: complex = dataclasses.field(compare=False)
    steps: int = 0

def iter_neigh(pos: complex):
    yield from (pos + direction for direction in (1, -1, 1j, -1j))

def walk_all(start_pos: complex, plots: frozenset[complex]) -> dict[complex, int]:
    visited = {}
    pq = [Branch(start_pos)]
    while pq:
        branch = heapq.heappop(pq)
        pos, steps = dataclasses.astuple(branch)

        if pos in visited:
            continue
        visited[pos] = steps

        for npos in iter_neigh(pos):
            if npos in visited:
                continue
            if npos not in plots:
                continue
            heapq.heappush(pq, Branch(npos, steps + 1))
    return visited

def possible_plots(
    start_pos: complex, plots: frozenset[complex], max_steps: int = 64
) -> frozenset[complex]:
    possible = {start_pos}
    for _ in range(max_steps):
        possible = (
            set(
                itertools.chain.from_iterable(
                    iter_neigh(pos) for pos in possible
                )
            ) & plots
        )
    return possible

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    walkable = {
        complex(x, y): tile
        for y, line in enumerate(inp.splitlines())
        for x, tile in enumerate(line)
        if tile != "#"
    }

    return next(pos for pos, tile in walkable.items() if tile == "S"), frozenset(walkable)
    

def p1(puzzle_file):
    start_pos, plots = parse_puzzle(puzzle_file)
    return len(possible_plots(start_pos, plots))

def p2(puzzle_file):

    grid_size = len(puzzle_file.read_text().strip().splitlines())
    edge_steps = grid_size // 2
    num = (26_501_365 - edge_steps) // grid_size
    evens_num = num ** 2
    odds_num = (num + 1) ** 2

    start_pos, plots = parse_puzzle(puzzle_file)
    visited = walk_all(start_pos, plots)

    counter = {
        "even": {"edge": 0, "inner": 0},
        "odd": {"edge": 0, "inner": 0},
    }

    for steps in visited.values():
        parity = {True: "even", False: "odd"}[steps % 2 == 0]
        typ = {True: "edge", False: "inner"}[steps > edge_steps]
        counter[parity][typ] += 1

    return (
        (odds_num * sum(counter["odd"].values()))
        + (evens_num * sum(counter["even"].values()))
        - ((num + 1) * counter["odd"]["edge"])
        + (num * counter["even"]["edge"])
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
