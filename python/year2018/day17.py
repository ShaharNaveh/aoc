import collections
import re
import unittest

from utils import Day, run

type Grid = collections.defaultdict[complex, str]


def find_overflow(
    pos: complex, offset: complex, grid: Grid
) -> tuple[bool, int, list[complex]]:
    new_water_springs = []
    is_overflow = None
    while True:
        curr = grid[pos]
        below = grid[pos + 1j]
        match (curr, below):
            case "#", _:
                pos -= offset
                is_overflow = False
                break
            case _, ".":
                new_water_springs.append(pos)
                is_overflow = True
                break
            case "|", "|":
                is_overflow = True
                break

        pos += offset

    return is_overflow, int(pos.real), new_water_springs


def drop_water(grid: Grid):
    grid = grid.copy()
    min_x, max_x, min_y, max_y = find_bounds(grid)
    min_x, max_x = min_x - 1, max_x + 1

    water_springs = [500]
    while water_springs:
        pos = water_springs.pop()
        if max_x <= pos.real <= min_x:
            continue
        if grid[pos] == "~":
            continue

        npos = pos + 1j
        while npos.imag <= max_y:
            match grid[npos]:
                case ".":
                    grid[npos] = "|"
                    npos += 1j
                case "#" | "~":
                    npos -= 1j
                    is_loverflow, lx, lwater = find_overflow(npos, -1, grid)
                    is_roverflow, rx, rwater = find_overflow(npos, 1, grid)
                    water_springs.extend(lwater + rwater)
                    is_overflow = is_loverflow or is_roverflow
                    ntile = {True: "|", False: "~"}[is_overflow]
                    grid |= {
                        complex(x, npos.imag): ntile
                        for x in range(lx, rx + 1)
                        if max_x > x > min_x
                    }
                case "|":
                    break

    return grid


def find_bounds(grid: Grid) -> tuple[int, int, int, int]:
    xs = {pos.real for pos in grid}
    ys = {pos.imag for pos in grid}
    tup = (xs, ys)
    min_x, min_y = map(int, map(min, tup))
    max_x, max_y = map(int, map(max, tup))
    return min_x, max_x, min_y, max_y


class Day17(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        grid = collections.defaultdict(lambda: ".")
        for line in inp.splitlines():
            axis = line[0]
            axis_val, start, end = map(int, re.findall(r"\d+", line))
            axis_offset, pos_offset = (1, 1j) if axis == "x" else (1j, 1)
            for i in range(start, end + 1):
                pos = ((axis_val) * axis_offset) + (i * pos_offset)
                grid[pos] = "#"
        return grid

    def part1(self, parsed):
        grid = drop_water(parsed)
        _, _, min_y, max_y = find_bounds(grid)

        return sum(
            max_y > pos.imag > min_y for pos, tile in grid.items() if tile in ("|", "~")
        )

    def part2(self, parsed):
        grid = drop_water(parsed)
        _, _, min_y, max_y = find_bounds(grid)

        return sum(
            max_y > pos.imag > min_y for pos, tile in grid.items() if tile == "~"
        )


TEST_PUZZLE = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


class Tests(unittest.TestCase):
    def test_part2_test_puzzle(self):
        d = Day17()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 29)


if __name__ == "__main__":
    run(Day17)
