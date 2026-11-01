import re
import unittest

from utils import Day, run

CUBE_LIMIT = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game_line(line: str):
    game_id = int(re.findall(r"Game (\d+)", line)[0])
    game = {game_id: {}}

    for color in ("red", "green", "blue"):
        cubes = re.findall(rf"(\d+) {color}", line)
        cubes = list(map(int, cubes))
        game[game_id][color] = cubes

    return game


def is_game_possible(game) -> bool:
    cubes_dict = next(iter(game.values()))
    for color, cubes in cubes_dict.items():
        if max(cubes) > CUBE_LIMIT[color]:
            return False
    return True


def solve_p1(games):
    for game in filter(is_game_possible, games):
        yield next(iter(game.keys()))


def max_cubes_color(game):
    cubes_dict = next(iter(game.values()))
    for cubes in cubes_dict.values():
        yield max(cubes)


def solve_p2(games):
    for game in games:
        r, g, b = max_cubes_color(game)
        yield r * g * b


class Day02(Day):
    def parse(self, inp: str):
        return list(map(parse_game_line, map(str.strip, inp.splitlines())))

    def part1(self, games) -> int:
        return sum(solve_p1(games))

    def part2(self, games) -> int:
        return sum(solve_p2(games))


EXAMPLE = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day02()
        self.assertEqual(d.part1(d.parse(EXAMPLE)), 8)

    def test_part2(self):
        d = Day02()
        self.assertEqual(d.part2(d.parse(EXAMPLE)), 2286)


if __name__ == "__main__":
    run(Day02)
