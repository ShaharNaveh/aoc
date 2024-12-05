import pathlib

def parse_rules(rule_block: str) -> list[int]:
  rules = map(lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines())
  
  result = []
  for rule in rules:
    before, after = int(rule.real), int(rule.imag)
    is_before_in = before in result
    is_after_in = after in result
    
    if is_before_in and is_after_in:
      continue

    if is_before_in and not is_after_in:
      before_idx = result.index(before)
      result.insert(before_idx + 1, after)
    elif is_after_in and not is_before_in:
      after_idx = result.index(after)
      result.insert(after_idx, after)
    else:
      result.insert(0, after)
      result.insert(0, before)

    #print(result)

  return result
  
def is_update_ok(update: list[int], key: callable) -> bool:
  return update == fix_update(update, key=key)

def fix_update(update: list[int], key: callalbe) -> list[int]:
  return sorted(update, key=key)
  
def middle_page(update: list[int]) -> int:
  idx = (len(update) - 1) // 2
  return update[idx]
  
def p1(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
  
  rules = parse_rules(rule_block)
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  
  good_updates = filter(lambda update: is_update_ok(update, rules.index), updates)
  res = sum(map(middle_page, good_updates))
  print(res)

def p2(path):
  inp = path.read_text().strip()
  rule_block, update_block = inp.split("\n" * 2)
 
  rules = parse_rules(rule_block)
  updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]
  
  bad_updates = filter(lambda update: not is_update_ok(update, rules.index), updates)
  fixed_updates = map(lambda update: fix_update(update, rules.index), bad_updates)
  res = sum(map(middle_page, fixed_updates))          
  print(res)

input_file = pathlib.Path(__file__).parent / "input.txt"
input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
p2(input_file)
