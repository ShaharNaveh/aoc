import pathlib
import re

input_file = pathlib.Path(__file__).parent / "input.txt"
raw = input_file.read_text()

def parse_raw(raw):
  lines = raw.splitlines()
  seed_line = lines.pop(0)
  data = "\n".join(lines)
  pattern = re.compile(r"(?P<section>[a-z-]+ map):\n(?P<data>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)

  for matched in pattern.finditer(data):
    section = matched.group("section")
    data = matched.group("data")
    source_name, dest_name = section.rstrip(" map").split("-to-")
    
  
parse_raw(raw)  


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
