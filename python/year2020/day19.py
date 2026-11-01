import re
import unittest

from utils import Day, aoc_main

T = "({})"


def build_pattern(
    rule: str, rules: dict[str, str], *, depth: int = 0, max_depth: int = 100
) -> str:
    if depth >= max_depth:
        return ""

    ndepth = depth + 1

    if "|" in rule:
        return T.format(
            "|".join(
                T.format(build_pattern(nrule, rules, depth=ndepth))
                for nrule in rule.split("|")
            )
        )
    elif " " in rule:
        return T.format(
            "".join(build_pattern(nrule, rules, depth=ndepth) for nrule in rule.split())
        )

    name = rules[rule]
    if name.isalpha():
        return name
    return build_pattern(name, rules, depth=ndepth)


class Day19(Day):
    def parse(self, input: str):
        inp = input.strip()
        raw_rules, raw_messages = inp.split("\n" * 2)

        rules = {
            name: rule.replace('"', "")
            for name, rule in re.findall(r"(\d+): (.*)", raw_rules, re.MULTILINE)
        }

        return rules, raw_messages.splitlines()

    def part1(self, parsed):
        rules, messages = parsed
        raw_pattern = build_pattern(rules["0"], rules)
        pattern = re.compile(f"^({raw_pattern})$")
        return sum(bool(pattern.search(message)) for message in messages)

    def part2(self, parsed):
        rules, messages = parsed
        raw_pattern = build_pattern(
            rules["0"], rules | {"8": "42 | 42 8", "11": "42 31 | 42 11 31"}
        )
        pattern = re.compile(f"^({raw_pattern})$")
        return sum(bool(pattern.search(message)) for message in messages)


TEST_PUZZLE = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day19()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 2)


if __name__ == "__main__":
    aoc_main(Day19)
