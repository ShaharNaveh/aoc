import collections
import itertools

from utils import Day, main


def sliding_window(iterable, n: int = 2):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day01(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(r > l for l, r in sliding_window(parsed))

    def part2(self, parsed):
        return sum(w[-1] > w[0] for w in sliding_window(parsed, 4))


if __name__ == "__main__":
    main(Day01)
