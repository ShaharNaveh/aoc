import collections
import itertools
import math
import pathlib
import re
import typing

MONSTER = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".splitlines()

MONSTER_POS = {
    (x, y) for y, row in enumerate(MONSTER) for x, char in enumerate(row) if char == "#"
}
MW = max(pos[0] for pos in MONSTER_POS) + 1
MH = max(pos[1] for pos in MONSTER_POS) + 1


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
    def orientations(self) -> set[typing.Self]:
        return self.rotations | self.flipped.rotations

    @property
    def top_side(self) -> str:
        return "".join(self.data[0])

    @property
    def left_side(self) -> str:
        return "".join(row[0] for row in self.data)

    @property
    def bottom_side(self) -> str:
        return "".join(self.data[-1])

    @property
    def right_side(self) -> str:
        return "".join(row[-1] for row in self.data)

    def __getitem__(self, item: str):
        return getattr(self, f"{item}_side")

    def __getattr__(self, attr: str):
        return self[attr]

    @property
    def all_tops(self) -> set[str]:
        return {rotated.top_side for rotated in self.rotations}

    @property
    def borderless(self) -> typing.Self:
        slc = slice(1, -1)
        borderless_data = tuple(tuple(row[slc]) for row in self.data[slc])
        return self._replace(data=borderless_data)

    def find_all_tops(self, with_flip: bool = True) -> set[str]:
        res = self.all_tops
        if with_flip:
            res |= self.flipped.all_tops
        return res

    def align_to_edges(
        self, edges: dict[str, int], sides: tuple[str, ...]
    ) -> typing.Self:
        rotated_tile = self
        while any(edges[rotated_tile[side]] != 1 for side in sides):
            rotated_tile = rotated_tile.rotated
        return rotated_tile

    def find_orientation(self, side: str, target: str) -> typing.Self | None:
        for orientation in self.orientations:
            if orientation[side] == target:
                return orientation

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        raw_id, *raw_data = raw.split("\n")
        _id = re.findall(r"Tile (\d+):", raw_id)[0]
        data = tuple(tuple(row) for row in raw_data)
        return cls(int(_id), data)


def sliding_window(iterable: typing.Iterable, n: int):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def find_matching_tile(tiles: frozenset[Tile], side: str, target: str) -> Tile:
    return next(
        tile.find_orientation(side, target)
        for tile in tiles
        if target in tile.find_all_tops()
    )


def find_monster_count(image: Tile) -> int:
    return sum(
        all(window[y][x] == "#" for x, y in MONSTER_POS)
        for rows in sliding_window(image.data, MH)
        for window in zip(*(sliding_window(row, MW) for row in rows))
    )


def assemble_image(tiles: frozenset[Tile], edges: dict[str, int]) -> Tile:
    corner = next(iter_corners(tiles, edges))

    image_size = int(math.sqrt(len(tiles)))
    raw_image = [[None for _ in range(image_size)] for _ in range(image_size)]

    for y, x in itertools.product(range(image_size), repeat=2):
        done_tile_ids = {
            tile.id
            for tile in itertools.chain.from_iterable(raw_image)
            if tile is not None
        }
        available_tiles = frozenset(
            tile for tile in tiles if tile.id not in done_tile_ids
        )

        if y == x == 0:
            ntile = next(
                tile
                for tile in available_tiles
                if (tile.id not in done_tile_ids) and (tile.id == corner.id)
            )
            ntile = ntile.align_to_edges(edges, ("top", "left"))
        elif x == 0:
            ntile = find_matching_tile(
                available_tiles, "top", raw_image[y - 1][x].bottom_side
            )

        else:
            ntile = find_matching_tile(
                available_tiles, "left", raw_image[y][x - 1].right_side
            )

        raw_image[y][x] = ntile

    image_data = tuple(
        tuple(itertools.chain.from_iterable(zipped_row))
        for row in raw_image
        for zipped_row in zip(*(tile.borderless.data for tile in row))
    )

    return Tile(-1, image_data)


def iter_corners(
    tiles: frozenset[Tile], edges: dict[str, int]
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
    edges = dict(
        collections.Counter(
            top_side for tile in tiles for top_side in tile.find_all_tops()
        )
    )

    if not is_p2:
        return math.prod(corner.id for corner in iter_corners(tiles, edges))

    image = assemble_image(tiles, edges)
    water = "".join(itertools.chain.from_iterable(image.data)).count("#")

    monster_count = next(
        count
        for orientation in image.orientations
        if (count := find_monster_count(orientation)) != 0
    )

    monster_len = len(MONSTER_POS)
    return water - (monster_count * monster_len)


def iter_puzzle(puzzle_file) -> typing.Iterator[Tile]:
    inp = puzzle_file.read_text().strip()
    yield from map(Tile.from_str, inp.split("\n" * 2))


def p1(puzzle_file):
    return solve(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return solve(iter_puzzle(puzzle_file), is_p2=True)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
