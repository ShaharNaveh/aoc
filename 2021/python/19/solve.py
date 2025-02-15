import collections
import itertools
import operator
import pathlib
import re
import typing


class Vec3(typing.NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self: "Vec3", other: "Vec3") -> "Vec3":
        return type(self)(*itertools.starmap(operator.sub, zip(self, other)))

    def manhattan(self: "Vec3", other: "Vec3") -> int:
        return sum(abs(dist) for dist in self - other)

    @classmethod
    def from_str(cls, raw: str):
        return cls(*map(int, raw.split(",")))


def find_common(s0, s1) -> tuple[tuple[Vec3, ...], Vec3] | None:
    coord = []
    aligned = []
    found = set()
    for s0_dim in range(3):
        s0_vals = [beacon[s0_dim] for beacon in s0]
        for signed_int, s1_dim in itertools.product((1, -1), range(3)):
            if s1_dim in found:
                continue
            s1_vals = [beacon[s1_dim] * signed_int for beacon in s1]
            diffs = [
                s0_val - s1_val
                for s0_val, s1_val in itertools.product(s0_vals, s1_vals)
            ]
            diff, overlap_count = collections.Counter(diffs).most_common(1)[0]
            if overlap_count >= 12:
                break
        else:
            return None
        found.add(s1_dim)
        aligned.append([s1_val + diff for s1_val in s1_vals])
        coord.append(diff)
    return tuple(Vec3(*pos) for pos in zip(*aligned)), Vec3(*coord)


def solve(scanners):
    scanner0, *unaligned = scanners
    beacons = set()
    aligned = [scanner0]
    scanner_coords = {Vec3(0, 0, 0)}
    while aligned:
        s0 = aligned.pop()
        buf = []
        for s1 in unaligned:
            common = find_common(s0, s1)
            if common is None:
                buf.append(s1)
                continue
            s0_aligned, scanner_coord = common
            aligned.append(s0_aligned)
            scanner_coords.add(scanner_coord)
        unaligned = buf
        beacons.update(s0)
    return beacons, scanner_coords


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from (
        tuple(map(Vec3.from_str, raw_beacons.splitlines()))
        for raw_beacons in re.split(r"\s*--- scanner \d+ ---\s*", inp)
        if raw_beacons
    )


def p1(puzzle_file):
    beacons, _ = solve(iter_puzzle(puzzle_file))
    return len(beacons)


def p2(puzzle_file):
    _, coords = solve(iter_puzzle(puzzle_file))
    return max(a.manhattan(b) for a, b in itertools.combinations(coords, 2))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
