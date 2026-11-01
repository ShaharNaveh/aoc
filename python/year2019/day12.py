import collections
import itertools
import math
import operator
import re
import typing
import unittest

from utils import Day, main


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

    def axis(self, idx: int) -> tuple[int, int]:
        return tuple(attr[idx] for attr in self)

    def find_vel_diff(self, other) -> Vec3:
        return Vec3(*itertools.starmap(cmp, zip(self.pos, other.pos)))

    def __add__(self, other) -> typing.Self:
        return Moon(*itertools.starmap(operator.add, zip(self, other)))

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        position = Vec3(*map(int, re.findall(r"-?\d+", raw)))
        return cls(position)


def simulate(moons: dict[int, Moon]):
    while True:
        nmoons = moons.copy()
        for (name1, moon1), (name2, moon2) in itertools.combinations(
            moons.items(), r=2
        ):
            vel_offset = moon1.find_vel_diff(moon2)
            nmoons[name1] += Moon(vel=-vel_offset)
            nmoons[name2] += Moon(vel=vel_offset)
        moons = {i: moon.moved for i, moon in nmoons.items()}
        yield moons


def predict(moons: dict[int, Moon]) -> int:
    states = collections.defaultdict(set)
    for moons in simulate(moons.copy()):
        nstates = {
            idx: tuple(moon.axis(idx) for moon in moons.values()) for idx in range(3)
        }

        if all(nstate in states[idx] for idx, nstate in nstates.items()):
            break

        for idx, nstate in nstates.items():
            states[idx].add(nstate)

    return math.lcm(*map(len, states.values()))


class Day12(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return dict(enumerate(map(Moon.from_str, inp.splitlines())))

    def part1(self, parsed):
        moons = next(
            moons for step, moons in enumerate(simulate(parsed), 1) if step == 1000
        )
        return sum(moon.energy for moon in moons.values())

    def part2(self, parsed):
        return predict(parsed)


TEST_PUZZLE = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


class Tests(unittest.TestCase):
    def test_part2_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 4686774924)


if __name__ == "__main__":
    main(Day12)
