import functools
import itertools
import json
import math
import unittest

from utils import Day, main


def compare_pair(left, right) -> bool:
    if right is None:
        return False

    if left is None:
        return True

    if all(isinstance(packet, int) for packet in (left, right)):
        if left == right:
            return None
        return right > left

    if all(isinstance(packet, list) for packet in (left, right)):
        for pair in itertools.zip_longest(left, right):
            if (res := compare_pair(*pair)) is not None:
                return res
        return None

    if isinstance(left, list):
        return compare_pair(left, [right])

    return compare_pair([left], right)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from (
        tuple(map(json.loads, pair.splitlines())) for pair in inp.split("\n" * 2)
    )


class Day13(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(idx for idx, pair in enumerate(parsed, 1) if compare_pair(*pair))

    def part2(self, parsed):
        divider_packets = [[[n]] for n in (2, 6)]
        packets = list(itertools.chain.from_iterable(parsed)) + divider_packets

        return math.prod(
            idx
            for idx, packet in enumerate(
                sorted(
                    packets,
                    key=functools.cmp_to_key(
                        lambda left, right: -1 if compare_pair(left, right) else 1
                    ),
                ),
                start=1,
            )
            if packet in divider_packets
        )


TEST_PUZZLE = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day13()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 13)

    def test_part2_test_puzzle(self):
        d = Day13()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 140)


if __name__ == "__main__":
    main(Day13)
