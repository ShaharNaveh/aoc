import pathlib
import re
import string

PATTERN = re.compile(
    "|".join(
        f"{char}{char.upper()}|{char.upper()}{char}" for char in string.ascii_lowercase
    )
)


def react(polymer: str) -> int:
    while PATTERN.search(polymer):
        polymer = PATTERN.sub("", polymer)
    return len(polymer)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return inp


def p1(puzzle_file):
    return react(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    polymer = parse_puzzle(puzzle_file)
    return min(
        react(polymer.replace(char, "").replace(char.upper(), ""))
        for char in string.ascii_lowercase
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
