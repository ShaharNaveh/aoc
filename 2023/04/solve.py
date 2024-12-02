import pathlib

INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

cards = INPUT_FILE.read_text().splitlines()

def parse_line(line):
  title, numbers = line.split(":")
  card_id = int(title.split(" ")[1])

  winning, have = numbers.strip().split("|")
  parse_numbers = lambda n: {int(x) for x in n.strip().split(" ") if x.strip() != ""}
  winning = parse_numbers(winning)
  have = parse_numbers(have)
  entry = {card_id: {"winning": winning, "have": have}}
  yield entry

