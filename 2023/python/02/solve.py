#!/usr/bin/env python
import pathlib
import re

DATA_FILE = pathlib.Path(__file__).parent / "data.txt"
with DATA_FILE.open() as fd:
    lines = fd.readlines()

lines = map(str.strip, lines)

CUBE_LIMIT = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game_line(line: str):
    game_id = int(re.findall("Game (\d+)", line)[0])
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


games = list(map(parse_game_line, lines))

print(sum(solve_p1(games)))
print(sum(solve_p2(games)))
