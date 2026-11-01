import hashlib
import itertools
import unittest

from utils import Day, main


def find(skey: str, prefix: str):
    for index in itertools.count():
        s = hashlib.md5(f"{skey}{index}".encode()).hexdigest()
        if s.startswith(prefix):
            yield index


class Day04(Day):
    def parse(self, inp: str) -> str:
        return inp.strip()

    def part1(self, parsed: str) -> int:
        return next(find(parsed, "0" * 5))

    def part2(self, parsed: str) -> int:
        return next(find(parsed, "0" * 6))


class Tests(unittest.TestCase):
    DAY = Day04()

    def test_part1(self):
        for inp, expected in [("abcdef", 609043), ("pqrstuv", 1048970)]:
            with self.subTest(inp=inp):
                self.assertEqual(self.DAY.part1(self.DAY.parse(inp)), expected)


if __name__ == "__main__":
    main(Day04)
