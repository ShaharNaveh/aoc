import enum
import pathlib

@enum.unique
class HandType(enum.IntEnum):
  HIGH_CARD = enum.auto()
  ONE_PAIR = enum.auto()
  TWO_PAIR = enum.auto()
  THREE_KIND = enum.auto()
  FULL_HOUSE = enum.auto()
  FOUR_KIND = enum.auto()
  FIVE_KIND = enum.auto()


CARD_VALUES = {
  **{str(num): num for num in range(2, 10)},
  **{c: num for num, c in enumerate("TJQKA")}
}

JOKER = "J"
JOKER_VALUE = 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        lines = file.read().splitlines()

    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


def part_one(lines: list[str]) -> int:
    hands = []
    bids = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append(hand)
        bids.append(int(bid))

    hand_bid_pairs = list(zip(hands, bids))
    hand_bid_pairs.sort(key=lambda pair: hand_to_score(pair[0]))

    total = 0
    for i, (_, bid) in enumerate(hand_bid_pairs):
        rank = i + 1
        total += rank * bid

    return total


def part_two(lines: List[str]) -> int:
    hands = []
    bids = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append(hand)
        bids.append(int(bid))

    hand_bid_pairs = list(zip(hands, bids))
    hand_bid_pairs.sort(key=lambda pair: hand_to_score(pair[0], True))

    total = 0
    for i, (_, bid) in enumerate(hand_bid_pairs):
        rank = i + 1
        total += rank * bid

    return total


# map each hand to a score such that better hands have higher scores
def hand_to_score(hand: str, use_joker=False) -> int:
    hand_type = get_hand_type(hand, use_joker)
    hand_tiebreaker = get_hand_tiebreaker(hand, use_joker)

    max_tiebreaker = get_hand_tiebreaker("AAAAA")
    score = TYPE_VALUES[hand_type] * max_tiebreaker + hand_tiebreaker
    return score


def get_hand_type(hand: str, use_joker=False) -> HandType:
    hand_counts = {}
    if use_joker:
        joker_count = 0
        for card in hand:
            if card == JOKER:
                joker_count += 1
            else:
                hand_counts[card] = hand_counts.get(card, 0) + 1

        if joker_count == 5:
            hand_counts["A"] = 5
        else:
            max_count = 0
            max_card = "A"
            for card, count in hand_counts.items():
                if count > max_count:
                    max_count = count
                    max_card = card

            hand_counts[max_card] += joker_count
    else:
        for card in hand:
            hand_counts[card] = hand_counts.get(card, 0) + 1

    if len(hand_counts) == 1:
        return HandType.FIVE_KIND

    if len(hand_counts) == 2:
        count = list(hand_counts.values())[0]
        if count == 1 or count == 4:
            return HandType.FOUR_KIND
        else:
            return HandType.FULL_HOUSE

    if len(hand_counts) == 3:
        for count in hand_counts.values():
            if count == 2:
                return HandType.TWO_PAIR

            if count == 3:
                return HandType.THREE_KIND

    if len(hand_counts) == 4:
        return HandType.ONE_PAIR

    return HandType.HIGH_CARD


# maps each hand to a tiebreaker between 0 and 10^10
def get_hand_tiebreaker(hand: str, use_joker=False) -> int:
    values = []
    for card in hand:
        if use_joker and card == JOKER:
            values.append(JOKER_VALUE)
        else:
            values.append(CARD_VALUES[card])

    tiebreaker = 0
    for value in values:
        tiebreaker = 100 * tiebreaker + value
    return tiebreaker


def p1(path):
  puzzle = path.read_text().strip()
  hands = sorted(map(Hand, puzzle.splitlines()))
  res = sum(rank * hand._bid for rank, hand in enumerate(hands, start=1))
  print(res)

def p2(path):
  puzzle = path.read_text().strip()
  hands = sorted(map(lambda line: Hand(line, is_p2=True), puzzle.splitlines()))
  res = sum(rank * hand._bid for rank, hand in enumerate(hands, start=1))
  print(res)
 
puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
