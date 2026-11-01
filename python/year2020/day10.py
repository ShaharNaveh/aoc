import collections
import functools
import itertools
import unittest

from utils import Day, main


@functools.cache
def possible_combinations(adapter: int, adapters: frozenset[int]) -> int:
    can_connect = frozenset(filter(lambda x: 3 >= x - adapter >= 1, adapters))
    if not can_connect:
        return 1
    return sum(possible_combinations(nadapter, adapters) for nadapter in can_connect)


def sliding_window(iterable, n: int = 2):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day10(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        diffs = collections.defaultdict(int)
        for a, b in sliding_window(itertools.chain([0], sorted(parsed))):
            diffs[b - a] += 1
        diffs[3] += 1
        return diffs[1] * diffs[3]

    def part2(self, parsed):
        adapters = frozenset(parsed)
        return possible_combinations(0, adapters)


TEST_PUZZLE = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


class Tests(unittest.TestCase):
    DAY = Day10()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 220)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 19208)


if __name__ == "__main__":
    main(Day10)
