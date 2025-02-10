import functools
import itertools
import json
import math
import pathlib


def add_left(sf: list | int, n: int | None):
    if n is None:
        return sf

    if isinstance(sf, int):
        return sf + n

    return [add_left(sf[0], n), sf[1]]


def add_right(sf: list | int, n: int | None):
    if n is None:
        return sf

    if isinstance(sf, int):
        return sf + n

    return [sf[0], add_right(sf[1], n)]


def split(sf: list | int):
    if isinstance(sf, int):
        if sf >= 10:
            return True, [sf // 2, math.ceil(sf / 2)]
        return False, sf

    a, b = sf

    change, a = split(a)
    if change:
        return True, [a, b]

    change, b = split(b)
    return change, [a, b]


def explode(sf: list | int, depth: int = 4):
    if isinstance(sf, int):
        return False, None, sf, None

    if depth == 0:
        return True, sf[0], 0, sf[1]

    a, b = sf

    exp, left, a, right = explode(a, depth - 1)
    if exp:
        return True, left, [a, add_left(b, right)], None

    exp, left, b, right = explode(b, depth - 1)
    if exp:
        return True, None, [add_right(a, left), b], right
    return False, None, sf, None


def add(left: list | int, right: list | int) -> list:
    sf = [left, right]
    while True:
        change, _, sf, _ = explode(sf)
        if change:
            continue
        change, sf = split(sf)
        if not change:
            break
    return sf


def magnitude(sf: list | int) -> int:
    if isinstance(sf, int):
        return sf

    return (magnitude(sf[0]) * 3) + (magnitude(sf[1]) * 2)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(json.loads, inp.splitlines())


def p1(puzzle_file):
    return magnitude(functools.reduce(add, iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return max(
        map(
            magnitude,
            itertools.starmap(add, itertools.permutations(iter_puzzle(puzzle_file), 2)),
        )
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
