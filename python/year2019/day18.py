import functools
import heapq
import itertools
import typing
import unittest

from utils import Day, main


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


class Day18(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {
            complex(x, y): tile
            for y, row in enumerate(inp.splitlines())
            for x, tile in enumerate(row)
            if tile != "#"
        }

    def part1(self, parsed):
        return solve(parsed)

    def part2(self, grid):
        pos = next(pos for pos, tile in grid.items() if tile == "@")
        for neigh in find_neighbors(pos):
            grid.pop(neigh)
        grid.pop(pos)
        for offset in itertools.starmap(complex, itertools.product((-1, 1), repeat=2)):
            grid[pos + offset] = "@"
        return solve(grid)


TEST_PUZZLE = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day18()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 86)


if __name__ == "__main__":
    main(Day18)
