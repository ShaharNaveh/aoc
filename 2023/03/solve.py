import pathlib

def read(path: pathlib.Path):
  yield from path.read_text().splitlines()
  
INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

schematic = [cell for cells in read(INPUT_PATH) for cell in cells.split('')]
print(schematic)
