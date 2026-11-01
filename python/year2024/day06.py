import enum
import itertools
import operator
import unittest

from utils import Day, main


@enum.unique
class Direction(complex, enum.Enum):
    North = (-1, 0)
    East = (0, 1)
    South = (1, 0)
    West = (0, -1)

    @classmethod
    def from_string(cls, char):
        mapping = {
            "^": cls.North,
            ">": cls.East,
            "<": cls.West,
            "v": cls.South,
        }
        return mapping[char.lower()]


def walked_cords(
    cord: complex, cords: dict[complex, str]
) -> tuple[set[tuple[complex, Direction]], bool]:
    directions = itertools.cycle(Direction)
    direction = next(directions)
    seen = set()
    while (cord in cords) and (cord, direction) not in seen:
        seen |= {(cord, direction)}

        while cords.get(cord + direction.value) == "#":
            direction = next(directions)
        cord = cord + direction.value

    return set(map(operator.itemgetter(0), seen)), (cord, direction) in seen


class Day06(Day):
    def parse(self, inp: str):
        inp = inp.strip().lower()
        grid = [list(line) for line in inp.splitlines()]

        cords = {}
        for row_idx, row in enumerate(grid):
            for col_idx, char in enumerate(row):
                cord = complex(row_idx, col_idx)
                cords[cord] = char
                if char not in {".", "#"}:
                    cords[cord] = "."  # If there's a guard there, it's walkable
                    guard = cord

        return {"guard": guard, "cords": cords}

    def part1(self, puzzle):
        cord, cords = puzzle["guard"], puzzle["cords"]
        seen, _ = walked_cords(cord, cords)
        return len(seen)

    def part2(self, puzzle):
        cord, cords = puzzle["guard"], puzzle["cords"]
        seen, _ = walked_cords(cord, cords)
        return sum(walked_cords(cord, (cords | {pos: "#"}))[1] for pos in seen) - 1


TEST_PUZZLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


class Tests(unittest.TestCase):
    DAY = Day06()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 41)


if __name__ == "__main__":
    main(Day06)
