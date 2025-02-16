import collections
import itertools
import pathlib


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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return next(
        num
        for *preamble, num in sliding_window(iter_puzzle(puzzle_file))
        if not is_valid(preamble, num)
    )


def p2(puzzle_file):
    target_num = p1(puzzle_file)
    nums = tuple(iter_puzzle(puzzle_file))
    for size in range(2, len(nums) + 1):
        for window in sliding_window(nums, size):
            if sum(window) == target_num:
                return min(window) + max(window)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
