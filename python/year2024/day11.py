import functools

from utils import Day, run


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


class Day11(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        puzzle = list(map(int, inp.split()))
        return puzzle

    def part1(self, parsed):
        count = 25
        stones = parsed
        res = sum(blink(stone, count) for stone in stones)
        return res

    def part2(self, parsed):
        count = 75
        stones = parsed
        res = sum(blink(stone, count) for stone in stones)
        return res


if __name__ == "__main__":
    run(Day11)
