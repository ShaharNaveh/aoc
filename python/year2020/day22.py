import unittest

from utils import Day, aoc_main


def play_combat(deck1: list[int], deck2: list[int]) -> tuple[list[int], list[int]]:
    while deck1 and deck2:
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if card1 > card2:
            deck1.extend([card1, card2])
        else:
            deck2.extend([card2, card1])
    return deck1, deck2


def play_recursive_combat(
    deck1: list[int], deck2: list[int]
) -> tuple[list[int], list[int]]:
    seen = set()
    while deck1 and deck2:
        if (key := tuple(deck1)) in seen:
            return deck1, []
        seen.add(key)

        card1, card2 = deck1.pop(0), deck2.pop(0)
        if (card1 <= len(deck1)) and (card2 <= len(deck2)):
            if play_recursive_combat(deck1[:card1].copy(), deck2[:card2].copy())[0]:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        else:
            if card1 > card2:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])

    return deck1, deck2


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from (
        list(map(int, raw_player.splitlines()[1:]))
        for raw_player in inp.split("\n" * 2)
    )


def find_deck_score(decks) -> int:
    return sum(
        card * idx for deck in decks for idx, card in enumerate(reversed(deck), 1)
    )


class Day22(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return find_deck_score(play_combat(*parsed))

    def part2(self, parsed):
        return find_deck_score(play_recursive_combat(*parsed))


TEST_PUZZLE = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day22()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 306)

    def test_part2_test_puzzle(self):
        d = Day22()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 291)


if __name__ == "__main__":
    aoc_main(Day22)
