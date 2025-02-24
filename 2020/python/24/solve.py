import collections
import functools
import pathlib
import re

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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    pattern = re.compile(r"(ne|nw|se|sw|e|w)")
    yield from map(pattern.findall, inp.splitlines())


def p1(puzzle_file):
    return len(find_black_tiles(iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return flip_tiles(find_black_tiles(iter_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
