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
    
