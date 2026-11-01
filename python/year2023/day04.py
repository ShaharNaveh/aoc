import unittest

from utils import Day, main


def parse_line(line):
    title, numbers = line.strip().split(":")
    card_id = int(title.strip().split(" ")[-1])

    winning, have = numbers.strip().split("|")
    parse_numbers = lambda n: {int(x) for x in n.strip().split(" ") if x.strip() != ""}
    winning = parse_numbers(winning)
    have = parse_numbers(have)
    entry = {card_id: {"winning": winning, "have": have}}
    return entry


def calc_won_points(card):
    count = matches_count(card)
    if count == 0:
        return 0
    return 2 ** (count - 1)


def matches_count(card):
    values = next(iter(card.values()))
    winning, have = values["winning"], values["have"]
    overlap = winning & have
    count = len(overlap)
    return count


def solve_p2(cards):
    # yield len(cards)
    counter = [1] * len(cards)
    for i, card in enumerate(cards):
        count = matches_count(card)
        for num in range(count):
            counter[i + num + 1] += counter[i]
    return sum(counter)


def solve_p1(cards):
    yield from map(calc_won_points, cards)


class Day04(Day):
    def parse(self, inp: str):
        return list(map(parse_line, inp.splitlines()))

    def part1(self, cards) -> int:
        return sum(solve_p1(cards))

    def part2(self, cards) -> int:
        return solve_p2(cards)


EXAMPLE = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day04()
        self.assertEqual(d.part1(d.parse(EXAMPLE)), 13)

    def test_part2(self):
        d = Day04()
        self.assertEqual(d.part2(d.parse(EXAMPLE)), 30)


if __name__ == "__main__":
    main(Day04)
