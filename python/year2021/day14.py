import collections
import unittest

from utils import Day, aoc_main


def solve(template: str, rules: dict[tuple[str, str], str], steps: int = 10) -> int:
    counter = collections.Counter(template)
    elements = collections.Counter(zip(template, template[1:]))
    for _ in range(steps):
        for tup, num in list(elements.items()):
            if not num:
                continue

            elements[tup] -= num
            out = rules[tup]

            l, r = tup
            elements[(l, out)] += num
            elements[(out, r)] += num

            counter[out] += num

    vals = counter.values()
    return max(vals) - min(vals)


class Day14(Day):
    def parse(self, input: str):
        inp = input.strip()
        template, raw_rules = inp.split("\n" * 2)
        rules = {
            tuple(k): v
            for k, v in map(lambda l: l.split(" -> "), raw_rules.splitlines())
        }
        return template, rules

    def part1(self, parsed):
        return solve(*parsed)

    def part2(self, parsed):
        return solve(*parsed, steps=40)


TEST_PUZZLE = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day14()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 1588)

    def test_part2_test_puzzle(self):
        d = Day14()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 2188189693529)


if __name__ == "__main__":
    aoc_main(Day14)
