import collections
import pathlib

def hand_strength(hand: str, card_strength: dict[str, int], *, base: int = 10) -> int:
  cards = list(hand)
  order_strength = sum(
    (base ** order) + cards_strength[card]
    for order, card in enumerate(reversed(cards), start=1)
  )
  
  card_count = len(cards)
  card_counter = 
  
  if len(set(cards)) == 1:
    # Five of a Kind
    kind_strength = base ** (card_count + 6)
    return kind_strength + order_strength

  if len(set(cards)) == card_count:
    kind_strength = base ** (card_count + 2)
    return kind_strength + order_strength
    
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
