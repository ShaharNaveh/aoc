import re

from utils import Day, run


class Day03(Day):
    def parse(self, inp: str) -> str:
        return inp

    def part1(self, text):
        pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)", re.MULTILINE)
        res = 0
        for m in re.findall(pattern, text):
            n1, n2 = map(int, m.lstrip("mul(").rstrip(")").split(","))
            res += n1 * n2
        return res

    def part2(self, text):
        pattern = re.compile(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", re.MULTILINE)
        res = 0
        do = True
        for m in re.findall(pattern, text):
            if m.startswith("do"):
                do = "don't" not in m
                continue

            if not do:
                continue

            n1, n2 = map(int, m.lstrip("mul(").rstrip(")").split(","))
            res += n1 * n2
        return res


if __name__ == "__main__":
    run(Day03)
