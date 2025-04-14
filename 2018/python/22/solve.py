import enum
import functools
import heapq
import itertools
import math
import pathlib
import re
import typing


@enum.unique
class Tool(enum.Flag):
    Neither = enum.auto()
    Torch = enum.auto()
    ClimbingGear = enum.auto()


@enum.unique
class Region(enum.IntEnum):
    Rocky = 0
    Wet = 1
    Narrow = 2

    @functools.cached_property
    def tools(self) -> Tool:
        if self == Region.Rocky:
            return Tool.Torch | Tool.ClimbingGear
        elif self == Region.Wet:
            return Tool.ClimbingGear | Tool.Neither
        else:
            return Tool.Torch | Tool.Neither


class Branch(typing.NamedTuple):
    pos: complex = 0
    minutes: int = 0
    tool: Tool = Tool.Torch

    def __lt__(self, other) -> bool:
        return self.minutes < other.minutes


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    depth, x, y = map(int, re.findall(r"\d+", inp))
    return complex(x, y), depth


@functools.cache
def find_neighbors(pos: complex) -> frozenset[complex]:
    return frozenset(
        filter(
            lambda p: all(dim >= 0 for dim in (p.real, p.imag)),
            (pos + offset for offset in (1, -1, 1j, -1j)),
        )
    )


@functools.cache
def find_geologic_index(pos: complex, target: complex, depth: int) -> int:
    if pos in (0, target):
        geologic_index = 0
    elif pos.imag == 0:
        geologic_index = pos.real * 16807
    elif pos.real == 0:
        geologic_index = pos.imag * 48271
    else:
        geologic_index = math.prod(
            find_erosion_level(pos - offset, target, depth) for offset in (1, 1j)
        )

    return int(geologic_index)


@functools.cache
def find_erosion_level(pos: complex, target: complex, depth: int) -> int:
    geologic_index = find_geologic_index(pos, target, depth) + depth
    return geologic_index % 20183


@functools.cache
def find_region_type(pos: complex, target: complex, depth: int) -> Region:
    return Region(find_erosion_level(pos, target, depth) % 3)


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def rescue(target: complex, depth: int) -> int:
    pq = [Branch()]
    seen = set()
    while pq:
        pos, minutes, tool = heapq.heappop(pq)

        key = (pos, tool)
        if key in seen:
            continue
        seen.add(key)

        if (pos == target) and (tool == Tool.Torch):
            return minutes

        region = find_region_type(pos, target, depth)
        nminutes = minutes + 7
        for ntool in (t for t in region.tools if not (t & tool)):
            heapq.heappush(pq, Branch(pos, nminutes, ntool))

        nminutes = minutes + 1
        for npos in find_neighbors(pos):
            nregion = find_region_type(npos, target, depth)
            if tool not in nregion.tools:
                continue
            heapq.heappush(pq, Branch(npos, nminutes, tool))


def p1(puzzle_file):
    target, depth = parse_puzzle(puzzle_file)
    x, y = map(int, (target.real, target.imag))
    return sum(
        find_region_type(pos, target, depth)
        for pos in itertools.starmap(
            complex, itertools.product(range(x + 1), range(y + 1))
        )
    )


def p2(puzzle_file):
    return rescue(*parse_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
