#!/usr/bin/env python
import pathlib
import re

DATA_FILE = pathlib.Path(__file__).parent / "data.txt"
with DATA_FILE.open() as fd:
  lines = fd.readlines()
  
lines = map(str.strip, data)

def parse_game_line(line: str):
  game_id = int(re.findall("Game (\d+)", line)[0])
  game = {game_id: {}}
  
  for color in ("red", "green", "blue"):
    cubes = re.findall(fr"(\d+) {color}", line)
    game[game_id][color] = cubes
    
  return game

def is_game_possible(game) -> bool:
  cubes_dict = game.values()
  
games = map(parse_game_line, lines)
