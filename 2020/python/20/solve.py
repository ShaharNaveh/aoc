import collections
import math
import pathlib
import re
import typing


class Tile(typing.NamedTuple):
    id: int
    data: tuple[tuple[str, ...], ...]

    @property
    def rotated(self) -> typing.Self:
        rotated_data = tuple(zip(*reversed(self.data)))
        return self._replace(data=rotated_data)

    @property
    def flipped(self) -> typing.Self:
        flipped_data = tuple(tuple(reversed(row)) for row in self.data)
        return self._replace(data=flipped_data)

    @property
    def rotations(self) -> set[typing.Self]:
        res = {self}
        rotated_tile = self
        for _ in range(3):
            rotated_tile = rotated_tile.rotated
            res.add(rotated_tile)
        return res

    @property
    def top_side(self) -> str:
        return "".join(self.data[0])

    @property
    def all_tops(self) -> set[str]:
        return {rotated.top_side for rotated in self.rotations}

    def find_all_tops(self, with_flip: bool = True) -> set[str]:
        res = self.all_tops
        if with_flip:
            res |= self.flipped.all_tops
        return res

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        raw_id, *raw_data = raw.split("\n")
        _id = re.findall(r"Tile (\d+):", raw_id)[0]
        data = tuple(tuple(row) for row in raw_data)

        return cls(int(_id), data)


def iter_corners(
    tiles: frozenset[Tile], edges: collections.Counter
) -> typing.Iterator[Tile]:
    for tile in tiles:
        outside = len(
            [side for side in tile.find_all_tops(with_flip=False) if edges[side] == 1]
        )
        if outside != 2:
            continue
        yield tile


def solve(iterable: typing.Iterable[Tile], *, is_p2: bool = False) -> int:
    tiles = frozenset(iterable)
    edges = collections.Counter(
        top_side for tile in tiles for top_side in tile.find_all_tops()
    )

    corners = iter_corners(tiles, edges)
    if not is_p2:
        return math.prod(corner.id for corner in corners)

    image_size = int(math.sqrt(len(tiles)))


def iter_puzzle(puzzle_file) -> typing.Iterator[Tile]:
    inp = puzzle_file.read_text().strip()
    yield from map(Tile.from_str, inp.split("\n" * 2))


def p1(puzzle_file):
    return solve(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
