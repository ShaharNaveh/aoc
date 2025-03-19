import collections
import itertools
import pathlib
import re
import typing


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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Claim.from_str, inp.splitlines())


def p1(puzzle_file):
    return sum(
        len(claims) >= 2 for claims in find_overlaps(iter_puzzle(puzzle_file)).values()
    )


def p2(puzzle_file):
    claims = set(iter_puzzle(puzzle_file))
    overlaps = find_overlaps(claims)
    return next(
        claim.id
        for claim in claims
        if all(len(overlaps[pos]) == 1 for pos in claim.iter_area())
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
