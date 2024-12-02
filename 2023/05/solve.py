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
    frm, to = section.rstrip(" map").split("-to-")
    print(frm)
    print(to)
    print(data)
  
parse_raw(raw)  


test_inp = """

seed-to-soil map:
2988689842 4194451945 100515351
2936009234 3353543976 52680608

soil-to-fertilizer map:
3961802244 3774724750 90737174
3164426550 3931513861 70563571
147221566 1279409424 704464""".strip()
