import pathlib
import re

BAG = "shiny gold"


def can_hold(bag: str, bags: dict[str, dict[int, str]]) -> bool:
    inner_bags = bags[bag]
    if BAG in inner_bags:
        return True
    return any(can_hold(inner_bag, bags) for inner_bag in inner_bags)


def hold_count(bag: str, bags: dict[str, dict[int, str]]) -> int:
    inner_bags = bags[bag]
    if not inner_bags:
        return 0
    return sum(inner_bags.values()) + sum(
        amount * hold_count(inner_bag, bags) for inner_bag, amount in inner_bags.items()
    )


def parse_puzzle(puzzle_file) -> dict[str, dict[int, str]]:
    inp = puzzle_file.read_text().strip()

    return {
        bag: {
            name: int(amount)
            for amount, name in re.findall(r"(\d) (\w+ \w+)", raw_bags)
        }
        for line in inp.splitlines()
        for bag, raw_bags in re.findall(r"(\w+ \w+) bags contain (.*)", line)
    }


def p1(puzzle_file):
    bags = parse_puzzle(puzzle_file)
    return sum(can_hold(bag, bags) for bag in bags)


def p2(puzzle_file):
    return hold_count(BAG, parse_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
