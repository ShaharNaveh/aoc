import collections
import pathlib
import re


def find_ore_required(reactions: dict, fuel: int = 1) -> int:
    need = collections.defaultdict(int, {"FUEL": fuel})
    have = collections.defaultdict(int)
    while True:
        chemical = next((chemical for chemical in need if chemical != "ORE"), None)
        if chemical is None:
            break

        quantity, inputs = reactions[chemical]
        quotient, remainder = divmod(need.pop(chemical), quantity)
        if remainder != 0:
            have[chemical] = quantity - remainder
            quotient += 1

        for iquantity, ichemical in inputs:
            need[ichemical] = need[ichemical] + quotient * iquantity - have[ichemical]
            have.pop(ichemical)

    return need["ORE"]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    reactions = {}
    for *raw_inputs, raw_output in map(
        lambda x: re.findall(r"\d+\s\w+", x), inp.splitlines()
    ):
        inputs = set()
        for raw_input in raw_inputs:
            quantity, chemical = raw_input.split()
            inputs.add((int(quantity), chemical))
        quantity, chemical = raw_output.split()
        reactions[chemical] = (int(quantity), frozenset(inputs))
    return reactions


def p1(puzzle_file):
    return find_ore_required(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    ORES = 1_000_000_000_000
    reactions = parse_puzzle(puzzle_file)
    fuel, search = 1, 2

    while find_ore_required(reactions, search) < ORES:
        fuel, search = search, search * 2

    while search - fuel >= 2:
        half = fuel + (search - fuel) // 2
        if find_ore_required(reactions, half) > ORES:
            search = half
        else:
            fuel = half
    return fuel


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
