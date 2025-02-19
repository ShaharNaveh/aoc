import pathlib


def simulate(nums: tuple[int, ...], steps: int = 2020) -> int:
    last = nums[-1]
    turns = {num: turn for turn, num in enumerate(nums)}
    for turn in range(len(nums) - 1, steps - 1):
        turns[last], last = turn, turn - turns.get(last, turn)

    return last


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(map(int, inp.split(",")))


def p1(puzzle_file):
    return simulate(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return simulate(parse_puzzle(puzzle_file), 30_000_000)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
