#!/usr/bin/env python
import pathlib

def get_distances(it1, it2):
  for d1, d2 in zip(it1, it2):
      yield abs(d1 - d2)
    
DATA_FILE = pathlib.Path(__file__).parent / "data.txt"

with DATA_FILE.open() as fd:
  lines = fd.readlines()

lst1 = []
lst2 = []

for line in lines:
  line = line.strip()
  item1, item2 = line.split(" " * 3)
  lst1.append(item1)
  lst2.append(item2)

it1 = sorted(map(int, lst1))
it2 = sorted(map(int, lst2))

res = sum(get_distances(it1, it2))
print(res)
