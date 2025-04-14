import heapq
import pathlib
import re
import typing


class Vec3(typing.NamedTuple):
    x: int
    y: int
    z: int

    def distance_to(self: typing.Self, other) -> float:
        return sum(abs(b - a) for a, b in zip(self, other))


class Nanobot(typing.NamedTuple):
    pos: Vec3
    r: int

    def __and__(self: typing.Self, other) -> bool:
        return self.distance_to(other) <= self.r

    def distance_to(self: typing.Self, other) -> float:
        return self.pos.distance_to(other.pos)

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        *pos, r = map(int, re.findall(r"(-?\d+)", raw))
        return cls(Vec3(*pos), r)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return frozenset(map(Nanobot.from_str, inp.splitlines()))


def p1(puzzle_file):
    nanobots = parse_puzzle(puzzle_file)
    nanobot = max(nanobots, key=lambda x: x.r)
    return sum(nanobot & other for other in nanobots)


def p2(puzzle_file):
    pq = []
    for nanobot in parse_puzzle(puzzle_file):
        dist = sum(map(abs, nanobot.pos))
        heapq.heappush(pq, (max(0, dist - nanobot.r), 1))
        heapq.heappush(pq, (dist + nanobot.r + 1, -1))

    count = max_count = res = 0
    while pq:
        dist, offset = heapq.heappop(pq)
        count += offset
        if count > max_count:
            res = dist
            max_count = count
    return res


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
