import unittest

from utils import Day, main


def snafu_to_decimal(raw: str) -> int:
    vals = {"=": -2, "-": -1}
    return sum(
        int(vals.get(char, char)) * (5**i) for i, char in enumerate(reversed(raw))
    )


def decimal_to_snafu(num: int) -> str:
    res = ""
    while num > 0:
        rem = num % 5
        if rem >= 3:
            res += {3: "=", 4: "-"}[rem]
            num += 5 - rem
        else:
            res += str(rem)

        num //= 5
    return res[::-1]


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.splitlines()


class Day25(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return decimal_to_snafu(sum(map(snafu_to_decimal, parsed)))


TEST_PUZZLE = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


class Tests(unittest.TestCase):
    DAY = Day25()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), "2=-1=0")


if __name__ == "__main__":
    main(Day25)
