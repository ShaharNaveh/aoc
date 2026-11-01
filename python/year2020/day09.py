import collections
import itertools

from utils import Day, aoc_main


def sliding_window(iterable, n: int = 26):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def is_valid(preamble: tuple[int, ...], num: int) -> bool:
    max_num = sum(sorted(preamble, reverse=True)[:2])
    if max_num < num:
        return False
    elif max_num == num:
        return True

    return any(sum(pair) == num for pair in itertools.combinations(preamble, 2))


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day09(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return next(
            num
            for *preamble, num in sliding_window(parsed)
            if not is_valid(preamble, num)
        )

    def part2(self, parsed):
        target_num = self.part1(parsed)
        nums = tuple(parsed)
        for size in range(2, len(nums) + 1):
            for window in sliding_window(nums, size):
                if sum(window) == target_num:
                    return min(window) + max(window)


if __name__ == "__main__":
    aoc_main(Day09)
