import collections
import functools
import itertools
import pathlib


@functools.cache
def possible_combinations(adapter: int, adapters: frozenset[int]) -> int:
    can_connect = frozenset(filter(lambda x: 3 >= x - adapter >= 1, adapters))
    if not can_connect:
        return 1
    return sum(possible_combinations(nadapter, adapters) for nadapter in can_connect)


def sliding_window(iterable, n: int = 2):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    diffs = collections.defaultdict(int)
    for a, b in sliding_window(itertools.chain([0], sorted(iter_puzzle(puzzle_file)))):
        diffs[b - a] += 1
    diffs[3] += 1
    return diffs[1] * diffs[3]


def p2(puzzle_file):
    adapters = frozenset(iter_puzzle(puzzle_file))
    return possible_combinations(0, adapters)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
