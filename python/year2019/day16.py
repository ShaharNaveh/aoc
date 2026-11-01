import itertools
import unittest

from utils import Day, main


def iter_pattern(r: int):
    yield from itertools.chain.from_iterable(
        itertools.repeat(n, r) for n in (0, 1, 0, -1)
    )


def fft(signal: tuple[int, ...]) -> tuple[int, ...]:
    max_r = len(signal) + 1
    while True:
        signal = tuple(
            abs(
                sum(
                    digit * num
                    for digit, num in zip(
                        signal,
                        itertools.islice(itertools.cycle(iter_pattern(r)), 1, None),
                    )
                )
            )
            % 10
            for r in range(1, max_r)
        )
        yield signal


def parse_puzzle(puzzle, *, is_p2: bool = False):
    inp = puzzle.strip()
    if is_p2:
        return tuple(map(int, reversed((inp * 10_000)[int(inp[:7]) :])))
    return tuple(map(int, inp))


class Day16(Day):
    def parse(self, inp: str) -> str:
        return inp

    def part1(self, puzzle):
        return "".join(
            map(
                str,
                next(
                    signal
                    for phase, signal in enumerate(fft(parse_puzzle(puzzle)), 1)
                    if phase == 100
                )[:8],
            )
        )

    def part2(self, puzzle):
        signal = parse_puzzle(puzzle, is_p2=True)
        for _ in range(100):
            signal = tuple(itertools.accumulate(signal, lambda a, b: (a + b) % 10))
        return "".join(map(str, itertools.islice(reversed(signal), 0, 8)))


TEST_PUZZLE = "80871224585914546619083218645595"


class Tests(unittest.TestCase):
    DAY = Day16()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), "24176176")


if __name__ == "__main__":
    main(Day16)
