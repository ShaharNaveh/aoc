import itertools
import pathlib


def dig(steps):
    xy = list(itertools.accumulate(steps))
    return (
        int(
            sum(
                a.real * b.imag
                - a.imag * b.real
                + abs(b.real - a.real + b.imag - a.imag)
                for a, b in itertools.pairwise(xy + xy[:1])
            )
        )
        // 2
        + 1
    )


def iter_puzzle(puzzle_file, *, is_p2: bool = False):
    inp = puzzle_file.read_text().strip()
    if is_p2:
        directions = {3: -1j, 1: 1j, 2: -1, 0: 1}
    else:
        directions = {"U": -1j, "D": 1j, "L": -1, "R": 1}

    for step in inp.splitlines():
        direction, distance, color = step.split()
        distance = int(distance)
        if is_p2:
            color = color.removeprefix("(#").removesuffix(")")
            distance = int(color[:-1], 16)
            yield directions[int(color[-1])] * distance
        else:
            yield directions[direction] * distance


def p1(puzzle_file):
    steps = iter_puzzle(puzzle_file)
    return dig(steps)


def p2(puzzle_file):
    steps = iter_puzzle(puzzle_file, is_p2=True)
    return dig(steps)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
