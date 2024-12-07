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

  @classmethod
  def from_str(cls, hand: str):
    cards = list(hand)
    cards_unique = set(cards)
    cards_count = len(cards)
    cards_unique_count = len(cards_unique)
  
    if cards_unique_count == 1:
      hand_type = cls.FiveOfAKind
    elif (cards_unique_count == 2) and any(cards.count(card) == 4 for card in cards_unique):
      hand_type =  cls.FourOfAKind
    elif cards_unique_count == 2:
      hand_type = cls.FullHouse
    elif (cards_unique_count == 3) and any(cards.count(card) == 3 for card in cards_unique):
      hand_type = cls.ThreeOfAKind
    elif cards_unique_count == 3:
      hand_type = cls.TwoPairs
    elif cards_unique_count == 4:
      hand_type = cls.OnePair
    elif cards_unique_count == cards_count:
      hand_type = cls.HighCard
    return hand_type
  

CARDS_STRENGTH = {
  **{str(num): num for num in range(2, 10)},
  **{symbol: idx for idx, symbol in enumerate(list("TJQKA"), start=10)},
}


def hand_strength(
 hand: str, cards_strength: dict[str, int], *, base: int = 15, mul_start: int = 1
) -> int:
  order_strength = sum(
    cards_strength[card] * order
    for order, card in enumerate(hand, start=mul_start)
  )

  hand_type = HandType.from_str(hand)
  hand_type_strength = base ** (hand_type.value + len(hand) + mul_start + mul_start)
  strength = hand_type_strength + order_strength
  return strength
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
   # if hand not in {"KK677", 
    yield (hand, int(bid))

def p1(path):
  it = sorted(iter_puzzle(path), key=lambda l: hand_strength(l[0], cards_strength=CARDS_STRENGTH))
  res = sum(rank * bid for rank, (_, bid) in enumerate(it, start=1))
  print(res)
  return
  
  res = 0
  for rank, (card, bid) in enumerate(it, start=1):
    print(f"{rank=}\t{card=}\t{bid=}")
    res += rank * bid
  print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
#p2(puzzle_file)
