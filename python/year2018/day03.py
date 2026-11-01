import collections
import itertools
import re
import typing

from utils import Day, run


class Claim(typing.NamedTuple):
    id: int
    x: int
    y: int
    width: int
    height: int

    def iter_area(self) -> typing.Iterator[complex]:
        return frozenset(
            self.offset + pos
            for pos in itertools.starmap(
                complex, itertools.product(range(self.width), range(self.height))
            )
        )

    @property
    def offset(self) -> complex:
        return complex(self.x, self.y)

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        id_, x, y, width, height = map(int, re.findall(r"(\d+)", raw))
        return cls(id_, x, y, width, height)


def find_overlaps(
    claims: typing.Iterable[Claim],
) -> collections.defaultdict[complex, set[Claim]]:
    overlaps = collections.defaultdict(set)
    for claim in claims:
        for pos in claim.iter_area():
            overlaps[pos].add(claim)

    return overlaps


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(Claim.from_str, inp.splitlines())


class Day03(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(len(claims) >= 2 for claims in find_overlaps(parsed).values())

    def part2(self, parsed):
        claims = set(parsed)
        overlaps = find_overlaps(claims)
        return next(
            claim.id
            for claim in claims
            if all(len(overlaps[pos]) == 1 for pos in claim.iter_area())
        )


if __name__ == "__main__":
    run(Day03)
