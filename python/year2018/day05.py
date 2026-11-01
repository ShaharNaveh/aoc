import re
import string

from utils import Day, aoc_main

PATTERN = re.compile(
    "|".join(
        f"{char}{char.upper()}|{char.upper()}{char}" for char in string.ascii_lowercase
    )
)


def react(polymer: str) -> int:
    while PATTERN.search(polymer):
        polymer = PATTERN.sub("", polymer)
    return len(polymer)


class Day05(Day):
    def parse(self, input: str):
        inp = input.strip()
        return inp

    def part1(self, parsed):
        return react(parsed)

    def part2(self, polymer):
        return min(
            react(polymer.replace(char, "").replace(char.upper(), ""))
            for char in string.ascii_lowercase
        )


if __name__ == "__main__":
    aoc_main(Day05)
