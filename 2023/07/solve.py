import enum
import functools
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

CARDS_STRENGTH_P2 = CARDS_STRENGTH.copy() | {"J": 1}

def hand_strength(hand: str, cards_strength: dict[str, int] = CARDS_STRENGTH) -> tuple[int, tuple[int, ...]]:
  hand_type = HandType.from_str(hand)
  cards = tuple(cards_strength[card] for card in hand)
  return (hand_type.value, cards)

def max_hand_strength_j(hand: str):
  hands = {hand.replace("J", card) for card in set(hand)} # Maybe exclude J
  return max(hand_strength(new_hand, CARDS_STRENGTH_P2) for new_hand in hands)

@functools.cmp_to_key
def cmp_hands_j(tup1: tuple, tup2: tuple, cards_strength: dict[str, int] = CARDS_STRENGTH_P2) -> bool:
  hand1, _ = tup1
  hand2, _ = tup2
  if all("J" not in hand for hand in (hand1, hand2)):
    hs1 = hand_strength(hand1, cards_strength=cards_strength)
    hs2 = hand_strength(hand2, cards_strength=cards_strength)
    if hs1 > hs2:
      return 1
    elif hs1 == hs2:
      return 0
    else:
      return -1

  hs1 = max_hand_strength_j(hand1)
  hs2 = max_hand_strength_j(hand2)
  if hs1 != hs2:
    if hs1 > hs2:
      return 1
    else:
      return -1

  hs1 = hand_strength(hand1, cards_strength=cards_strength)
  hs2 = hand_strength(hand2, cards_strength=cards_strength)
  if hs1 > hs2:
    return 1
  elif hs1 == hs2:
    return 0
  else:
    return -1
  
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
  it = sorted(iter_puzzle(path), key=cmp_hands_j, reverse=False)
  res = sum(rank * bid for rank, (_, bid) in enumerate(it, start=1))
  print(res)
  it = sorted(iter_puzzle(path), key=cmp_hands_j, reverse=True)
  res = sum(rank * bid for rank, (_, bid) in enumerate(it, start=1))
  print(res)
  
  
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
