import re
import unittest

from utils import Day, main


def do_fold(coords: set[complex], fold: complex) -> set[complex]:
    if fold.imag:
        bottom = {pos for pos in coords if pos.imag > fold.imag}
        coords -= bottom
        coords |= {complex(pos.real, (fold.imag * 2) - pos.imag) for pos in bottom}
    else:
        right = {pos for pos in coords if pos.real > fold.real}
        coords -= right
        coords |= {complex((fold.real * 2) - pos.real, pos.imag) for pos in right}

    return coords


class Day13(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        raw_coords, raw_folds = inp.split("\n" * 2)
        coords = {
            complex(*map(int, line.split(","))) for line in raw_coords.splitlines()
        }

        folds = [
            int(val) * {"x": 1, "y": 1j}[axis]
            for axis, val in re.findall(r"(\w)=(\d+)", raw_folds, re.MULTILINE)
        ]
        return coords, folds

    def part1(self, parsed):
        coords, folds = parsed
        return len(do_fold(coords, folds[0]))

    def part2(self, parsed):
        coords, folds = parsed
        for fold in folds:
            coords = do_fold(coords, fold)

        xs = {int(pos.real) for pos in coords}
        ys = {int(pos.imag) for pos in coords}

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        for y in range(min_y, max_y + 1):
            print(
                " ".join(
                    "#" if complex(x, y) in coords else "."
                    for x in range(min_x, max_x + 1)
                )
            )


TEST_PUZZLE = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day13()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 17)


if __name__ == "__main__":
    main(Day13)
