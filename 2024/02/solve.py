import pathlib

inp_file = pathlib.Path(__file__).parent / "input.txt"

data = inp_file.read_text().splitlines()

levels = [list(map(int, line.split(" "))) for line in data]

def p1(level):
  slevel = sorted(level)
  if not ((level == slevel) or (level == sorted(level, reverse=True))):
    return False
    
  for n1, n2 in zip(slevel, slevel[1:]):
    if n1 == n2:
      return False
      
    diff = abs(n1 - n2)
    if diff > 3:
      return False
  return True

print(sum(map(p1, levels)))
    
