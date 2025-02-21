import pathlib
import re

T = "({})"


def build_pattern(
    rule: str, rules: dict[str, str], *, depth: int = 0, max_depth: int = 100
) -> str:
    if depth >= max_depth:
        return ""

    ndepth = depth + 1

    if "|" in rule:
        return T.format(
            "|".join(
                T.format(build_pattern(nrule, rules, depth=ndepth))
                for nrule in rule.split("|")
            )
        )
    elif " " in rule:
        return T.format(
            "".join(build_pattern(nrule, rules, depth=ndepth) for nrule in rule.split())
        )

    name = rules[rule]
    if name.isalpha():
        return name
    return build_pattern(name, rules, depth=ndepth)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_rules, raw_messages = inp.split("\n" * 2)

    rules = {
        name: rule.replace('"', "")
        for name, rule in re.findall(r"(\d+): (.*)", raw_rules, re.MULTILINE)
    }

    return rules, raw_messages.splitlines()


def p1(puzzle_file):
    rules, messages = parse_puzzle(puzzle_file)
    raw_pattern = build_pattern(rules["0"], rules)
    pattern = re.compile(f"^({raw_pattern})$")
    return sum(bool(pattern.search(message)) for message in messages)


def p2(puzzle_file):
    rules, messages = parse_puzzle(puzzle_file)
    raw_pattern = build_pattern(
        rules["0"], rules | {"8": "42 | 42 8", "11": "42 31 | 42 11 31"}
    )
    pattern = re.compile(f"^({raw_pattern})$")
    return sum(bool(pattern.search(message)) for message in messages)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
