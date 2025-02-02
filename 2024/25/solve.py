import itertools
import pathlib


def non_overlapping_pairs(locks, keys):
    for lock, key in itertools.product(locks, keys):
        if is_overlap(lock, key):
            continue
        yield lock, key


def is_overlap(lock, key):
    return any((a + b) > 5 for a, b in zip(lock, key, strict=True))


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    locks = set()
    keys = set()
    for block in inp.split("\n" * 2):
        indicator, *lines, _ = block.splitlines()
        char = indicator[0]
        data = tuple(zipped.count("#") for zipped in zip(*lines))
        if char == "#":
            locks.add(data)
        else:
            keys.add(data)
    return locks, keys


def p1(puzzle_file):
    locks, keys = parse_puzzle(puzzle_file)
    res = sum(1 for _ in non_overlapping_pairs(locks, keys))
    return res


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")
print(p1(puzzle_file))
