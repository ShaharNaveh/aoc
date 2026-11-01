import re
import unittest

from utils import Day, aoc_main

BAG = "shiny gold"


def can_hold(bag: str, bags: dict[str, dict[int, str]]) -> bool:
    inner_bags = bags[bag]
    if BAG in inner_bags:
        return True
    return any(can_hold(inner_bag, bags) for inner_bag in inner_bags)


def hold_count(bag: str, bags: dict[str, dict[int, str]]) -> int:
    inner_bags = bags[bag]
    if not inner_bags:
        return 0
    return sum(inner_bags.values()) + sum(
        amount * hold_count(inner_bag, bags) for inner_bag, amount in inner_bags.items()
    )


class Day07(Day):
    def parse(self, input: str):
        inp = input.strip()

        return {
            bag: {
                name: int(amount)
                for amount, name in re.findall(r"(\d) (\w+ \w+)", raw_bags)
            }
            for line in inp.splitlines()
            for bag, raw_bags in re.findall(r"(\w+ \w+) bags contain (.*)", line)
        }

    def part1(self, bags):
        return sum(can_hold(bag, bags) for bag in bags)

    def part2(self, parsed):
        return hold_count(BAG, parsed)


TEST_PUZZLE = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day07()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 4)

    def test_part2_test_puzzle(self):
        d = Day07()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 32)


if __name__ == "__main__":
    aoc_main(Day07)
