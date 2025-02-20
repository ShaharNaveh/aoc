import math
import pathlib
import re
import typing


class Field(typing.NamedTuple):
    name: str
    rules: tuple[range, range]

    def __contains__(self, x: int) -> bool:
        return any(x in rule for rule in self.rules)

    @classmethod
    def from_str(cls, raw: str) -> "Field":
        name, raw_rules = raw.split(":")

        rules = []
        for pair in re.findall(r"(\d+)-(\d+)", raw_rules):
            low, high = map(int, pair)
            rule = range(low, high + 1)
            rules.append(rule)

        return cls(name, tuple(rules))


def iter_invalid_fields(ticket: tuple[int, ...], fields: frozenset[Field]):
    for val in ticket:
        if any(val in field for field in fields):
            continue
        yield val


def build_fields_index(
    fields: frozenset[Field], tickets: frozenset[tuple[int, ...]]
) -> dict[int, Field]:
    fields_count = len(fields)
    fields_index = {idx: None for idx in range(fields_count)}
    while None in fields_index.values():
        for idx in range(fields_count):
            if fields_index[idx] is not None:
                continue
            vals = {ticket[idx] for ticket in tickets}
            todo_fields = fields - set(fields_index.values())

            valid_fields = set()
            for todo_field in todo_fields:
                if all(val in todo_field for val in vals):
                    valid_fields.add(todo_field)
            if len(valid_fields) == 1:
                fields_index[idx] = valid_fields.pop()

    return fields_index


def parse_puzzle(
    puzzle_file,
) -> tuple[frozenset[Field], tuple[int, ...], frozenset[tuple[int, ...]]]:
    inp = puzzle_file.read_text().strip()
    raw_fields, raw_my_ticket, raw_nearby_tickets = inp.split("\n" * 2)

    fields = frozenset(map(Field.from_str, raw_fields.splitlines()))

    my_ticket = tuple(map(int, raw_my_ticket.splitlines()[1].split(",")))

    nearby_tickets = frozenset(
        tuple(map(int, raw_nearby_ticket.split(",")))
        for raw_nearby_ticket in raw_nearby_tickets.splitlines()[1:]
    )
    return fields, my_ticket, nearby_tickets


def p1(puzzle_file):
    fields, _, nearby_tickets = parse_puzzle(puzzle_file)
    return sum(
        val
        for nearby_ticket in nearby_tickets
        for val in iter_invalid_fields(nearby_ticket, fields)
    )


def p2(puzzle_file):
    fields, my_ticket, nearby_tickets = parse_puzzle(puzzle_file)
    valid_tickets = frozenset(
        ticket
        for ticket in nearby_tickets
        if next(iter_invalid_fields(ticket, fields), None) is None
    )
    fields_index = build_fields_index(fields, valid_tickets | {my_ticket})
    return math.prod(
        my_ticket[idx]
        for idx, field in fields_index.items()
        if field.name.startswith("departure")
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
