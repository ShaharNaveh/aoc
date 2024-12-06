import pathlib

def hand_strength(hand: str, card_strength: dict[str, int]) -> int:
  cards = list(hand)
  order_strength = sum(
    cards_strength[card] * (10 ** order)
    for order, card in enumerate(reversed(cards), start=1)
  )
  
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
