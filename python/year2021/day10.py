import unittest

from utils import Day, main

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def autocomplete_score(todo: list[str]) -> int:
    score = 0
    for char in (PAIRS[c] for c in reversed(todo)):
        score *= 5
        score += ")]}>".index(char) + 1
    return score


def illegal_char(line: str) -> str | list[str]:
    buf = []
    for char in line:
        if char in PAIRS:
            buf.append(char)
        else:
            if char != PAIRS[buf.pop()]:
                return char

    return buf


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.splitlines()


class Day10(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(
            {")": 3, "]": 57, "}": 1197, ">": 25137}[char]
            for char in map(illegal_char, parsed)
            if isinstance(char, str)
        )

    def part2(self, parsed):
        scores = tuple(
            autocomplete_score(buf)
            for buf in map(illegal_char, parsed)
            if isinstance(buf, list)
        )
        return sorted(scores)[len(scores) // 2]


TEST_PUZZLE = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


class Tests(unittest.TestCase):
    DAY = Day10()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 26397)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 288957)


if __name__ == "__main__":
    main(Day10)
