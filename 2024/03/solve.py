import pathlib
import re

input_file = pathlib.Path(__file__).parent / "input.txt"

def p1(path):
  text = path.read_text()
  pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)", re.MULTILINE)
  for m in re.findall(pattern, text):
    print(m)
  

p1()
