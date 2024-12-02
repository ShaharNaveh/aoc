import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

data = INPUT_FILE.read_text().splitlines()

def parse_line(line):
  title, numbers = line.strip().split(":")
  card_id = int(title.strip().split(" ")[-1])

  winning, have = numbers.strip().split("|")
  parse_numbers = lambda n: {int(x) for x in n.strip().split(" ") if x.strip() != ""}
  winning = parse_numbers(winning)
  have = parse_numbers(have)
  entry = {card_id: {"winning": winning, "have": have}}
  return entry

def calc_won_points(card):
  values = next(iter(card.values()))
  winning, have = values["winning"], values["have"]
  
  overlap = winning & have
  count = len(overlap)   
  mul = min(count, 2)
  res = count * mul

  print(winning)
  print(have)
  print(count)
  print(mul)
  print(res)
  
  return res
  
def solve_p1(cards):
  yield from map(calc_won_points, cards)
  
cards = list(map(parse_line, data))

#print(sum(solve_p1(cards)))

inp = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip().splitlines()

tmp = list(map(parse_line, inp))

print(sum(solve_p1(tmp)))
