import pathlib


def p1(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = set()
  for line in rule_block.splitlines():
    rules |= set(map(int, line.split("|")))
    
  updates = set()
  for line in update_block.splitlines():
    updates |= {tuple(map(int, line.split(",")))}

  for update in updates:
    if not set(update).issubset(rules):
      print(update)


    



input_file = pathlib.Path(__file__).parent / "input.txt"

p1(input_file)
