import collections
import pathlib

def card_strength(card: str, is_p2: bool = False) -> int:
 	if card.isnumeric():   
	   return int(card)
   
 	dct = {c: idx for idx, c in enumerate("TJQKA", start=10)}
  if is_p2:
    dct["J"] = -1
 	return dct[card]

class Hand:
  __slots__ = ("_cards", "_bid", "_typ", "_is_p2")

 	def __init__(self, line: str, *, is_p2: bool = True):
	  	raw, bid = line.split()
	  	self._bid = int(bid)
  		self._cards = tuple(card_strength(c, is_p2=is_p2) for c in raw)
 	 	self._typ = self.detect_type()
    self._is_p2 = is_p2

 	def detect_type(self):
	  	counter = collections.Counter(self._cards)
  		highest = max(counter.values())
  		if is_p2:
	   		wilds = counter[1]
		   	del counter[1]
	   		highest = wilds
		   	if counter:
		    		highest += max(counter.values())

	  	if highest == 5:
		   	return 6 # Five of a kind
  		elif highest == 4:
		   	return 5 # Four of a kind
  		elif len(counter) == 2:
		   	return 4 # Full house
  		elif highest == 3:
		   	return 3 # Three of a kind
  		elif len(counter) == 3:
		   	return 2 # Two pair
  		elif highest == 2:
		   	return 1 # One pair
	  	else:
		   	return 0 # High card
     
 	def __lt__(self, other):
	  	return self._typ < other._typ or (self._typ == other._typ and self._cards < other._cards)

def p1(path):
  puzzle = path.read_text().strip()
  hands = sorted(map(Hand, puzzle.splitlines()))
  res = sum(rank * hand._bid for rank, hand in hands)
  print(res)

def p2(path):
  puzzle = path.read_text().strip()
  hands = sorted(map(lambda line: Hand(line, is_p2=True, puzzle.splitlines()))
  res = sum(rank * hand._bid for rank, hand in hands)
  print(res)
 
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
