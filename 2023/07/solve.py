import pathlib

CARDS_STRENGTH = {
  **{str(num): num for num in range(2, 10)},
  **{symbol: idx for idx, symbol in enumerate(list("TJQKA"), start=10)},
}

def hand_strength(
 hand: str, cards_strength: dict[str, int], *, base: int = 10
) -> int:
  cards = list(hand)
  order_strength = sum(
    (base ** order) + cards_strength[card]
    for order, card in enumerate(reversed(cards), start=1)
  )
  
  cards_count = len(cards)
  cards_unique = set(cards)
  cards_unique_count = len(cards_unique)

  type_strength = 0
  
  if cards_unique_count == 1:
    # Five of a Kind
    type_strength = 6 
  elif cards_unique_count == 2:
    # Four of a Kind
    type_strength =  5
  elif (cards_unique_count == 3) and any(cards.count(card) == 3 for card in cards_unique):
    # Three of a Kind
    type_strength = 4
  elif cards_unique_count == 3:
    # Two Pairs
    type_strength = 3
  elif cards_unique_count == cards_count:
    # High Card
    type_strength = 2

  if type_strength == 0:
    
    print(f"{hand=}")
    print(f"{cards=}")
    print(f"{cards_count=}")
    print(f"{cards_unique=}")
    print(f"{cards_unique_count=}")
   
  
  base_type_strength = base ** (cards_count + type_strength)
  return base_type_strength + order_strength
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))

def p1(path):
 it = sorted(iter_puzzle(path), key=lambda l: hand_strength(l[0], cards_strength=CARDS_STRENGTH), reverse=True)
 res = 0
 for rank, (_, bid) in enumerate(it, start=1):
   res += rank * bid
 print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
