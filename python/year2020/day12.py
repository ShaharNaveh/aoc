import operator
import re
import typing
import unittest

from utils import Day, aoc_main

DIRECTIONS = list("ESWN")
ROTATIONS = {"L": operator.sub, "R": operator.add}


class Pos(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def move(self, direction: str, amount: int) -> "Pos":
        x, y = self
        match direction:
            case "N":
                y += amount
            case "S":
                y -= amount
            case "E":
                x += amount
            case "W":
                x -= amount
        return Pos(x, y)

    @property
    def distance(self) -> int:
        return sum(map(abs, self))


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    pattern = re.compile(r"(\w)(\d+)", re.MULTILINE)
    yield from map(lambda ins: (ins[0], int(ins[1])), pattern.findall(inp))


class Day12(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        pos = Pos()
        facing = "E"
        for direction, amount in parsed:
            match direction:
                case "F":
                    pos = pos.move(facing, amount)
                case "L" | "R":
                    op = ROTATIONS[direction]
                    cdirection = DIRECTIONS.index(facing)
                    idx = op(cdirection, amount // 90) % 4
                    facing = DIRECTIONS[idx]
                case _:
                    pos = pos.move(direction, amount)
        return pos.distance

    def part2(self, parsed):
        pos = Pos()
        wp = Pos(10, 1)
        for direction, amount in parsed:
            match direction:
                case "F":
                    nx = pos.x + (wp.x * amount)
                    ny = pos.y + (wp.y * amount)
                    pos = Pos(nx, ny)
                case "L" | "R":
                    amount //= 90
                    for _ in range(amount):
                        if direction == "L":
                            wp = Pos(-wp.y, wp.x)
                        else:
                            wp = Pos(wp.y, -wp.x)
                case _:
                    wp = wp.move(direction, amount)
        return pos.distance


TEST_PUZZLE = """\
F10
N3
F7
R90
F11"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 25)

    def test_part2_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 286)


if __name__ == "__main__":
    aoc_main(Day12)
