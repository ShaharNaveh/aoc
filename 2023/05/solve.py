import itertools
import pathlib
from typing import TypedDict
import re

input_file = pathlib.Path(__file__).parent / "test_input.txt"

def p1(path):
  puzzle = path.read_text().strip()
  seeds, *blocks = puzzle.split("\n" * 2)
  seeds = list(map(int, seeds.split(":")[1].split()))
  for block in blocks:
    ranges = []
    for line in block.splitlines()[1:]:
      info = list(map(int, line.split()))
      ranges.append(info)
      
    buf = []
    for seed in seeds:
      for dest, src, range_len in ranges:
        if src <= seed < src + range_len:
          val = seed - src + dest
          buf.append(val)
          break
      else:
        buf.append(seed)
    seeds = buf
  print(min(seeds))

def p2(path):
  puzzle = path.read_text().strip()
  inputs, *blocks = puzzle.split("\n" * 2)
  inputs = list(map(int, inputs.split(":")[1].split()))
  
  seeds = []
  for i in range(0, len(inputs), 2):
    seeds.append((inputs[i], inputs[i] + inputs[i + 1]))
    
  for block in blocks:
    ranges = []
    for line in block.splitlines()[1:]:
      info = list(map(int, line.split()))
      ranges.append(info)
      
    buf = []
    while seeds:
      start, end = seeds.pop()
      for dest, src, range_len in ranges:
        overlap_start = max(start, src)
        overlap_end = min(end, src + range_len)
        if overlap_start < overlap_end:
          buf.append((overlap_start - src + dest, overlap_end - src + dest))
          if overlap_start > start:
            seeds.append((start, overlap_start))
          if overlap_end > end:
            seeds.append((overlap_end, end))
          break
      else:
        buf.append((start, end))
        
    seeds = buf
  print(min(seeds)[0])

p1(input_file)
p2(input_file)
