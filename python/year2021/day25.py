import unittest

from utils import Day, main


def step(f: callable, typ: str, grid: dict[complex, str]) -> dict[complex, str]:
    return {
        npos if (((npos := f(pos)) not in grid) and (char == typ)) else pos: char
        for pos, char in grid.items()
    }


def solve(grid: dict[complex, str], bounds: complex) -> int:
    before, after = None, grid
    steps = 0
    while True:
        steps += 1

        before = after.copy()
        after = step(
            lambda pos: complex((pos.real + 1) % bounds.real, pos.imag), ">", after
        )
        after = step(
            lambda pos: complex(pos.real, (pos.imag + 1) % bounds.imag), "v", after
        )
        if before == after:
            return steps


class Day25(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        lines = inp.splitlines()
        bounds = complex(*map(len, (lines[0], lines)))
        grid = {
            complex(x, y): char
            for y, row in enumerate(lines)
            for x, char in enumerate(row)
            if char != "."
        }
        return grid, bounds

    def part1(self, parsed):
        return solve(*parsed)

    def part2(self, parsed):
        return


TEST_PUZZLE = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day25()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 58)


if __name__ == "__main__":
    main(Day25)
