import math
import unittest

from utils import Day, main


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def vaporize(station: complex, astroids: set[complex]):
    astroids = set(astroids) - {station}
    angles = {astroid: find_angle(station, astroid) for astroid in astroids}

    lst = sorted(angles.items(), key=lambda x: (x[1], manhattan(station, x[0])))
    idx = 0
    pos, angle = lst.pop(idx)
    yield pos
    while lst:
        if idx >= len(lst):
            idx, angle = 0, None

        if angle == lst[idx][1]:
            idx += 1
            continue

        pos, angle = lst.pop(idx)
        yield pos


def find_angle(src: complex, dest: complex) -> float:
    angle = math.atan2(dest.real - src.real, src.imag - dest.imag) * 180 / math.pi
    if angle >= 0:
        return angle
    return angle + 360


def find_best_location(astroids: frozenset[complex]) -> tuple[complex, int]:
    return max(
        {
            astroid: len(
                {find_angle(astroid, dest) for dest in astroids if dest != astroid}
            )
            for astroid in astroids
        }.items(),
        key=lambda x: x[1],
    )


class Day10(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return frozenset(
            complex(x, y)
            for y, row in enumerate(inp.splitlines())
            for x, char in enumerate(row)
            if char == "#"
        )

    def part1(self, parsed):
        return find_best_location(parsed)[1]

    def part2(self, astroids):
        station, _ = find_best_location(astroids)
        pos = next(
            pos for i, pos in enumerate(vaporize(station, astroids), 1) if i == 200
        )
        return int(pos.real * 100 + pos.imag)


TEST_PUZZLE = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""


class Tests(unittest.TestCase):
    DAY = Day10()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 210)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 802)


if __name__ == "__main__":
    main(Day10)
