from utils import Day, main


def iter_puzzle(puzzle):
    inp = puzzle.strip()

    trans = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})
    yield from map(lambda raw: int(raw.translate(trans), 2), inp.splitlines())


class Day05(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return max(parsed)

    def part2(self, parsed):
        ids = sorted(parsed)
        for a, b in zip(ids, ids[1:]):
            if b - a != 1:
                return a + 1


if __name__ == "__main__":
    main(Day05)
