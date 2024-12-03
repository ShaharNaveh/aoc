import pathlib
from typing import TypedDict
import re

class Record(TypedDict):
  src: str
  dest: str
  src_range: int
  dest_range: int
  range_len: int
  
def parse_almanac_line(line: str, *, src: str, dest: str) -> Record:
  data = line.split(" ")
  dest_range, src_range, range_len = map(int, data)
  res = Record(src_range=src_range, dest_range=dest_range, range_len=range_len, src=src, dest=dest)
  return res

def parse_raw(raw: str):
  pattern = re.compile(r"(?P<section>[a-z-]+ map):\n(?P<data>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)
  
  seed_line, _, raw_almanac = raw.strip().partition("\n")
  seeds_data = seed_line.split(":")[1].strip().split(" ")
  seeds = set(map(int, seeds_data))
  
  result = {"seeds": seeds, "mappings": []}

  for matched in pattern.finditer(raw_almanac):
    section = matched.group("section")
    data = matched.group("data")
    src, dest = section.rstrip(" map").split("-to-")
    for line in data.splitlines():
      mapping = parse_almanac_line(line, src=src, dest=dest)
      result["mappings"].append(mapping)
  return result

def is_val_in_record(*, val: int, record: Record) -> bool:
  range_len = record["range_len"]
  src_range = record["src_range"]
  dest_range = record["dest_range"]
  if (val >= src_range) and (val < dest_range + range_len):
    return True
  return False

def calc_val_in_record(val: int, record: Record):
  src_range = record["src_range"]
  dest_range = record["dest_range"]
  return val + (dest_range - src_range)
  
def find_in_almanac(src: str, val: int, dest: str, *, mappings: dict):
  records = list(filter(lambda r: src == r["src"], mappings))
  print(f"{records=}")
  dest_records = list(filter(lambda r: dest == r["dest"], records))
  if dest_records:
    for dest_record in dest_records:
      if is_val_in_record(val=val, record=dest_record):
        return calc_val_in_record(val, dest_record)
    return val

  for record in records:
    if is_val_in_record(val=val, record=record):
      next_val = calc_val_in_record(val, record)
      break
  else:
    next_val = val
  
  next_dest = records[0]["dest"]
  return find_in_almanac(src=dest, dest=next_dest, val=next_val, mappings=mappings)

input_file = pathlib.Path(__file__).parent / "input.txt"
raw = input_file.read_text()
 
#parse_raw(raw)  


test_inp = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

almanac = parse_raw(test_inp)
seeds, mappings = almanac["seeds"], almanac["mappings"]
print(f"{mappings=}")
res = find_in_almanac(src="seed", val=79, dest="location", mappings=mappings)
print(res)
res = find_in_almanac(src="seed", val=13, dest="location", mappings=mappings)
print(res)

