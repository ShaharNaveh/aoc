import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

def read():
  yield from input_file.read_text().splitlines()

schematic = [cell for cell in cells.split('') for cells in read()]
print(schematic)
