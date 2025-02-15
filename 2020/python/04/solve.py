import pathlib
import string
import typing


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


def iter_puzzle(puzzle_file) -> tuple[frozenset[complex], complex]:
    inp = puzzle_file.read_text().strip()
    yield from map(Passport.from_str, inp.split("\n" * 2))


def p1(puzzle_file):
    return sum(passport is not None for passport in iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return sum(
        passport.is_valid
        for passport in iter_puzzle(puzzle_file)
        if passport is not None
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
