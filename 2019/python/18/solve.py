import functools
import heapq
import itertools
import pathlib
import typing


@functools.cache
def find_neighbors(pos: complex) -> frozenset[complex]:
    return frozenset(pos + offset for offset in (1, -1, 1j, -1j))


class Branch(typing.NamedTuple):
    robots: tuple[complex, ...]
    keys: frozenset[str] = frozenset()
    cost: int = 0

    @property
    def key(self) -> tuple[tuple[complex, ...], frozenset[str]]:
        return self.robots, self.keys

    def __lt__(self, other) -> bool:
        return self.cost < other.cost


def solve(grid: dict[complex, str]) -> int:
    end = frozenset(tile for tile in grid.values() if tile.islower())
    robots = tuple(pos for pos, tile in grid.items() if tile == "@")
    seen = set()
    pq = [Branch(robots)]

    while pq:
        branch = heapq.heappop(pq)
        robots, keys, cost = branch

        if keys == end:
            return cost

        branch_key = branch.key
        if branch_key in seen:
            continue
        seen.add(branch_key)

        for i, pos in enumerate(robots):
            for npos, distance, key in find_reachable_keys(pos, keys, grid):
                nrobots = list(robots)
                nrobots[i] = npos
                nrobots = tuple(nrobots)
                heapq.heappush(pq, Branch(nrobots, keys | {key}, cost + distance))


def find_reachable_keys(
    start_pos: complex, keys: frozenset[str], grid: dict[complex, str]
) -> typing.Iterator[tuple[complex, int]]:
    seen = set()
    pq = [Branch(start_pos, keys)]
    while pq:
        pos, _, cost = heapq.heappop(pq)
        if pos in seen:
            continue
        seen.add(pos)

        tile = grid[pos]
        if tile.islower() and (tile not in keys):
            yield pos, cost, tile
            continue

        for npos in find_neighbors(pos):
            ntile = grid.get(npos)
            if ntile is None:
                continue
            if ntile.isupper() and (ntile.lower() not in keys):
                continue
            heapq.heappush(pq, Branch(npos, keys, cost + 1))


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): tile
        for y, row in enumerate(inp.splitlines())
        for x, tile in enumerate(row)
        if tile != "#"
    }


def p1(puzzle_file):
    return solve(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    pos = next(pos for pos, tile in grid.items() if tile == "@")
    for neigh in find_neighbors(pos):
        grid.pop(neigh)
    grid.pop(pos)
    for offset in itertools.starmap(complex, itertools.product((-1, 1), repeat=2)):
        grid[pos + offset] = "@"
    return solve(grid)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
