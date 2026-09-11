#!/usr/bin/env python
import functools
import hashlib
import itertools
import pathlib
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

PATTERN = re.compile(r"(.)\1\1")


@functools.cache
def build_hash(salt: str, index: int, *, iterations: int = 1) -> str:
    res = f"{salt}{index}"

    for _ in range(iterations):
        res = hashlib.md5(res.encode()).hexdigest()

    return res


def iter_hashes(salt: str, it: Iterable[int], f=build_hash):
    yield from (f(salt, index) for index in it)


def get_triple(s: str) -> str | None:
    m = PATTERN.search(s)
    return m.group(1) if m else None


def iter_keys(salt: str, f=build_hash):
    for index in itertools.count():
        key = f(salt, index)
        c = get_triple(key)
        if c is None:
            continue

        target = c * 5
        nindex = index + 1
        range_ = range(nindex, nindex + 1000)
        if not any(target in nkey for nkey in iter_hashes(salt, range_, f)):
            continue

        yield index


def parse_puzzle(puzzle_file):
    return puzzle_file.read_text().strip()


def p1(puzzle_file):
    salt = parse_puzzle(puzzle_file)
    return next(itertools.islice(iter_keys(salt), 64 - 1, None))


def p2(puzzle_file):
    salt = parse_puzzle(puzzle_file)
    f = functools.partial(build_hash, iterations=2016 + 1)
    return next(itertools.islice(iter_keys(salt, f), 64 - 1, None))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
