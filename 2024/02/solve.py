import pathlib

inp_file = pathlib.Path(__file__).parent / "input.txt"

data = inp_file.read_text().splitlines()

levels = [list(map(int, line.split(" "))) for line in data]

def is_safe(level):
  if not (level == sorted(level)) or (level == sorted(level, reversed=True)):
    return False
    
  for n1, n2 in zip(level, level[1:]):
    diff = abs(n1 - n2)
    if diff > 3:
      return False
  return True


    
