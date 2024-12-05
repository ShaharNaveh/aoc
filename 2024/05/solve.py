import pathlib

def build_rules(rules: set[complex]) -> list[int]:
  result = []
  for rule in rules:
    before, after = int(rule.real), int(rule.imag)
  
def is_in_order(update: list[int], rules: set[complex]) -> bool:
  for rule in rules:
    before, after = rule.real, rule.imag
    if not all(x in update for x in (before, after)):
      continue
    if update.index(before) > update.index(after):
      return False
      
  return True

def fix_update(update: list[int], rules: set[complex]) -> list[int]:
  pass
  
def middle_page(update: list[int]) -> int:
  idx = (len(update) - 1) // 2
  return update[idx]
  
def p1(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = set(map(lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()))
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  
  good_updates = filter(lambda update: is_in_order(update, rules), updates)
  res = sum(map(middle_page, good_updates))
  print(res)

def p2(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = set(map(lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()))
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  
  bad_updates = filter(lambda update: not is_in_order(update, rules), updates)
  fixed_updates = map(lambda update: fix_update(update, rules), bad_updates)
  res = sum(map(middle_page, fixed_updates))          
  print(res)

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
p2(input_file)
