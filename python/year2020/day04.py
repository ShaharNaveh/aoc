import string
import typing
import unittest

from utils import Day, main


class Passport(typing.NamedTuple):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: str | None = None

    @property
    def is_valid(self) -> bool:
        byr, iyr, eyr, hgt, hcl, ecl, pid, _ = self

        if any(
            int(field) not in range(*bounds)
            for field, bounds in (
                (byr, (1920, 2002 + 1)),
                (iyr, (2010, 2020 + 1)),
                (eyr, (2020, 2030 + 1)),
            )
        ):
            return False

        height, typ = hgt[:-2], hgt[-2:]
        height_ranges = {"cm": range(150, 193 + 1), "in": range(59, 76 + 1)}
        if not ((typ in height_ranges) and (int(height) in height_ranges[typ])):
            return False

        if not (
            hcl.startswith("#")
            and (len(hcl) == 6 + 1)
            and all(char in string.hexdigits for char in hcl.removeprefix("#"))
        ):
            return False

        if ecl not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            return False

        if not ((len(pid) == 9) and pid.isdigit()):
            return False

        return True

    @classmethod
    def from_str(cls: "Passport", raw: str) -> "Passport | None":
        line = raw.replace("\n", " ")
        if line.count(" ") != 6 + line.count("cid:"):
            return

        return Passport(**dict(map(lambda field: field.split(":"), line.split())))


def iter_puzzle(puzzle) -> tuple[frozenset[complex], complex]:
    inp = puzzle.strip()
    yield from map(Passport.from_str, inp.split("\n" * 2))


class Day04(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(passport is not None for passport in parsed)

    def part2(self, parsed):
        return sum(passport.is_valid for passport in parsed if passport is not None)


TEST_PUZZLE = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""


class Tests(unittest.TestCase):
    DAY = Day04()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 2)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 2)


if __name__ == "__main__":
    main(Day04)
