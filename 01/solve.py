#!/usr/bin/env python
import pathlib

DATA_FILE = pathlib.Path(__file__).parent / "data.txt"

with DATA_FILE.open() as fd:
  lines = fd.readlines()

lst1 = []
lst2 = []

for line in lines:
  line = line.strip()
  
  print(line)
  print(line.split(" " * 3))
  print(line.split("\t"))
  break
