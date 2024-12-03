import itertools
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

def parse_raw(raw: str, *, p2: bool = False):
  pattern = re.compile(r"(?P<section>[a-z-]+ map):\n(?P<data>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)
  
  seed_line, _, raw_almanac = raw.strip().partition("\n")
  seeds_data = seed_line.split(":")[1].strip().split(" ")
  seeds = map(int, seeds_data)
  
  if p2:
    seeds = set(itertools.batched(seeds))
  
  result = {"seeds": set(seeds), "mappings": []}

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
  if (val >= src_range) and (val < src_range + range_len):
    #print(f"{val=} in {record=}")
    return True
  return False

def calc_val_in_record(val: int, record: Record, reverse=False):
  src_range = record["src_range"]
  dest_range = record["dest_range"]
  range_len = record["range_len"]
  if reverse:
    return val - 
  return val - src_range + dest_range
  
def find_in_almanac(src: str, val: int, dest: str, *, mappings: list[Record], reverse: bool = False):
  records = [record for record in mappings if src == record["src"]] 
  dest_records = [record for record in records if dest == record["dest"]]
  #print(f"{src=} {dest=} {val=}")
  if dest_records:
    for dest_record in dest_records:
      if is_val_in_record(val=val, record=dest_record):
        return calc_val_in_record(val, dest_record, reverse=reverse)
    return val

  for record in records:
    if is_val_in_record(val=val, record=record):
      next_val = calc_val_in_record(val, record, reverse=reverse)
      break
  else:
    next_val = val

  if reverse:
    next_src = next(iter({record["src"] for record in mappings if src == record["dest"]}))
  else:
    next_src = records[0]["dest"]
    
  return find_in_almanac(src=next_src, dest=dest, val=next_val, mappings=mappings, reverse=reverse)

def seed_of_loc(src="location", dest="seed", val, *, mappings):
  records = [{record for record in mappings if True]
  

  
def p2(seeds: set[tuple[int, int]], mappings: list[Record]):
  nm = [{**record, **{"src": record["dest"], "dest": record["src"]}} for record in mappings]
  find_in_almanac(src="location", dest="seed"
  
  
#input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"
raw = input_file.read_text()
 
almanac = parse_raw(raw)  
seeds, mappings = almanac["seeds"], almanac["mappings"]
#print(min((find_in_almanac(src="seed", val=seed, dest="location", mappings=mappings) for seed in seeds)))

almanac = parse_raw(raw, p2=True)
seeds, mappings = almanac["seeds"], almanac["mappings"]
res = 
