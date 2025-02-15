import functools
import pathlib


@functools.cache
def blink(stone: int, count: int):
    if count == 0:
        return 1

    next_count = count - 1
    if stone == 0:
        return blink(1, next_count)
    elif ((stone_l := len((stone_s := str(stone)))) % 2) == 0:
        middle = stone_l // 2
        return blink(int(stone_s[:middle]), next_count) + blink(
            int(stone_s[middle:]), next_count
        )
    else:
        return blink(stone * 2024, next_count)


def p1(path):
    count = 25
    stones = parse_puzzle(path)
    res = sum(blink(stone, count) for stone in stones)
    print(res)


def p2(path):
    count = 75
    stones = parse_puzzle(path)
    res = sum(blink(stone, count) for stone in stones)
    print(res)


def parse_puzzle(path):
    inp = path.read_text().strip()
    puzzle = list(map(int, inp.split()))
    return puzzle


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
