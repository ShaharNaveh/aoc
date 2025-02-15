import collections
import dataclasses
import functools
import itertools
import operator
import pathlib
import re

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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Valve.from_str, inp.splitlines())


def p1(puzzle_file):
    global dists

    valves = frozenset(iter_puzzle(puzzle_file))
    targets = frozenset(valve for valve in valves if valve.rate > 0)
    dists = build_dists(valves)
    return search(targets=targets)


def p2(puzzle_file):
    global dists

    valves = frozenset(iter_puzzle(puzzle_file))
    targets = frozenset(valve for valve in valves if valve.rate > 0)
    dists = build_dists(valves)
    return search(minutes=26, targets=targets, is_p2=True)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
