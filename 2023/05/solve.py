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
      mapping = {"src": src, "dest": dest, "range": parse_almanac_line(line, src=src, dest=dest)}
      result["mappings"].append(mapping)
  return result

def find_in_almanac(src: str, val: int, dest: str, *, mappings: dict):
  records = filter(lambda r: (src == r["src"]) and (dest == r["dest"]), mappings)
  for record in records:
    range_len = record["range_len"]
    src_range = record["src_range"]
    dest_range = record["dest_range"]
    if (val >= src_range) and (val < dest_range + range_len):
      return val + range_len

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
print(almanac)
