import collections
import enum
import functools
import pathlib
import re
#from typing import Sequence

CARDS_STRENGTH = {
  **{str(num): num for num in range(2, 10)},
  **{symbol: idx for idx, symbol in enumerate(list("TJQKA"), start=10)},
}

@enum.unique
class HandType(enum.IntEnum):
  HighCard = enum.auto()
  OnePair = enum.auto()
  TwoPairs = enum.auto()
  ThreeOfAKind = enum.auto()
  FullHouse = enum.auto()
  FourOfAKind = enum.auto()
  FiveOfAKind = enum.auto()

  @classmethod
  def detect(cls, hand: str):
    counts = sorted(collections.Counter(hand).values(), reverse=True)
    
    if counts[0] == 5:
      return cls.FiveOfAKind

    if counts[0] == 4:
      return cls.FourOfAKind

    if (counts[0] == 3) and (counts[1] == 2):
      return cls.FullHouse 
    elif counts[0] == 3:
      return cls.ThreeOfAKind

    if all(count == 2 for count in counts[:2]):
      return cls.TwoPairs
    elif counts[0] == 2:
      return cls.OnePair

    if counts[0] == 1:
      return cls.HighCard
      
    raise ValueError(f"Could not determine the hand type of: {repr(hand)}")     

def cmp(a, b, *, cards_strength=None) -> int:
  type_a = HandType.detect(a)
  type_b = HandType.detect(b)

  if type_a > type_b:
    return 1
  elif type_b > type_a:
    return -1

  cards_strength = cards_strength if cards_strength else CARSS_STRENGTH
  for i, j in zip(a, b):
    i_strength = cards_strength[i]
    j_strength = cards_strength[j]
    
    if i_strength > j_strength:
      return 1
    elif j_strength > i_strength:
      return -1
  return 0

def iter_puzzle(path):
  puzzle = path.read_text().strip()
  return re.findall(r"(\w{5}) (\d+)", puzzle)

def p1(path):
  hands = iter_puzzle(path)
  it = sorted(hands, key=functools.cmp_to_key(lambda a, b: cmp(a[0], b[0])))
  res = 0
  for rank, (_, bid) in enumerate(it, start=1):
    bid = int(bid)
    res += bid * rank
    
  print(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"


p1(puzzle_file)
#p2(puzzle_file)
