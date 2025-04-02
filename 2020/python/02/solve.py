import pathlib


def is_valid(line: str, *, is_p2: bool = False) -> bool:
    raw_range, letter, password = line.replace(":", "").split()
    l, m = map(int, raw_range.split("-"))

    if is_p2:
        a, b = password[l - 1], password[m - 1]
        return (a != b) and (letter in (a, b))

    return password.count(letter) in range(l, m + 1)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.splitlines()


def p1(puzzle_file):
    return sum(map(is_valid, iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return sum(map(lambda l: is_valid(l, is_p2=True), iter_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
