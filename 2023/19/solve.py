import math
import operator
import pathlib
import re

def calc_accepted_parts(
        ranged_workflow: tuple[str, dict[str, range]], workflows: dict[str, callable]
) -> int:
    workflow, part = ranged_workflow

    if workflow == "R":
        return 0
    elif workflow == "A":
        return math.prod(len(rng) for rng in part.values())

    return sum(
        calc_accepted_parts(rworkflow, workflows) 
        for rworkflow in workflows[workflow](part)
    )

def bisect_range(rng: range, val: int) -> tuple[range, range]:
    return range(rng.start, val), range(val, rng.stop)

def build_ranged_workflow(raw_filters: str, fallback: str) -> callable:
    def get_next_dest(part: dict[str, range]) -> tuple[tuple[str, range], ...]:
        ranges = []

        for raw_filter in raw_filters.split(","):
            category, op, val, dest = parse_filter(raw_filter)

            if op == operator.gt:
                keep, send = bisect_range(part[category], val + 1)
            else:
                send, keep = bisect_range(part[category], val)

            ranges.append((dest, {**part, category: send}))
            part = {**part, category: keep}

        res = ranges + [(fallback, part)]
        return tuple(res)

    return get_next_dest

def is_part_accepted(part: dict[str, int], workflows, workflow: str = "in") -> bool:
    if workflow in ("A", "R"):
        return workflow == "A"
    return is_part_accepted(part, workflows, workflows[workflow](part))

def parse_filter(segment: str) -> tuple[str, callable, int, str]:
    category = segment[0]
    op = {">": operator.gt, "<": operator.lt}[segment[1]]
    raw_val, dest = segment[2:].split(":")
    return category, op, int(raw_val), dest

def build_workflow(raw_filters: str, fallback: str) -> callable:
    def get_next_dest(part: dict[str, int]) -> str:
        for raw_filter in raw_filters.split(","):
            category, op, val, dest = parse_filter(raw_filter)
            if op(part[category], val):
                return dest

        return fallback

    return get_next_dest

def parse_workflow(
    raw_workflow: str, builder: callable = build_workflow
) -> tuple[str, callable]:
    matched = re.search(r"(.*){(.*),(.*)}", raw_workflow)
    name, raw_filters, fallback = matched.groups()
    return name, builder(raw_filters, fallback)

def parse_puzzle(puzzle_file, *, is_p2: bool = False):
    inp = puzzle_file.read_text().strip()
    workflows_block, parts_block = inp.split("\n" * 2)

    if is_p2:
        workflows = dict(
            map(
                lambda raw_workflow: parse_workflow(
                    raw_workflow, build_ranged_workflow
                ),
                workflows_block.splitlines()
            )
        )
    else:
        workflows = dict(map(parse_workflow, workflows_block.splitlines()))

    parts = tuple(
        {
            char: int(num)
            for char, num in map(
                lambda sline: sline.split("="),
                line.removeprefix("{").removesuffix("}").split(",")
            )
        }
        for line in parts_block.splitlines()
    )
    return workflows, parts

def p1(puzzle_file):
    workflows, parts = parse_puzzle(puzzle_file)
    return sum(
        sum(part.values()) for part in parts if is_part_accepted(part, workflows)
    )

def p2(puzzle_file):
    workflows, _ = parse_puzzle(puzzle_file, is_p2=True)
    
    return calc_accepted_parts(
        ("in", {char: range(1, 4001) for char in "xmas"}),
        workflows,
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))




