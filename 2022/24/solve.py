import functools
import heapq
import pathlib
import typing

###
import sys
from pprint import pprint
###


class Blizzard(typing.NamedTuple):
    pos: complex
    direction: complex


@functools.cache
def blizzard_at(blizzard: Blizzard, minute: int, bounds: complex) -> complex:
    x_offset = blizzard.direction.real * minute
    y_offset = blizzard.direction.imag * minute
    nx = (blizzard.pos.real - 1 + x_offset) % (bounds.real - 1) + 1
    ny = (blizzard.pos.imag - 1 + y_offset) % (bounds.imag - 1) + 1
    return complex(nx, ny)

@functools.cache
def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


@functools.cache
def is_oob(pos: complex, bounds: complex) -> bool:
    return (pos not in (1, bounds - 1)) and (
        (0 >= pos.real)
        or (pos.real >= bounds.real)
        or (0 >= pos.imag)
        or (pos.imag >= bounds.imag)
    )


class Branch(typing.NamedTuple):
    priority: int = float("inf")
    pos: complex = 1
    minute: int = 0

    def __lt__(self, other) -> int:
        return self.priority < other.priority


def walk(blizzards: frozenset[Blizzard], bounds: complex) -> int:
    end = bounds - 1

    pq = [Branch()]
    while pq:
        P_REMOVE_ME, pos, minute = heapq.heappop(pq)
        sys.stdout.write(f"\rpriority={P_REMOVE_ME:_} {minute=} {pos=} len={len(pq):_}")
        sys.stdout.flush()

        if pos == end:
            print()
            return minute

        for direction in (-1, 1, 1j, -1j, 0):
            npos = pos + direction
            nminute = minute + 1
            if is_oob(npos, bounds) or any(
                npos == blizzard_at(blizzard, nminute, bounds) for blizzard in blizzards
            ):
                continue
            priority = nminute + manhattan(npos, end)
            heapq.heappush(pq, Branch(priority=priority, pos=npos, minute=nminute))

    return min_minute


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
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


def p1(puzzle_file):
    return walk(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = puzzle_file.with_stem("test_puzzle")
# puzzle_file = puzzle_file.with_stem("small_test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
