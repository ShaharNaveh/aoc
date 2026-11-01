import collections
import functools
import unittest

from utils import Day, main


def parse_rules(rule_block: str) -> dict[int, set[int]]:
    rules = map(
        lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()
    )

    result = collections.defaultdict(set)
    for rule in rules:
        before, after = int(rule.real), int(rule.imag)
        result[before] |= {after}

    return dict(result)


def is_update_correct(update: list[int], rules: dict[int, set[int]]) -> bool:
    for idx, num in enumerate(update):
        befores = set(update[:idx])
        afters = rules.get(num, set())
        if befores & afters:
            return False
    return True


def fix_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    func = lambda before, after: (before in rules.get(after, set())) - 1
    res = sorted(update, key=functools.cmp_to_key(func))
    return res


def middle_page(update: list[int]) -> int:
    idx = (len(update) - 1) // 2
    return update[idx]


class Day05(Day):
    def parse(self, inp: str) -> str:
        return inp

    def part1(self, puzzle):
        inp = puzzle.strip()
        rule_block, update_block = inp.split("\n" * 2)

        rules = parse_rules(rule_block)
        updates = [
            list(map(int, line.split(","))) for line in update_block.splitlines()
        ]

        good_updates = filter(lambda update: is_update_correct(update, rules), updates)
        res = sum(map(middle_page, good_updates))
        return res

    def part2(self, puzzle):
        inp = puzzle.strip()
        rule_block, update_block = inp.split("\n" * 2)

        rules = parse_rules(rule_block)
        updates = [
            list(map(int, line.split(","))) for line in update_block.splitlines()
        ]

        bad_updates = filter(
            lambda update: not is_update_correct(update, rules), updates
        )
        fixed_updates = map(lambda update: fix_update(update, rules), bad_updates)
        res = sum(map(middle_page, fixed_updates))
        return res


TEST_INPUT = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


class Tests(unittest.TestCase):
    def test_part1_test_input(self):
        d = Day05()
        self.assertEqual(d.part1(d.parse(TEST_INPUT)), 143)

    def test_part2_test_input(self):
        d = Day05()
        self.assertEqual(d.part2(d.parse(TEST_INPUT)), 123)


if __name__ == "__main__":
    main(Day05)
