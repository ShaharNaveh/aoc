import collections
import dataclasses
import heapq
import unittest

from utils import Day, aoc_main


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


class Day12(Day):
    def parse(self, input: str):
        inp = input.strip()
        return {
            complex(x, y): char
            for y, line in enumerate(inp.splitlines())
            for x, char in enumerate(line)
        }

    def part1(self, grid):
        start = next(pos for pos, char in grid.items() if char == "S")
        return walk(grid, start)

    def part2(self, grid):
        return min(walk(grid, start) for start, char in grid.items() if char == "a")


TEST_PUZZLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 31)

    def test_part2_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 29)


if __name__ == "__main__":
    aoc_main(Day12)
