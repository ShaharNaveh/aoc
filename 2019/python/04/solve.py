import itertools
import pathlib


def is_valid_password(num: int, *, is_p2: bool = False) -> bool:
    s = str(num)

    if len(s) != 6:
        return False

    for _, group in itertools.groupby(s):
        size = len(list(group))
        if (is_p2 and (size == 2)) or ((not is_p2) and (size >= 2)):
            break
    else:
        return False

    if s != "".join(sorted(s)):
        return False

    return True


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    start, stop = map(int, inp.split("-"))
    return range(start, stop + 1)


def p1(puzzle_file):
    return sum(map(is_valid_password, parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    return sum(is_valid_password(num, is_p2=True) for num in parse_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
