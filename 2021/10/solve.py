import pathlib

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def autocomplete_score(todo: list[str]) -> int:
    score = 0
    for char in (PAIRS[c] for c in reversed(todo)):
        score *= 5
        score += ")]}>".index(char) + 1
    return score


def illegal_char(line: str) -> str | list[str]:
    buf = []
    for char in line:
        if char in PAIRS:
            buf.append(char)
        else:
            if char != PAIRS[buf.pop()]:
                return char

    return buf


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.splitlines()


def p1(puzzle_file):
    return sum(
        {")": 3, "]": 57, "}": 1197, ">": 25137}[char]
        for char in map(illegal_char, iter_puzzle(puzzle_file))
        if isinstance(char, str)
    )


def p2(puzzle_file):
    scores = tuple(
        autocomplete_score(buf)
        for buf in map(illegal_char, iter_puzzle(puzzle_file))
        if isinstance(buf, list)
    )
    return sorted(scores)[len(scores) // 2]


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
