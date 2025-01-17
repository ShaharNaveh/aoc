import dataclasses
import functools
import itertools
import operator
import pathlib
import random

@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Vec3:
    x: int = 0
    y: int = 0
    z: int = 0

    def __iter__(self):
        return iter(dataclasses.astuple(self))

    def __sub__(self, other):
        return Vec3(*(operator.sub(*pair) for pair in zip(self, other)))

    @classmethod
    def from_str(cls, s: str):
        return cls(*map(int, s.split(", ")))

@dataclasses.dataclass(order=True, slots=True)
class Hailstone:
    pos: Vec3
    velocity: Vec3
    slope: float = dataclasses.field(init=False)
    y_hit_at: float = dataclasses.field(init=False)

    def slow(self, rvx, rvy):
        return Hailstone(pos=self.pos, velocity=Vec3(self.velocity.x - rvx, self.velocity.y - rvy, self.velocity.z))

    def __post_init__(self):
        self.slope = self.velocity.y / self.velocity.x
        self.y_hit_at = self.pos.y - (self.pos.x * self.slope)

    def is_x_history(self, x: int) -> bool:
        if self.velocity.x > 0:
            return self.pos.x > x
        return x > self.pos.x

    def intersects_with(self, other):
        xi = (other.y_hit_at - self.y_hit_at) / (self.slope - other.slope)
        yi = self.y_hit_at + (self.slope * xi)
        return xi, yi

    @classmethod
    def from_str(cls, s: str):
        return cls(*map(Vec3.from_str, s.split(" @ ")))

def iter_possible_velocities(velocity, distance, rng: range):
    yield from (
        v
        for v in rng
        if (v != velocity) and ((distance % (v - velocity)) == 0)
    )

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Hailstone.from_str, inp.splitlines())

def p1(puzzle_file):
    BOUNDS_MIN = 200_000_000_000_000
    BOUNDS_MAX = 400_000_000_000_000

    hailstones = iter_puzzle(puzzle_file)
    res = 0
    for a, b in itertools.combinations(hailstones, 2):
        if a.slope == b.slope:
            continue

        xi, yi = a.intersects_with(b)
        if any(h.is_x_history(xi) for h in (a, b)):
            continue

        if all(BOUNDS_MIN <= i <= BOUNDS_MAX for i in (xi, yi)):
            res += 1

    return res

def p2(puzzle_file):
    hailstones = list(iter_puzzle(puzzle_file))
    all_velocities = set(
        itertools.chain.from_iterable(
            map(
                dataclasses.astuple,
                map(operator.attrgetter("velocity"), hailstones)
            )
        )
    )
    min_v, max_v = min(all_velocities), max(all_velocities)
    rng = range(min_v, max_v + 1)

    rock_dims = {}
    for dim in map(operator.attrgetter("name"), dataclasses.fields(Vec3)):
        common = functools.reduce(
            set.intersection,
            (
                set(
                    iter_possible_velocities(
                        velocity=getattr(a.velocity, dim),
                        distance=getattr(b.pos, dim) - getattr(a.pos, dim),
                        rng=rng,
                    )
                )
                for a, b in itertools.combinations(hailstones, 2)
                if getattr(a.velocity, dim) == getattr(b.velocity, dim)
            )
        )
        rock_dims[dim] = common.pop()

    rock_v = Vec3(**rock_dims)

    rvx, rvy, rvz = dataclasses.astuple(rock_v)
    a, b = random.sample(hailstones, 2)

    avx = a.velocity.x
    a = a.slow(rvx, rvy)
    b = b.slow(rvx, rvy)

    rx, ry = a.intersects_with(b)
    t = (rx - a.pos.x) / (avx - rvx)
    rz = a.pos.z + ((a.velocity.z - rvz) * t)

    return int(rx + ry + rz)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
