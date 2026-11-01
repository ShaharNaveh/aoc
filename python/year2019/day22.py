import enum
import re
import unittest

from utils import Day, main


@enum.unique
class Technique(enum.Enum):
    DealIntoNewStack = enum.auto()
    Cut = enum.auto()
    DealWithIncrement = enum.auto()

    @classmethod
    def from_str(cls, raw: str) -> "Technique":
        if "new" in raw:
            technique = Technique.DealIntoNewStack
        elif raw.startswith("cut"):
            technique = Technique.Cut
        else:
            technique = Technique.DealWithIncrement

        return technique


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        technique = Technique.from_str(line)
        amount = int(next(iter(re.findall(r"-?\d+", line)), 0))
        yield technique, amount


def find_position(instructions, cards: int = 10_007, card: int = 2019) -> int:
    """Position of `card` after a single shuffle."""
    pos = card
    for technique, amount in instructions:
        match technique:
            case Technique.DealIntoNewStack:
                pos = -pos - 1
            case Technique.Cut:
                pos -= amount
            case Technique.DealWithIncrement:
                pos *= amount
        pos %= cards
    return pos


def solve(instructions, cards: int = 10_007, repeats: int = 1, idx: int = 2019):
    mul, diff = 1, 0
    for technique, amount in instructions:
        match technique:
            case Technique.DealIntoNewStack:
                mul = -mul % cards
                diff = (diff + mul) % cards
            case Technique.Cut:
                diff = (diff + amount * mul) % cards
            case Technique.DealWithIncrement:
                mul = (mul * pow(amount, cards - 2, cards)) % cards

    increment = pow(mul, repeats, cards)
    offset = (diff * (1 - increment) * pow((1 - mul) % cards, cards - 2, cards)) % cards

    return (offset + idx * increment) % cards


class Day22(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return find_position(parsed)

    def part2(self, parsed):
        return solve(parsed, 119_315_717_514_047, 101_741_582_076_661, 2020)


EXAMPLE_1 = """\
deal with increment 7
deal into new stack
deal into new stack"""

EXAMPLE_2 = """\
cut 6
deal with increment 7
deal into new stack"""

EXAMPLE_3 = """\
deal with increment 7
deal with increment 9
cut -2"""

EXAMPLE_4 = """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""


class Tests(unittest.TestCase):
    DAY = Day22()

    def test_find_position(self):
        # The puzzle gives each example's result as the final order of a 10 card deck.
        for example, deck in [
            (EXAMPLE_1, "0 3 6 9 2 5 8 1 4 7"),
            (EXAMPLE_2, "3 0 7 4 1 8 5 2 9 6"),
            (EXAMPLE_3, "6 3 0 7 4 1 8 5 2 9"),
            (EXAMPLE_4, "9 2 5 8 1 4 7 0 3 6"),
        ]:
            parsed = self.DAY.parse(example)
            deck = list(map(int, deck.split()))
            with self.subTest(example=example):
                for card in range(10):
                    self.assertEqual(deck[find_position(parsed, 10, card)], card)


if __name__ == "__main__":
    main(Day22)
