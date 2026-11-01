from utils import Day, aoc_main


def find_distance(a: str, b: str) -> int:
    return sum(l != r for l, r in zip(a, b))


def find_reflection(note: list[str], flips: int = 0) -> int:
    for idx in range(1, len(note)):
        dist = sum(
            find_distance(a, b) for a, b in zip(reversed(note[:idx]), note[idx:])
        )
        if dist == flips:
            return idx
    return 0


def summarize_note(note: list[str], flips: int = 0) -> int:
    rows = find_reflection(note, flips)
    cols = find_reflection(list(zip(*note)), flips)
    return cols + (100 * rows)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for raw_note in inp.split("\n" * 2):
        yield raw_note.splitlines()


class Day13(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return sum(summarize_note(note) for note in parsed)

    def part2(self, parsed):
        return sum(summarize_note(note, flips=1) for note in parsed)


if __name__ == "__main__":
    aoc_main(Day13)
