import itertools
import unittest

from utils import Day, run


class Day13(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        raw_ts, raw_buses = inp.splitlines()
        buses = tuple(
            (idx, int(bus))
            for idx, bus in enumerate(raw_buses.split(","))
            if bus != "x"
        )
        return int(raw_ts), buses

    def part1(self, parsed):
        start_ts, buses = parsed
        return next(
            (ts - start_ts) * target_bus
            for ts in itertools.count(start_ts)
            if any(ts % (target_bus := bus) == 0 for _, bus in buses)
        )

    def part2(self, parsed):
        ts, buses = parsed
        step = 1
        for idx, bus in buses:
            ts = next(c for c in itertools.count(ts, step) if (c + idx) % bus == 0)
            step *= bus
        return ts


TEST_PUZZLE = """\
939
7,13,x,x,59,x,31,19"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day13()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 295)

    def test_part2_test_puzzle(self):
        d = Day13()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 1068781)


if __name__ == "__main__":
    run(Day13)
