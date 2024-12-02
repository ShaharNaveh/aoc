import pathlib

input_file = pathlib.Path(__file__).parent / "input.txt"
raw = input_file.read_text()

def parse_raw(raw):
  lines = raw.splitlines()
  seed_line = lines.pop(0)
  for line in lines:
    line = line.strip()
    if not line:
      continue
    


test_inp = """

seed-to-soil map:
2988689842 4194451945 100515351
2936009234 3353543976 52680608

soil-to-fertilizer map:
3961802244 3774724750 90737174
3164426550 3931513861 70563571
147221566 1279409424 704464""".strip()

import re

pattern = re.compile(r"(?P<section>[a-z-]+ map):\n(?P<numbers>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)

for m in pattern.finditer(test_inp):
  print(m.groups())
  print("#" * 10)
