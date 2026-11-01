import functools
import unittest

from utils import Day, aoc_main


@functools.cache
def max_pos(seats_pos: frozenset[complex]) -> tuple[float, float]:
    x = max(p.real for p in seats_pos)
    y = max(p.imag for p in seats_pos)

    return x, y


@functools.cache
def find_neighs(
    pos: complex, seats_pos: frozenset[complex], *, is_p2: bool = False
) -> frozenset[complex]:
    offsets = (-1 - 1j, -1j, 1 - 1j, -1, 1, -1 + 1j, 1j, 1 + 1j)
    if not is_p2:
        return frozenset(pos + offset for offset in offsets) & seats_pos

    neighs = set()
    max_x, max_y = max_pos(seats_pos)

    for offset in offsets:
        npos = pos + offset
        while (max_x >= npos.real >= 0) and (max_y >= npos.imag >= 0):
            if npos in seats_pos:
                neighs.add(npos)
                break
            npos += offset

    return frozenset(neighs) & seats_pos


def simulate(seats: dict[complex, bool], *, is_p2: bool = False) -> int:
    seats_pos = frozenset(seats)
    before, after = {}, seats.copy()
    while True:
        if before == after:
            return sum(before.values())

        before = after.copy()
        for pos, is_occupied in before.items():
            if is_occupied:
                count = 0
                for npos in find_neighs(pos, seats_pos, is_p2=is_p2):
                    count += before[npos]
                    if count >= (4 + is_p2):
                        after[pos] = False
                        break
            else:
                after[pos] = all(
                    not before[npos]
                    for npos in find_neighs(pos, seats_pos, is_p2=is_p2)
                )


class Day11(Day):
    def parse(self, input: str):
        inp = input.strip()
        return {
            complex(x, y): False
            for y, row in enumerate(inp.splitlines())
            for x, char in enumerate(row)
            if char == "L"
        }

    def part1(self, parsed):
        return simulate(parsed)

    def part2(self, parsed):
        return simulate(parsed, is_p2=True)


TEST_PUZZLE = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 37)

    def test_part2_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 26)


if __name__ == "__main__":
    aoc_main(Day11)
