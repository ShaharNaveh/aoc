import itertools
import typing
import unittest

from utils import Day, main


class Cart(typing.NamedTuple):
    pos: complex
    offset: complex
    turns: int = 0

    def __and__(self, other) -> bool:
        return self.pos == other.pos

    def __lt__(self, other) -> bool:
        return (self.pos.imag, self.pos.real) < (other.pos.imag, other.pos.real)


def simulate(carts, grid, *, is_p2: bool = False):
    carts = carts.copy()
    while True:
        crashed = set()
        for idx, cart in sorted(carts.items(), key=lambda t: t[1]):
            if idx in crashed:
                continue
            pos, offset, turns = cart
            tile = grid[pos]
            match tile:
                case "/":
                    offset = -1j / offset
                case "\\":
                    offset = 1j / offset
                case "+":
                    offset *= {0: -1j, 1: 1, 2: 1j}[turns % 3]
                    turns += 1
            carts[idx] = Cart(pos + offset, offset, turns)
            for (idx1, cart1), (idx2, cart2) in itertools.combinations(
                carts.items(), r=2
            ):
                if cart1 & cart2:
                    crashed |= {idx1, idx2}

        if crashed:
            if not is_p2:
                idx = crashed.pop()
                return carts[idx].pos
            for idx in crashed:
                carts.pop(idx)

        if len(carts) == 1:
            return next(iter(carts.values())).pos


def pos_to_str(pos: complex) -> str:
    return ",".join(map(str, map(int, (pos.real, pos.imag))))


class Day13(Day):
    def parse(self, inp: str):
        inp = inp.rstrip()
        base_grid = {
            complex(x, y): tile
            for y, row in enumerate(inp.splitlines())
            for x, tile in enumerate(row)
            if tile
        }
        offsets = {"^": -1j, "<": -1, "v": 1j, ">": 1}
        carts = {
            idx: Cart(pos, offset)
            for idx, (pos, tile) in enumerate(base_grid.items())
            if (offset := offsets.get(tile)) is not None
        }
        grid = base_grid | {
            pos: "-" if offset in (1, -1) else "|" for pos, offset, _ in carts.values()
        }

        return carts, grid

    def part1(self, parsed):
        return pos_to_str(simulate(*parsed))

    def part2(self, parsed):
        return pos_to_str(simulate(*parsed, is_p2=True))


TEST_PUZZLE = """\
/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   """


class Tests(unittest.TestCase):
    DAY = Day13()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), "7,3")


if __name__ == "__main__":
    main(Day13)
