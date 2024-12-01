#!/usr/bin/env python

DATA_FILE = "data.txt"
with open(DATA_FILE) as fd:
  lines = fd.readlines()

for line in lines:
  print(line)
  print(line.split(" "))
  print(line.split("\t"))
  break
