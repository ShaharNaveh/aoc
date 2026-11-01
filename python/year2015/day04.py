import hashlib
import itertools
import unittest

from utils import Day, aoc_main


def find(skey: str, prefix: str):
    for index in itertools.count():
        s = hashlib.md5(f"{skey}{index}".encode()).hexdigest()
        if s.startswith(prefix):
            yield index


class Day04(Day[str]):
    def parse(self, input: str) -> str:
        return input.strip()

    def part1(self, parsed: str) -> int:
        return next(find(parsed, "0" * 5))

    def part2(self, parsed: str) -> int:
        return next(find(parsed, "0" * 6))


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day04()
        for input, expected in [("abcdef", 609043), ("pqrstuv", 1048970)]:
            with self.subTest(input=input):
                self.assertEqual(d.part1(d.parse(input)), expected)


if __name__ == "__main__":
    aoc_main(Day04)
