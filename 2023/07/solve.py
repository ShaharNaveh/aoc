import enum
import pathlib

@enum.unique
class HandType(enum.Enum):
  HighCard = enum.auto()
  OnePair = enum.auto()
  TwoPairs = enum.auto()
  ThreeOfAKind = enum.auto()
  FullHouse = enum.auto()
  FourOfAKind = enum.auto()
  FiveOfAKind = enum.auto()

CARDS_STRENGTH = {
  **{str(num): num for num in range(2, 10)},
  **{symbol: idx for idx, symbol in enumerate(list("TJQKA"), start=10)},
}

def hand_strength(
 hand: str, cards_strength: dict[str, int], *, base: int = 10
) -> int:
  cards = list(hand)
  #order_strength = sum(
   # (base ** order) + cards_strength[card]
   # for order, card in enumerate(reversed(cards), start=2)
 # )
  print()
  print("*" * 10)
  print()
  order_strength = 0
  for order, card in enumerate(reversed(cards), start=2):
    strength = (base ** order) + cards_strength[card]
    print(f"{card=}\t{strength=}")
    order_strength += strength
  
  cards_count = len(cards)
  cards_unique = set(cards)
  cards_unique_count = len(cards_unique)
  
  if cards_unique_count == 1:
    hand_type = HandType.FiveOfAKind
  elif (cards_unique_count == 2) and any(cards.count(card) == 4 for card in cards_unique):
    hand_type =  HandType.FourOfAKind
  elif cards_unique_count == 2:
    hand_type = HandType.FullHouse
  elif (cards_unique_count == 3) and any(cards.count(card) == 3 for card in cards_unique):
    hand_type = HandType.ThreeOfAKind
  elif cards_unique_count == 3:
    hand_type = HandType.TwoPairs
  elif cards_unique_count == 4:
    hand_type = HandType.OnePair
  elif cards_unique_count == cards_count:
    hand_type = HandType.HighCard
  
  hand_type_strength = base ** (hand_type.value + cards_count + 1)
  strength = hand_type_strength + order_strength
  if True:
    print(f"{hand=}")
    print(f"{hand_type=}")
    print(f"{cards=}")
    print(f"{cards_count=}")
    print(f"{cards_unique=}")
    print(f"{cards_unique_count=}")
    print(f"{order_strength=}")
    print(f"{hand_type_strength=}")
    print(f"{strength=}")
    print()
    print("*" * 10)
  return strength
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))

def p1(path):
 it = sorted(iter_puzzle(path), key=lambda l: hand_strength(l[0], cards_strength=CARDS_STRENGTH))
 res = 0
 for rank, (card, bid) in enumerate(it, start=1):
   print(f"{rank=}\t{card=}\t{bid=}")
   res += rank * bid
 print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
