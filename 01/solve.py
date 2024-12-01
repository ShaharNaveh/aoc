#!/usr/bin/env python
import pathlib



DATA_FILE = pathlib.Path(__file__).parent / "data.txt"

with DATA_FILE.open() as fd:
  lines = fd.readlines()

for line in lines:
  print(line)
  print(line.split(" "))
  print(line.split("\t"))
  break
