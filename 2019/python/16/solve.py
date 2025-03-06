import itertools
import pathlib


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


def parse_puzzle(puzzle_file, *, is_p2: bool = False):
    inp = puzzle_file.read_text().strip()
    if is_p2:
        return tuple(map(int, reversed((inp * 10_000)[int(inp[:7]) :])))
    return tuple(map(int, inp))


def p1(puzzle_file):
    return "".join(
        map(
            str,
            next(
                signal
                for phase, signal in enumerate(fft(parse_puzzle(puzzle_file)), 1)
                if phase == 100
            )[:8],
        )
    )


def p2(puzzle_file):
    signal = parse_puzzle(puzzle_file, is_p2=True)
    for _ in range(100):
        signal = tuple(itertools.accumulate(signal, lambda a, b: (a + b) % 10))
    return "".join(map(str, itertools.islice(reversed(signal), 0, 8)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
