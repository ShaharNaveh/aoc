import pathlib


def p1(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = set(map(lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()))
  print(rules)
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  print(updates)


input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
