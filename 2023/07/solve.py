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

def hand_strength(hand: str, cards_strength: dict[str, int]) -> tuple[int, tuple[int, ...]]:
  hand_type = HandType.from_str(hand)
  cards = tuple(cards_strength[card] for card in hand)
  return (hand_type.value, cards)

def hand_strength_j(hand: str, cards_strength: dict[str, int]) -> tuple[int, tuple[int, ...]]:
  hands = {hand.replace("J", card) for card in set(hand)}
  return max(
    hand_strength(new_hand, cards_strength=cards_strength)
    for new_hand in hands
  )
  
def iter_puzzle(path):
  puzzle = path.read_text().strip()
  for line in puzzle.splitlines():
    hand, bid = line.split()
    yield (hand, int(bid))

def p1(path):
  it = sorted(iter_puzzle(path), key=lambda l: hand_strength(l[0], cards_strength=CARDS_STRENGTH))
  res = sum(rank * bid for rank, (_, bid) in enumerate(it, start=1))
  print(res)
  
def p2(path):
  it = sorted(iter_puzzle(path), key=lambda l: hand_strength_j(l[0], cards_strength=CARDS_STRENGTH))
  res = sum(rank * bid for rank, (_, bid) in enumerate(it, start=1))
  print(res)
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
