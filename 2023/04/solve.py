import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

data = INPUT_FILE.read_text().splitlines()

def parse_line(line):
  title, numbers = line.split(":")
  card_id = int(title.split(" ")[1])

  winning, have = numbers.strip().split("|")
  parse_numbers = lambda n: [int(x) for x in n.strip().split(" ") if x.strip() != ""]
  winning = parse_numbers(winning)
  have = parse_numbers(have)
  entry = {card_id: {"winning": winning, "have": have}}
  yield entry

def calc_won_points(card):
  values = next(iter(card.values()))
  winning, have = values["winning"], values["have"]
  count = 0
  for num in have:
    if num in winning:
      count += 1
      
  mul = min(count, 2)
  return count * mul              
  
def solve_p1(cards):
  yield from map(calc_won_points, cards)
  
cards = list(map(parse_line, data))
print(cards)

print(sum(solve_p1(cards)))
