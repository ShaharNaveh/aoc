import collections
import heapq
import itertools
import pathlib
import typing


class Branch(typing.NamedTuple):
    pos: complex = 0
    cost: int = 0

    def __lt__(self, other) -> bool:
        return self.cost < other.cost


def expand_grid(grid, mul: int = 5):
    end = [*grid][-1]
    max_x, max_y = map(int, (end.real + 1, end.imag + 1))

    for pos, val in grid.copy().items():
        for nx, ny in itertools.product(range(mul), range(mul)):
            nval = val + nx + ny
            if nval > 9:
                nval = nval % 10 + 1

            xpos = int(pos.real) + max_x * nx
            ypos = int(pos.imag) + max_y * ny

            npos = complex(xpos, ypos)
            grid[npos] = nval
    return grid


def iter_neigh(pos: complex):
    yield from (pos + offset for offset in (1, -1, 1j, -1j))


def walk(grid):
    start = 0
    end = [*grid][-1]
    costs = collections.defaultdict(lambda: float("inf"))
    min_cost = float("inf")

    pq = [Branch()]

    while pq:
        pos, cost = heapq.heappop(pq)

        if cost >= costs[pos]:
            continue
        costs[pos] = cost

        if pos == end:
            min_cost = min(min_cost, cost)
            continue

        for neigh in iter_neigh(pos):
            if (risk_level := grid.get(neigh)) is None:
                continue

            ncost = cost + risk_level
            heapq.heappush(pq, Branch(neigh, cost + risk_level))

    return min_cost


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): int(val)
        for y, row in enumerate(inp.splitlines())
        for x, val in enumerate(row)
    }


def p1(puzzle_file):
    return walk(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return walk(expand_grid(parse_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
