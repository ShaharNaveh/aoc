import collections
import functools
import re
import unittest

from utils import Day, run

"""
NOTE:
        2
    7       3
        1
    6       4
        5


      2   3
    
    7   1   4

      6   5

Is like:
    23
    714
     65

    72
    613
     54
"""


OFFSETS = {"w": -1 + 1j, "nw": 1j, "sw": -1, "e": 1 - 1j, "ne": 1, "se": -1j}


def find_black_tiles(tiles) -> frozenset[complex]:
    counter = collections.Counter(
        sum(OFFSETS[offset] for offset in tile) for tile in tiles
    )
    return frozenset(pos for pos, count in counter.items() if count % 2)


@functools.cache
def find_neighs(pos: complex) -> frozenset[complex]:
    return frozenset(pos + offset for offset in OFFSETS.values())


def flip_tiles(tiles: frozenset[complex], days: int = 100) -> int:
    for _ in range(days):
        ntiles = set()
        for pos in {neigh for tile in tiles for neigh in find_neighs(tile)}:
            if pos in ntiles:
                continue
            neighs = find_neighs(pos)
            adj_count = len(neighs & tiles)

            if ((pos in tiles) and ((adj_count == 0) or (adj_count > 2))) or (
                (pos not in tiles) and (adj_count != 2)
            ):
                continue
            ntiles.add(pos)

        tiles = frozenset(ntiles)

    return len(tiles)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    pattern = re.compile(r"(ne|nw|se|sw|e|w)")
    yield from map(pattern.findall, inp.splitlines())


class Day24(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return len(find_black_tiles(parsed))

    def part2(self, parsed):
        return flip_tiles(find_black_tiles(parsed))


TEST_PUZZLE = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day24()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 10)

    def test_part2_test_puzzle(self):
        d = Day24()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 2208)


if __name__ == "__main__":
    run(Day24)
