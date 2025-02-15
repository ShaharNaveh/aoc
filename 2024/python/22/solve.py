import collections
import pathlib


def generate(num: int, count: int = 2000):
    for _ in range(count):
        num = (num ^ num << 6) & 0xFFFFFF
        num = (num ^ num >> 5) & 0xFFFFFF
        num = (num ^ num << 11) & 0xFFFFFF
        yield num


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return sum(
        collections.deque(generate(num), maxlen=1)[0]
        for num in iter_puzzle(puzzle_file)
    )


def p2(puzzle_file):
    prices = collections.defaultdict(int)

    for initial_snum in iter_puzzle(puzzle_file):
        seen = set()
        diffs = collections.deque(maxlen=4)

        prev = initial_snum % 10
        for price in (num % 10 for num in generate(initial_snum)):
            diffs.append(price - prev)
            prev = price
            if len(diffs) != diffs.maxlen:
                continue
            if (seq := tuple(diffs)) in seen:
                continue
            seen.add(seq)
            prices[seq] += price

    return max(prices.values())


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
