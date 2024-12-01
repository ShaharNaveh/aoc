#!/usr/bin/env python
import pathlib

def get_distances(it1, it2):
  for d1, d2 in zip(sorted(it1), sorted(it2)):
      yield abs(d1 - d2)
    
DATA_FILE = pathlib.Path(__file__).parent / "data.txt"

with DATA_FILE.open() as fd:
  lines = fd.readlines()

l_lst = []
r_lst = []

for line in lines:
  line = line.strip()
  l_item, r_item = line.split(" " * 3)
  l_lst.append(l_item)
  r_lst.append(r_item)

l_lst = list(map(int, l_lst))
r_lst = list(map(int, r_lst))

p1_res = sum(get_distances(l_lst, r_lst))
print(f"Part 1 result:\n{p1_res}")
