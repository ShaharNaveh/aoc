import pathlib
import re

def parse_almanac_line(line: str):
  data = line.split(" ")
  lst = list(map(int, data))
  return range(lst[1], lst[0] + lst[2])

def parse_raw(raw: str):
  pattern = re.compile(r"(?P<section>[a-z-]+ map):\n(?P<data>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)
  seed_line, _, raw_almanac = raw.strip().partition("\n")
  print(seed_line)
  seeds_data = seed_line.split(":")[1].strip()
  seeds = set(map(int, seeds_data))
  result = {"seeds": seeds, "mappings": []}

  for matched in pattern.finditer(raw_almanac):
    section = matched.group("section")
    data = matched.group("data")
    src, dest = section.rstrip(" map").split("-to-")
    for line in data.splitlines():
      mapping = {"src": src, "dest": dest, "range": parse_almanac_line(line)}
      result["mappings"].append(mapping)
  return result



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
