#!/usr/bin/env python
import hashlib
import itertools
import pathlib


def find(skey: str, prefix: str):
    for index in itertools.count():
        s = hashlib.md5(f"{skey}{index}".encode()).hexdigest()
        if s.startswith(prefix):
            yield index


def parse_puzzle(puzzle_file):
    return puzzle_file.read_text().strip()


def p1(puzzle_file):
    return next(find(parse_puzzle(puzzle_file), "0" * 5))


def p2(puzzle_file):
    return next(find(parse_puzzle(puzzle_file), "0" * 6))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
