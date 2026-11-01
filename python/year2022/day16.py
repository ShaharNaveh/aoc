import collections
import dataclasses
import functools
import itertools
import operator
import re
import unittest

from utils import Day, main

global dists  # Instead of writing a custom cache decorator


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Valve:
    name: str
    rate: int
    connected: frozenset[str] = dataclasses.field(default_factory=frozenset)

    @classmethod
    def from_str(
        cls, raw: str, pattern=re.compile(r"Valve (\w+) .*=(\d*); .* valves? (.*)")
    ):
        name, raw_rate, raw_connected = pattern.findall(raw)[0]
        rate = int(raw_rate)
        connected = frozenset(raw_connected.split(", "))
        return cls(name, rate, connected)


def build_dists(valves: frozenset[Valve]) -> dict[tuple[str, str], int]:
    dists = collections.defaultdict(lambda: float("inf")) | {
        (valve.name, connected): 1 for valve in valves for connected in valve.connected
    }

    names = frozenset(map(operator.attrgetter("name"), valves))
    for a, b, c in itertools.product(*(names,) * 3):
        dists[(b, c)] = min(dists[(b, c)], dists[(b, a)] + dists[(a, c)])

    return dict(dists)


@functools.cache
def search(
    *,
    valve_name: str = "AA",
    targets: frozenset[Valve],
    minutes: int = 30,
    is_p2: bool = False,
):
    global dists
    return max(
        [
            nvalve.rate * (minutes - dists[(valve_name, nvalve.name)] - 1)
            + search(
                valve_name=nvalve.name,
                targets=targets - {nvalve},
                minutes=minutes - dists[(valve_name, nvalve.name)] - 1,
                is_p2=is_p2,
            )
            for nvalve in targets
            if minutes > dists[(valve_name, nvalve.name)]
        ]
        + [search(minutes=26, targets=targets, is_p2=False) if is_p2 else 0]
    )


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(Valve.from_str, inp.splitlines())


class Day16(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        global dists

        valves = frozenset(parsed)
        targets = frozenset(valve for valve in valves if valve.rate > 0)
        dists = build_dists(valves)
        return search(targets=targets)

    def part2(self, parsed):
        global dists

        valves = frozenset(parsed)
        targets = frozenset(valve for valve in valves if valve.rate > 0)
        dists = build_dists(valves)
        return search(minutes=26, targets=targets, is_p2=True)


TEST_PUZZLE = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


class Tests(unittest.TestCase):
    DAY = Day16()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 1651)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 1707)


if __name__ == "__main__":
    main(Day16)
