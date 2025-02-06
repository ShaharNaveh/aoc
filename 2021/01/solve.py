import collections
import itertools
import pathlib


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
    return sum(r > l for l, r in sliding_window(iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return sum(w[-1] > w[0] for w in sliding_window(iter_puzzle(puzzle_file), 4))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
