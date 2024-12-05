import pathlib
import functools

def is_in_order(update: list[int], rules: set) -> bool:
  for rule in rules:
    before, after = rule.real, rule.imag
    if not all(x in update for x in (before, after)):
      continue
    if update.index(before) > update.index(after):
      return False
      
  return True

def middle_page(update: list[int]) -> int:
  idx = (len(update) - 1) // 2
  return update[idx]
  
def p1(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = set(map(lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()))
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  func = functools.partial(is_in_order, rules=rules)
  res = sum(map(middle_page, filter(func, updates)))
  print(res)

input_file = pathlib.Path(__file__).parent / "input.txt"
#input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
