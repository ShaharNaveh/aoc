import collections

from utils import Day, main


def generate(num: int, count: int = 2000):
    for _ in range(count):
        num = (num ^ num << 6) & 0xFFFFFF
        num = (num ^ num >> 5) & 0xFFFFFF
        num = (num ^ num << 11) & 0xFFFFFF
        yield num


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day22(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(collections.deque(generate(num), maxlen=1)[0] for num in parsed)

    def part2(self, parsed):
        prices = collections.defaultdict(int)

        for initial_snum in parsed:
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


if __name__ == "__main__":
    main(Day22)
