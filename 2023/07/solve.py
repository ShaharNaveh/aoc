import pathlib

CARD_STRENGTH = {
  **{str(num): num for num in range(2, 10)},
  **{symbol: idx for idx, symbol in enumerate(list("TJQKA"), start=10)},
}  

def hand_strength(hand: str, card_strength: dict[str, int], *, base: int = 10) -> int:
  cards = list(hand)
  order_strength = sum(
    (base ** order) + cards_strength[card]
    for order, card in enumerate(reversed(cards), start=1)
  )
  
  cards_count = len(cards)
  cards_unique = set(cards)
  cards_unique_count = len(cards_unique)
  
  if unique_unique_count == 1:
    # Five of a Kind
    kind_strength = base ** (cards_count + 6) 
  elif cards_unique_count == 2:
    # Four of a Kind
    kind_strength =  5
  elif unique_cards_len == 3:
    # Two of a Kind
    type_strength = 3

    if any(cards.count(card) == 3 for card in unique_cards):
      # Three of a Kind
      type_strength = 4

  elif unique_cards_len == card_count:
    # High Card
    type_strength = base ** (card_count + 2)
    
  base_type_strength = base ** (cards_count + type_strength)
  return base_type_strength + order_strength  
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))

def p1(path):
 it = sorted(iter_puzzle(path), key=lambda l: hand_strength(l[0]), reverse=True)
 res = 0
 for rank, _, bid in enumerate(it, start=1):
   res += rank * bid
 print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
