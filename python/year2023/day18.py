import itertools

from utils import Day, main


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


def iter_puzzle(puzzle, *, is_p2: bool = False):
    inp = puzzle.strip()
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


class Day18(Day):
    def parse(self, inp: str) -> str:
        return inp

    def part1(self, puzzle):
        steps = iter_puzzle(puzzle)
        return dig(steps)

    def part2(self, puzzle):
        steps = iter_puzzle(puzzle, is_p2=True)
        return dig(steps)


if __name__ == "__main__":
    main(Day18)
