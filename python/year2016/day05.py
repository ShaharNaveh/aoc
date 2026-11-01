import hashlib
import itertools
import unittest

from utils import Day, run


def find(door_id: str):
    for index in itertools.count():
        s = hashlib.md5(f"{door_id}{index}".encode()).hexdigest()
        if s.startswith("0" * 5):
            yield s[5], s[6]


class Day05(Day):
    def parse(self, inp: str) -> str:
        return inp.strip()

    def part1(self, parsed: str) -> str:
        return "".join(
            itertools.islice(
                map(lambda tup: tup[0], find(parsed)),
                8,
            )
        )

    def part2(self, parsed: str) -> str:
        buf = ["_"] * 8
        for pos, val in find(parsed):
            try:
                pos = int(pos)
            except ValueError:
                continue

            if pos > 7:
                continue

            if buf[pos] != "_":
                continue

            buf[pos] = val

            if "_" not in buf:
                break

        return "".join(buf)


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day05()
        self.assertEqual(d.part1(d.parse("abc")), "18f47a30")

    def test_part2(self):
        d = Day05()
        self.assertEqual(d.part2(d.parse("abc")), "05ace8e3")


if __name__ == "__main__":
    run(Day05)
