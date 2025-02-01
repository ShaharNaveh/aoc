import dataclasses
import heapq
import itertools
import math
import operator
import pathlib
import re

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

def mine(
    blueprint: Blueprint, minutes: int = 24, *, max_queue_size: int = 1000
) -> int:
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

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Blueprint.from_str, inp.splitlines())

def p1(puzzle_file):
    return sum(
        mine(blueprint) * blueprint._id for blueprint in iter_puzzle(puzzle_file)
    )

def p2(puzzle_file):
    return math.prod(
        mine(blueprint, 32, max_queue_size=20_000)
        for blueprint in itertools.islice(iter_puzzle(puzzle_file), 3)
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file)) 
print(p2(puzzle_file))
