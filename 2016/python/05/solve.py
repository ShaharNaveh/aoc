#!/usr/bin/env python
import hashlib
import itertools
import pathlib


def find(door_id: str):
    for index in itertools.count():
        s = hashlib.md5(f"{door_id}{index}".encode()).hexdigest()
        if s.startswith("0" * 5):
            yield s[5], s[6]


def parse_puzzle(puzzle_file):
    return puzzle_file.read_text().strip()


def p1(puzzle_file):
    return "".join(
        itertools.islice(
            map(lambda tup: tup[0], find(parse_puzzle(puzzle_file))),
            8,
        )
    )


def p2(puzzle_file):
    buf = ["_"] * 8
    for pos, val in find(parse_puzzle(puzzle_file)):
        try:
            pos = int(pos)
        except ValueError:
            continue

        if pos > 7:
            continue

        if buf[pos] != "_":
            continue

        buf[pos] = val

        if "_" not in buf:
            break

    return "".join(buf)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
