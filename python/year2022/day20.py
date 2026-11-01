import collections
import unittest

from utils import Day, aoc_main


def mix(lst: list[int], multiplier: int = 1, times: int = 1) -> int:
    items = list(enumerate(map(lambda n: n * multiplier, lst)))
    items_len = len(items)
    deque = collections.deque(items)
    zero_item = None

    for _ in range(times):
        for item in items:
            num = item[1]
            if (zero_item is None) and (num == 0):
                zero_item = item

            deque.rotate(-deque.index(item))
            deque.popleft()

            rotate = num % (items_len - 1)
            deque.rotate(-rotate)
            deque.appendleft(item)

    deque.rotate(-deque.index(zero_item))
    return sum(deque[i * 1000 % items_len][1] for i in range(1, 4))


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day20(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return mix(list(parsed))

    def part2(self, parsed):
        return mix(list(parsed), 811_589_153, 10)


TEST_PUZZLE = """\
1
2
-3
3
-2
0
4"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day20()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 3)

    def test_part2_test_puzzle(self):
        d = Day20()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 1623178306)


if __name__ == "__main__":
    aoc_main(Day20)
