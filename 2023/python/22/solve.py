import dataclasses
import itertools
import operator
import pathlib


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Brick:
    _id: int
    cubes: frozenset[tuple[int, int, int]]
    lowest_z: int

    def fall(self):
        if self.on_ground:
            return self

        return Brick(
            self._id,
            frozenset((x, y, z - 1) for x, y, z in self.cubes),
            self.lowest_z - 1,
        )

    def is_intersects(self, other) -> bool:
        return bool(self.cubes & other.cubes)

    @property
    def on_ground(self) -> bool:
        return self.lowest_z == 1

    @classmethod
    def from_str(cls, line: str):
        start, end = (map(int, s.split(",")) for s in line.split("~"))
        dims = [l if l == r else range(l, r + 1) for l, r in zip(start, end)]

        match dims:
            case x, y, range() as r:
                cubes = frozenset((x, y, z) for z in r)
            case x, range() as r, z:
                cubes = frozenset((x, y, z) for y in r)
            case range() as r, y, z:
                cubes = frozenset((x, y, z) for x in r)
            case x, y, z:
                cubes = frozenset({(x, y, z)})

        lowest_z = getattr(dims[2], "start", dims[2])

        return cls(hash(line), cubes, lowest_z)


def settle_bricks(bricks: frozenset[Brick]) -> frozenset[Brick]:
    settled_bricks = []
    settled_cubes = set()

    for brick in sorted(bricks, key=operator.attrgetter("lowest_z")):
        cpos = brick
        while not (cpos.on_ground or ((npos := cpos.fall()).cubes & settled_cubes)):
            cpos = npos

        settled_bricks.append(cpos)
        settled_cubes |= cpos.cubes

    return frozenset(settled_bricks)


def build_support_layout(bricks: frozenset[Brick]) -> dict[int, frozenset[Brick]]:
    support_layout = {}
    for brick in sorted(bricks, key=operator.attrgetter("lowest_z")):
        if brick.on_ground:
            continue

        under = brick.fall()
        support_layout[brick._id] = frozenset(
            other._id
            for other in bricks
            if (brick._id != other._id) and under.is_intersects(other)
        )
    return support_layout


def iter_chain_reactions(
    bricks: frozenset[Brick], support_layout: dict[int, frozenset[Brick]]
):
    yield []
    for _id in map(operator.attrgetter("_id"), bricks):
        removed = {_id}

        while True:
            would_fall = {
                brick
                for brick, supporting in support_layout.items()
                if removed >= supporting
            }
            if len(would_fall) == len(removed) - 1:
                yield would_fall
                break
            removed |= would_fall


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Brick.from_str, inp.splitlines())


def p1(puzzle_file):
    bricks = frozenset(iter_puzzle(puzzle_file))
    settled_bricks = settle_bricks(bricks)
    support_layout = build_support_layout(settled_bricks)
    load = frozenset(
        itertools.chain(filter(lambda b: len(b) == 1, support_layout.values()))
    )
    return len(bricks) - len(load)


def p2(puzzle_file):
    bricks = frozenset(iter_puzzle(puzzle_file))
    settled_bricks = settle_bricks(bricks)
    support_layout = build_support_layout(settled_bricks)
    return sum(map(len, iter_chain_reactions(settled_bricks, support_layout)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
