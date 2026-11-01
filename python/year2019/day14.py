import collections
import re
import unittest

from utils import Day, main


def find_ore_required(reactions: dict, fuel: int = 1) -> int:
    need = collections.defaultdict(int, {"FUEL": fuel})
    have = collections.defaultdict(int)
    while True:
        chemical = next((chemical for chemical in need if chemical != "ORE"), None)
        if chemical is None:
            break

        quantity, inputs = reactions[chemical]
        quotient, remainder = divmod(need.pop(chemical), quantity)
        if remainder != 0:
            have[chemical] = quantity - remainder
            quotient += 1

        for iquantity, ichemical in inputs:
            need[ichemical] = need[ichemical] + quotient * iquantity - have[ichemical]
            have.pop(ichemical)

    return need["ORE"]


class Day14(Day):
    def parse(self, inp: str):
        inp = inp.strip()

        reactions = {}
        for *raw_inputs, raw_output in map(
            lambda x: re.findall(r"\d+\s\w+", x), inp.splitlines()
        ):
            inputs = set()
            for raw_input in raw_inputs:
                quantity, chemical = raw_input.split()
                inputs.add((int(quantity), chemical))
            quantity, chemical = raw_output.split()
            reactions[chemical] = (int(quantity), frozenset(inputs))
        return reactions

    def part1(self, parsed):
        return find_ore_required(parsed)

    def part2(self, parsed):
        ORES = 1_000_000_000_000
        reactions = parsed
        fuel, search = 1, 2

        while find_ore_required(reactions, search) < ORES:
            fuel, search = search, search * 2

        while search - fuel >= 2:
            half = fuel + (search - fuel) // 2
            if find_ore_required(reactions, half) > ORES:
                search = half
            else:
                fuel = half
        return fuel


TEST_PUZZLE = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day14()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 31)


if __name__ == "__main__":
    main(Day14)
