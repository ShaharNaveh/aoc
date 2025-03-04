import itertools
import math
import operator
import pathlib
import re
import typing


def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


class Vec3(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other) -> typing.Self:
        return Vec3(*itertools.starmap(operator.add, zip(self, other)))

    def __neg__(self) -> typing.Self:
        return Vec3(*map(operator.neg, self))


class Moon(typing.NamedTuple):
    pos: Vec3 = Vec3()
    vel: Vec3 = Vec3()

    @property
    def energy(self) -> int:
        return math.prod(sum(map(abs, attr)) for attr in self)

    @property
    def moved(self) -> typing.Self:
        return self._replace(pos=self.pos + self.vel)

    def find_vel_diff(self, other) -> Vec3:
        return Vec3(*itertools.starmap(cmp, zip(self.pos, other.pos)))

    def __add__(self, other) -> typing.Self:
        return Moon(*itertools.starmap(operator.add, zip(self, other)))

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        position = Vec3(*map(int, re.findall(r"-?\d+", raw)))
        return cls(position)


def simulate(moons: dict[int, Moon], steps: int = 1000) -> int:
    for _ in range(steps):
        nmoons = moons.copy()
        for (name1, moon1), (name2, moon2) in itertools.combinations(
            moons.items(), r=2
        ):
            vel_offset = moon1.find_vel_diff(moon2)
            nmoons[name1] += Moon(vel=-vel_offset)
            nmoons[name2] += Moon(vel=vel_offset)
        moons = {i: moon.moved for i, moon in nmoons.items()}

    return sum(moon.energy for moon in moons.values())


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return dict(enumerate(map(Moon.from_str, inp.splitlines())))


def p1(puzzle_file):
    return simulate(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
