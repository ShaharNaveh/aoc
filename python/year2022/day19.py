import dataclasses
import heapq
import itertools
import math
import operator
import re
import unittest

from utils import Day, main


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Resources:
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0

    def increment(self, name: str, amount: int = 1):
        return dataclasses.replace(self, **{name: self[name] + amount})

    def _combine(self, other, f: callable):
        return Resources(*itertools.starmap(f, zip(self, other)))

    def __add__(self, other):
        return self._combine(other, operator.add)

    def __sub__(self, other):
        return self._combine(other, operator.sub)

    def __getitem__(self, item: str) -> int:
        return getattr(self, item)

    def __iter__(self):
        return iter(dataclasses.astuple(self))


@dataclasses.dataclass(frozen=True, slots=True)
class Blueprint:
    _id: int
    prices: dict[str, Resources]

    @classmethod
    def from_str(cls, raw: str):
        _id, *resources = map(int, re.findall(r"\d+", raw))

        prices = {
            "ore": Resources(ore=resources[0]),
            "clay": Resources(ore=resources[1]),
            "obsidian": Resources(ore=resources[2], clay=resources[3]),
            "geode": Resources(ore=resources[4], obsidian=resources[5]),
        }

        return cls(_id, prices)


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class Branch:
    total: Resources = Resources()
    current: Resources = dataclasses.field(compare=False, default=Resources())
    robots: Resources = dataclasses.field(compare=False, default=Resources(ore=1))


def mine(blueprint: Blueprint, minutes: int = 24, *, max_queue_size: int = 1000) -> int:
    queue = [Branch()]

    for minute in range(minutes):
        next_queue = []

        if len(queue) > max_queue_size:
            queue = heapq.nlargest(max_queue_size, queue)

        for branch in queue:
            current = branch.current
            total = branch.total
            robots = branch.robots

            mined_branch = Branch(
                current=current + robots, total=total + robots, robots=robots
            )

            heapq.heappush(next_queue, mined_branch)

            if minute == minutes - 1:
                continue

            for resource, price in blueprint.prices.items():
                if any(b > a for a, b in zip(current, price)):
                    continue
                buy_branch = Branch(
                    current=mined_branch.current - price,
                    total=mined_branch.total,
                    robots=robots.increment(resource),
                )
                heapq.heappush(next_queue, buy_branch)

        queue = next_queue

    return heapq.nlargest(1, queue)[0].current.geode


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(Blueprint.from_str, inp.splitlines())


class Day19(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(mine(blueprint) * blueprint._id for blueprint in parsed)

    def part2(self, parsed):
        return math.prod(
            mine(blueprint, 32, max_queue_size=20_000)
            for blueprint in itertools.islice(parsed, 3)
        )


TEST_PUZZLE = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


class Tests(unittest.TestCase):
    DAY = Day19()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 33)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 3472)


if __name__ == "__main__":
    main(Day19)
