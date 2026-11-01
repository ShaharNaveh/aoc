import enum
import heapq
import typing
import unittest

from utils import Day, main

type Portals = dict[complex, tuple[str, "PortalType"]]


@enum.unique
class PortalType(enum.Enum):
    Inner = enum.auto()
    Outer = enum.auto()

    def __invert__(self) -> typing.Self:
        return PortalType.Inner if self == PortalType.Outer else PortalType.Outer


def find_neighbors(pos: complex) -> frozenset[complex]:
    return frozenset(pos + offset for offset in (1, -1, 1j, -1j))


class Branch(typing.NamedTuple):
    pos: complex
    level: int = 0
    cost: int = 0

    def __lt__(self, other) -> bool:
        return (self.cost, self.level) < (other.cost, other.level)


def find_portals(grid: dict[complex, str]) -> Portals:
    portals = {}

    min_x = min_y = 0
    max_x = int(max(pos.real for pos in grid))
    max_y = int(max(pos.imag for pos in grid))

    for pos, tile_b in grid.items():
        if not tile_b.isalpha():
            continue
        for offset in (1, 1j):
            pos_a, pos_c = pos + offset * -1, pos + offset
            tile_a, tile_c = map(grid.get, (pos_a, pos_c))
            if None in (tile_a, tile_c):
                continue
            tiles = (tile_a, tile_b, tile_c)
            if tiles.count(".") != 1:
                continue

            if any(
                (p.real in (min_x, max_x)) or (p.imag in (min_y, max_y))
                for p in (pos_a, pos_c)
            ):
                typ = PortalType.Outer
            else:
                typ = PortalType.Inner

            name = "".join(t for t in tiles if t.isalpha())
            portals[pos] = (name, typ)

    return portals


def extract_info(
    grid: dict[complex, str],
) -> tuple[Portals, frozenset[complex], complex, complex]:
    portals = find_portals(grid)

    start = next(pos for pos, (name, _) in portals.items() if name == "AA")

    start_pos = next(
        pos for pos in find_neighbors(start) if not grid.get(pos, "a").isalpha()
    )

    end = next(pos for pos, (name, _) in portals.items() if name == "ZZ")
    end_pos = next(
        pos for pos in find_neighbors(end) if not grid.get(pos, "a").isalpha()
    )

    portals.pop(start)
    portals.pop(end)

    walkable = frozenset(pos for pos, tile in grid.items() if tile == ".") | frozenset(
        portals
    )

    return portals, walkable, start_pos, end_pos


def walk(
    portals: Portals,
    walkable: frozenset[complex],
    start: complex,
    end: complex,
    *,
    is_p2: bool = False,
) -> int:
    seen = set()
    pq = [Branch(start)]
    while pq:
        pos, level, cost = heapq.heappop(pq)
        if (pos, level) in seen:
            continue
        seen.add((pos, level))

        if (pos, level) == (end, 0):
            return cost

        for npos in find_neighbors(pos) & walkable:
            if (tup := portals.get(npos)) is not None:
                name, typ = tup
                if is_p2:
                    if (level == 0) and (typ == PortalType.Outer):
                        continue
                    nlevel = level + 1 if typ == PortalType.Outer else level - 1
                else:
                    nlevel = level
                pair_pos = next(
                    p
                    for p, (pair_name, pair_typ) in portals.items()
                    if (name == pair_name) and (typ != pair_typ)
                )
                nbranch = Branch(pair_pos, nlevel, cost)
            else:
                nbranch = Branch(npos, level, cost + 1)
            heapq.heappush(pq, nbranch)


class Day20(Day):
    def parse(self, inp: str):
        inp = inp.rstrip()
        return {
            complex(x, y): tile
            for y, row in enumerate(inp.splitlines())
            for x, tile in enumerate(row)
            if tile not in "# "
        }

    def part1(self, parsed):
        return walk(*extract_info(parsed))

    def part2(self, parsed):
        return walk(*extract_info(parsed), is_p2=True)


TEST_PUZZLE = """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """


class Tests(unittest.TestCase):
    def test_part2_test_puzzle(self):
        d = Day20()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 396)


if __name__ == "__main__":
    main(Day20)
