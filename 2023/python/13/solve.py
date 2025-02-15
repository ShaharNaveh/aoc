import pathlib


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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for raw_note in inp.split("\n" * 2):
        yield raw_note.splitlines()


def p1(puzzle_file):
    return sum(summarize_note(note) for note in iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return sum(summarize_note(note, flips=1) for note in iter_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
