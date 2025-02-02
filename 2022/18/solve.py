import collections
import dataclasses
import enum
import itertools
import operator
import pathlib


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Vec3:
    x: int = 0
    y: int = 0
    z: int = 0

    def iter_neigh(self):
        yield from (
            self + Vec3(*offset)
            for offset in itertools.product(range(-1, 2), repeat=3)
            if offset.count(0) == 2
        )

    def __iter__(self):
        return iter(dataclasses.astuple(self))

    def __add__(self, other):
        return Vec3(*(operator.add(*pair) for pair in zip(self, other)))

    @classmethod
    def from_str(cls, raw: str):
        return cls(*map(int, raw.split(",")))


@enum.unique
class State(enum.Enum):
    Unreachable = enum.auto()
    Droplet = enum.auto()
    Reachable = enum.auto()


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Vec3.from_str, inp.splitlines())


def p1(puzzle_file):
    droplets = frozenset(iter_puzzle(puzzle_file))
    return sum(
        neigh not in droplets for droplet in droplets for neigh in droplet.iter_neigh()
    )


def p2(puzzle_file):
    droplets = frozenset(iter_puzzle(puzzle_file))
    grid = collections.defaultdict(lambda: State.Unreachable) | {
        droplet: State.Droplet for droplet in droplets
    }
    max_pos = (
        max(
            itertools.chain.from_iterable(map(dataclasses.astuple, droplets)),
            default=0,
        )
        + 1
    )

    seen = set()
    queue = [Vec3()]
    while queue:
        droplet = queue.pop()
        grid[droplet] = State.Reachable
        seen.add(droplet)

        for neigh in droplet.iter_neigh():
            if grid[neigh] != State.Unreachable:
                continue
            if neigh in seen:
                continue
            if any((-1 > pos) or (pos > max_pos) for pos in neigh):
                continue
            queue.append(neigh)

    return sum(
        grid[neigh] == State.Reachable
        for droplet in droplets
        for neigh in droplet.iter_neigh()
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
