import itertools

from utils import Day, run


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, list(inp))


class Day08(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        image = tuple(itertools.batched(parsed, 25 * 6))
        layer = min(image, key=lambda layer: layer.count(0))
        return layer.count(1) * layer.count(2)

    def part2(self, parsed):
        raw_image = [
            next(str(digit) for digit in layer if digit != 2)
            for layer in zip(*itertools.batched(parsed, 25 * 6))
        ]

        trans = str.maketrans({"0": " ", "1": "#"})

        return "\n".join(
            " ".join(row).translate(trans) for row in itertools.batched(raw_image, 25)
        )


if __name__ == "__main__":
    run(Day08)
