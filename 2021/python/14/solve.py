import collections
import pathlib


def solve(template: str, rules: dict[tuple[str, str], str], steps: int = 10) -> int:
    counter = collections.Counter(template)
    elements = collections.Counter(zip(template, template[1:]))
    for _ in range(steps):
        for tup, num in list(elements.items()):
            if not num:
                continue

            elements[tup] -= num
            out = rules[tup]

            l, r = tup
            elements[(l, out)] += num
            elements[(out, r)] += num

            counter[out] += num

    vals = counter.values()
    return max(vals) - min(vals)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    template, raw_rules = inp.split("\n" * 2)
    rules = {
        tuple(k): v for k, v in map(lambda l: l.split(" -> "), raw_rules.splitlines())
    }
    return template, rules


def p1(puzzle_file):
    return solve(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return solve(*parse_puzzle(puzzle_file), steps=40)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
