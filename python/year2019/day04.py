import itertools

from utils import Day, main


def is_valid_password(num: int, *, is_p2: bool = False) -> bool:
    s = str(num)

    if len(s) != 6:
        return False

    for _, group in itertools.groupby(s):
        size = len(list(group))
        if (is_p2 and (size == 2)) or ((not is_p2) and (size >= 2)):
            break
    else:
        return False

    if s != "".join(sorted(s)):
        return False

    return True


class Day04(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        start, stop = map(int, inp.split("-"))
        return range(start, stop + 1)

    def part1(self, parsed):
        return sum(map(is_valid_password, parsed))

    def part2(self, parsed):
        return sum(is_valid_password(num, is_p2=True) for num in parsed)


if __name__ == "__main__":
    main(Day04)
