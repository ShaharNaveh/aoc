import collections
import pathlib
import re


def play(max_players: int, last_marble: int) -> int:
    scores = collections.defaultdict(int)
    circle = collections.deque([0])
    for marble in range(1, last_marble + 1):
        if (marble % 23) == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores.values())


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return map(int, re.findall(r"(\d+)", inp))


def p1(puzzle_file):
    return play(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    max_players, last_marble = parse_puzzle(puzzle_file)
    return play(max_players, last_marble * 100)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
