import itertools
import pathlib


def iter_puzzle(puzzle_file):
    yield 1

    inp = puzzle_file.read_text().strip()
    func = lambda x: int(x) if x[-1].isdigit() else 0
    yield from map(func, inp.split())


def simulate(ops):
    yield from enumerate(itertools.accumulate(ops), start=1)


def p1(puzzle_file):
    return sum(
        cycle * x for cycle, x in simulate(iter_puzzle(puzzle_file)) if cycle % 40 == 20
    )


def p2(puzzle_file):
    return "\n".join(
        "".join(
            "#" if (cycle - 1) % 40 - x in (-1, 0, 1) else " " for cycle, x in batch
        )
        for batch in itertools.batched(simulate(iter_puzzle(puzzle_file)), 40)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
