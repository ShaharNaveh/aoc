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
    yield into(res)

p1_solution = sum(solve_p1(words))
print(p1_solution)
  
