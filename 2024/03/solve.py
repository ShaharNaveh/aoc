import pathlib
import re

input_file = pathlib.Path(__file__).parent / "input.txt"

def p1(path):
  text = path.read_text()
  pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)", re.MULTILINE)
  res = 0
  for m in re.findall(pattern, text):
    n1, n2 = map(int, m.lstrip("mul(").rstrip(")").split(","))
    res += n1 * n2
  print(res)

p1(input_file)
