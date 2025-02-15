import functools
import pathlib

NUMPAD = {
    "0": 1 + 3j,
    "1": 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    "4": 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "7": 0,
    "8": 1,
    "9": 2,
    "A": 2 + 3j,
}

DIRPAD = {
    "<": 1j,
    ">": 2 + 1j,
    "A": 2,
    "^": 1,
    "v": 1 + 1j,
}


def best_path(start, end, robots, pad):
    res = float("inf")
    todo = [(start, "")]
    while todo:
        pos, path = todo.pop()
        if pos == end:
            res = min(res, best_robot(path + "A", robots - 1))
        elif pos in pad.values():
            if end.real > pos.real:
                todo.append((pos + 1, path + ">"))
            if pos.real > end.real:
                todo.append((pos - 1, path + "<"))
            if end.imag > pos.imag:
                todo.append((pos + 1j, path + "v"))
            if pos.imag > end.imag:
                todo.append((pos - 1j, path + "^"))
    return res


@functools.cache
def best_robot(path, robots):
    if robots == 0:
        return len(path)
    start = DIRPAD["A"]
    return sum(
        best_path(start, (start := DIRPAD[char]), robots, DIRPAD) for char in path
    )


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for code in inp.splitlines():
        yield code, int(code.removesuffix("A"))


def p1(puzzle_file):
    start = NUMPAD["A"]
    return sum(
        sum(best_path(start, (start := NUMPAD[char]), 3, NUMPAD) for char in code)
        * numeric
        for code, numeric in parse_puzzle(puzzle_file)
    )


def p2(puzzle_file):
    start = NUMPAD["A"]
    return sum(
        sum(best_path(start, (start := NUMPAD[char]), 26, NUMPAD) for char in code)
        * numeric
        for code, numeric in parse_puzzle(puzzle_file)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
