#!/usr/bin/env python
import pathlib

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

lst1 = map(int, lst1)
lst2 = map(int, lst2)

for a in sorted(lst1):
  print(a)
  print(type(a))
  break
