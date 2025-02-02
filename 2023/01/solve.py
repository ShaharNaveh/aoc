#!/usr/bin/env/python
import pathlib
import re

DATA_FILE = pathlib.Path(__file__).parent / "data.txt"
with DATA_FILE.open() as fd:
    lines = fd.readlines()

words = list(map(str.strip, lines))


def solve_p1(lst):
    r = re.compile(r"\d")
    for word in lst:
        found = re.findall(r, word)
        res = found[0] + found[-1]
        yield int(res)


def solve_p2(lst):
    dct = {
        #    "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    joined = "|".join(dct)
    expr = rf"(?=(\d|{joined}))"
    r = re.compile(expr)

    for word in lst:
        found = re.findall(r, word)
        if len(found) > 1:
            first, *_, last = found
        else:
            first = last = found[0]
        res = dct.get(first, first) + dct.get(last, last)
        yield int(res)


p1_solution = sum(solve_p1(words))
print(p1_solution)

p2_solution = sum(solve_p2(words))
print(p2_solution)
