import dataclasses
import functools
import itertools
import math
import operator
import pathlib
import re

@dataclasses.dataclass(frozen=True, slots=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def _combine(self, other, f: callable):
        return Resources(*(f(*pair) for pair in zip(self, other)))

    def __add__(self, other):
        return self._combine(other, operator.add)

    def __sub__(self, other):
        return self._combine(other, operator.sub)

    def __mul__(self, other):
        return Resources(*(val * other for val in self))

    def __getitem__(self, item: str) -> int:
        return getattr(self, item)

    def __iter__(self):
        return iter(dataclasses.astuple(self))

@dataclasses.dataclass(frozen=True)
class Blueprint:
    _id: int
    prices: dict[str, Resources] = dataclasses.field(hash=False)

    @functools.cache
    def mine(
        self,
        minutes: int = 24,
        *,
        resources: Resources = Resources(), 
        robots: Resources = Resources(ore=1),
    ) -> int:
        if minutes == 0:
            return resources.geode
        max_geode = resources.geode + robots.geode * minutes

        for name, price in self.prices.items():
            if (name != "geode") and (robots[name] >= self.max_price(name)):
                continue

            wait = 0
            for rname, amount in dataclasses.asdict(price).items():
                if amount == 0:
                    continue
                if robots[rname] == 0:
                    break
                wait = max(wait, -(-(amount - resources[rname]) // robots[rname]))
            else:
                rminutes = minutes - wait - 1
                if rminutes <= 0:
                    continue

                nresources = (resources + robots * (wait + 1)) - price
                nresources = dataclasses.replace(
                    nresources,
                    **{
                        name: min(val, self.max_price(name) * rminutes)
                        for name, val in dataclasses.asdict(nresources).items()
                        if name != "geode"
                    }
                )

                nrobots = dataclasses.replace(robots, **{name: robots[name] + 1})

                max_geode = max(
                    max_geode, self.mine(rminutes, resources=nresources, robots=nrobots)
                )
        return max_geode

    @functools.cache
    def max_price(self, name: str) -> int:
        return max(price[name] for price in self.prices.values())

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

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Blueprint.from_str, inp.splitlines())

def p1(puzzle_file):
    return sum(
        blueprint.mine() * blueprint._id
        for blueprint in iter_puzzle(puzzle_file)
    )

def p2(puzzle_file):
    return math.prod(
        map(
            operator.methodcaller("mine", 32),
            itertools.islice(iter_puzzle(puzzle_file), 3),
        )
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file)) 
print(p2(puzzle_file))
