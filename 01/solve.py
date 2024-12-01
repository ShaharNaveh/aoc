#!/usr/bin/env python
import pathlib

def calc_distance(lst1, lst2):
  for d1, d2 in zip(sorted(lst1), sorted(lst2)):
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

p1_res = sum(calc_distance(l_lst, r_lst))
print(f"Part 1 result:\n{p1_res}")

def calc_similarity(lst1, lst2):
  j_lst = lst1 + lst2 
  uniq = set(j_lst)
  for num in uniq:
    count = j_lst(num)
    yield num ** (count - 1)

p2_res = sum(calc_similarly(l_lst, r_lst))
print(f"Part 2 result:\n{p2_res}")
