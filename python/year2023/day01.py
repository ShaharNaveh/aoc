import re
import unittest

from utils import Day, main


def solve_p1(lst):
    r = re.compile(r"\d")
    for word in lst:
        found = re.findall(r, word)
        res = found[0] + found[-1]
        yield int(res)


def solve_p2(lst):
    dct = {
        #    "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    joined = "|".join(dct)
    expr = rf"(?=(\d|{joined}))"
    r = re.compile(expr)

    for word in lst:
        found = re.findall(r, word)
        if len(found) > 1:
            first, *_, last = found
        else:
            first = last = found[0]
        res = dct.get(first, first) + dct.get(last, last)
        yield int(res)


class Day01(Day):
    def parse(self, inp: str) -> list[str]:
        return list(map(str.strip, inp.splitlines()))

    def part1(self, words: list[str]) -> int:
        return sum(solve_p1(words))

    def part2(self, words: list[str]) -> int:
        return sum(solve_p2(words))


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day01()
        example = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet"
        self.assertEqual(d.part1(d.parse(example)), 142)

    def test_part2(self):
        d = Day01()
        example = (
            "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n"
            "4nineeightseven2\nzoneight234\n7pqrstsixteen"
        )
        self.assertEqual(d.part2(d.parse(example)), 281)


if __name__ == "__main__":
    main(Day01)
