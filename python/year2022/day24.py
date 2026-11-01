import functools
import heapq
import typing
import unittest

from utils import Day, main


class Blizzard(typing.NamedTuple):
    pos: complex
    direction: complex


@functools.cache
def blizzards_pos_at(
    blizzards: frozenset[Blizzard], minute: int, bounds: complex
) -> complex:
    def inner(blizzard: Blizzard) -> complex:
        x_offset = blizzard.direction.real * minute
        y_offset = blizzard.direction.imag * minute
        nx = (blizzard.pos.real + x_offset - 1) % (bounds.real - 1) + 1
        ny = (blizzard.pos.imag + y_offset - 1) % (bounds.imag - 1) + 1
        return complex(nx, ny)

    return frozenset(map(inner, blizzards))


@functools.cache
def is_oob(pos: complex, bounds: complex) -> bool:
    return (pos not in (1, bounds - 1)) and (
        (0 >= pos.real)
        or (pos.real >= bounds.real)
        or (0 >= pos.imag)
        or (pos.imag >= bounds.imag)
    )


class Branch(typing.NamedTuple):
    pos: complex = 1
    minute: int = 0

    def __lt__(self, other) -> bool:
        return self.minute < other.minute


def walk(
    *,
    initial_blizzards: frozenset[Blizzard],
    starting_minute: int,
    bounds: complex,
    start: complex,
    end: complex,
) -> int:
    seen = set()
    pq = [Branch(pos=start, minute=starting_minute)]
    while pq:
        branch = heapq.heappop(pq)

        pos, minute = branch
        if pos == end:
            return minute

        if branch in seen:
            continue
        seen.add(branch)

        nminute = minute + 1
        blizzards_pos = blizzards_pos_at(initial_blizzards, nminute, bounds)

        for direction in (-1, 1, 1j, -1j, 0):
            npos = pos + direction
            if is_oob(npos, bounds) or (npos in blizzards_pos):
                continue
            heapq.heappush(pq, Branch(pos=npos, minute=nminute))


class Day24(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        lines = inp.splitlines()
        max_x, max_y = len(lines[0]) - 1, len(lines) - 1

        bounds = complex(max_x, max_y)

        blizzards = set()
        for y, row in enumerate(lines):
            for x, tile in enumerate(row):
                if tile in "#.":
                    continue
                pos = complex(x, y)
                direction = {"<": -1, "^": -1j, ">": 1, "v": 1j}[tile]

                blizzard = Blizzard(pos=pos, direction=direction)
                blizzards.add(blizzard)

        return frozenset(blizzards), bounds

    def part1(self, parsed):
        blizzards, bounds = parsed
        return walk(
            initial_blizzards=blizzards,
            starting_minute=0,
            bounds=bounds,
            start=1,
            end=bounds - 1,
        )

    def part2(self, parsed):
        blizzards, bounds = parsed
        start, end = 1, bounds - 1
        pwalk = functools.partial(walk, initial_blizzards=blizzards, bounds=bounds)

        minute1 = pwalk(starting_minute=0, start=start, end=end)
        minute2 = pwalk(starting_minute=minute1, start=end, end=start)
        return pwalk(starting_minute=minute2, start=start, end=end)


TEST_PUZZLE = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day24()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 18)

    def test_part2_test_puzzle(self):
        d = Day24()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 54)


if __name__ == "__main__":
    main(Day24)
