import collections
import pathlib


def get_marker(signal: str, window_size: int = 4) -> int:
    for i in range(len(signal) - window_size + 1):
        window = signal[i : i + window_size]
        if all(window.count(char) == 1 for char in window):
            return i + window_size


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return inp


def p1(puzzle_file):
    signal = parse_puzzle(puzzle_file)
    return get_marker(signal)


def p2(puzzle_file):
    signal = parse_puzzle(puzzle_file)
    return get_marker(signal, 14)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
