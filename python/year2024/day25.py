import itertools

from utils import Day, aoc_main


def non_overlapping_pairs(locks, keys):
    for lock, key in itertools.product(locks, keys):
        if is_overlap(lock, key):
            continue
        yield lock, key


def is_overlap(lock, key):
    return any((a + b) > 5 for a, b in zip(lock, key, strict=True))


class Day25(Day):
    def parse(self, input: str):
        inp = input.strip()
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

    def part1(self, parsed):
        locks, keys = parsed
        res = sum(1 for _ in non_overlapping_pairs(locks, keys))
        return res


if __name__ == "__main__":
    aoc_main(Day25)
