import itertools
import math
import pathlib
import re
import typing


class Point(typing.NamedTuple):
    x: int
    y: int
    z: int

    def __getitem__(self, name: str) -> int:
        return getattr(self, name)


class Cuboid(typing.NamedTuple):
    p1: Point
    p2: Point

    def __and__(self: "Cuboid", other: "Cuboid") -> "Cuboid | None":
        l = Point(*(max(self.p1[dim], other.p1[dim]) for dim in "xyz"))
        r = Point(*(min(self.p2[dim], other.p2[dim]) for dim in "xyz"))
        overlap = Cuboid(l, r)
        if overlap:
            return overlap

    def __len__(self) -> int:
        return math.prod(self.p2[dim] - self.p1[dim] for dim in "xyz")

    def __bool__(self) -> bool:
        return all(self.p1[dim] < self.p2[dim] for dim in "xyz")

    @classmethod
    def from_str(cls: "Cuboid", raw: str) -> "Cuboid":
        p1 = []
        p2 = []
        for pair in re.findall(r"(-?\d+)\.\.(-?\d+)", raw):
            l, r = map(int, pair)
            p1.append(l)
            p2.append(r + 1)

        return cls(*(Point(*points) for points in (p1, p2)))


class Step(typing.NamedTuple):
    on: bool
    cuboid: Cuboid

    @classmethod
    def from_str(cls: "Step", raw: str) -> "Step":
        action, raw_cuboid = raw.split()
        on = action == "on"
        cuboid = Cuboid.from_str(raw_cuboid)
        return cls(on, cuboid)


def run_steps(steps) -> int:
    placed = []
    volume = 0
    for step in reversed(list(steps)):
        if not step.on:
            placed.append(step.cuboid)
            continue

        overlaps = []
        for cuboid in placed:
            overlapping = cuboid & step.cuboid
            if overlapping is not None:
                overlaps.append(Step(True, overlapping))

        volume += len(step.cuboid) - run_steps(overlaps)
        placed.append(step.cuboid)
    return volume


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Step.from_str, inp.splitlines())


def p1(puzzle_file):
    init_region = Cuboid(Point(-50, -50, -50), Point(51, 51, 51))

    return run_steps(
        filter(
            lambda step: step is not None,
            map(
                lambda step: Step(step.on, overlap)
                if (overlap := (init_region & step.cuboid)) is not None
                else None,
                iter_puzzle(puzzle_file),
            ),
        )
    )


def p2(puzzle_file):
    return run_steps(iter_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")
# puzzle_file = puzzle_file.with_stem("test_puzzle_p2")

print(p1(puzzle_file))
print(p2(puzzle_file))
