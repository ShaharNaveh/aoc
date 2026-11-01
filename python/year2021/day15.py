import collections
import heapq
import itertools
import typing
import unittest

from utils import Day, main


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


class Day15(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {
            complex(x, y): int(val)
            for y, row in enumerate(inp.splitlines())
            for x, val in enumerate(row)
        }

    def part1(self, parsed):
        return walk(parsed)

    def part2(self, parsed):
        return walk(expand_grid(parsed))


TEST_PUZZLE = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


class Tests(unittest.TestCase):
    DAY = Day15()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 40)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 315)


if __name__ == "__main__":
    main(Day15)
