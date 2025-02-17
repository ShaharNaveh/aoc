import collections
import functools
import pathlib


def parse_rules(rule_block: str) -> dict[int, set[int]]:
    rules = map(
        lambda line: complex(*map(int, line.split("|"))), rule_block.splitlines()
    )

    result = collections.defaultdict(set)
    for rule in rules:
        before, after = int(rule.real), int(rule.imag)
        result[before] |= {after}

    return dict(result)


def is_update_correct(update: list[int], rules: dict[int, set[int]]) -> bool:
    for idx, num in enumerate(update):
        befores = set(update[:idx])
        afters = rules.get(num, set())
        if befores & afters:
            return False
    return True


def fix_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    func = lambda before, after: (before in rules.get(after, set())) - 1
    res = sorted(update, key=functools.cmp_to_key(func))
    return res


def middle_page(update: list[int]) -> int:
    idx = (len(update) - 1) // 2
    return update[idx]


def p1(path):
    inp = path.read_text().strip()
    rule_block, update_block = inp.split("\n" * 2)

    rules = parse_rules(rule_block)
    updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]

    good_updates = filter(lambda update: is_update_correct(update, rules), updates)
    res = sum(map(middle_page, good_updates))
    print(res)


def p2(path):
    inp = path.read_text().strip()
    rule_block, update_block = inp.split("\n" * 2)

    rules = parse_rules(rule_block)
    updates = [list(map(int, line.split(","))) for line in update_block.splitlines()]

    bad_updates = filter(lambda update: not is_update_correct(update, rules), updates)
    fixed_updates = map(lambda update: fix_update(update, rules), bad_updates)
    res = sum(map(middle_page, fixed_updates))
    print(res)


input_file = pathlib.Path(__file__).parent / "input.txt"
# input_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(input_file)
p2(input_file)
