import operator
import pathlib

inp_file = pathlib.Path(__file__).parent / "input.txt"

data = inp_file.read_text().splitlines()

levels = [list(map(int, line.split(" "))) for line in data]

def is_safe(level):
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
  
def p2(levels):
  for level in levels:
    for idx in range(len(level)):
      lvl = level[:idx] + level[idx+1:]
      if is_safe(lvl):
        yield 1
        break
    
print(sum(map(is_safe, levels)))
    
print(sum(p2(levels)))
