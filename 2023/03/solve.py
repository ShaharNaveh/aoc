import pathlib

def read(path: pathlib.Path):
  yield from map(str.strip, path.read_text().splitlines())
  
INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

schematic = [list(line) for line in read(INPUT_FILE)]
schematic_size = (sum(1 for _ in next(schematic)), len(schematic))
print(schematic_size)
