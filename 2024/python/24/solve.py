from operator import (
    and_ as AND,
    or_ as OR,
    xor as XOR,
)
import pathlib

OPS = {"AND": AND, "OR": OR, "XOR": XOR}


def is_op_in_ladder(w: str, gate: callable, gates: dict):
    return any((gate == op) and (w in (a, b)) for op, a, b in gates.values())


def resolve_gate(gate: str, wires: dict, gates: dict):
    if (res := wires.get(gate)) is not None:
        return res
    op, a, b = gates[gate]
    return op(
        resolve_gate(a, wires=wires, gates=gates),
        resolve_gate(b, wires=wires, gates=gates),
    )


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    wires_block, gates_block = inp.split("\n" * 2)
    wires = {
        wire: int(val)
        for wire, val in map(lambda line: line.split(": "), wires_block.splitlines())
    }

    gates = {
        dest: (OPS[op], a, b)
        for a, op, b, _, dest in map(str.split, gates_block.splitlines())
    }

    return wires, gates


def p1(puzzle_file):
    wires, gates = parse_puzzle(puzzle_file)
    zgates = set(filter(lambda k: k.startswith("z"), gates))
    res = "".join(
        str(resolve_gate(zgate, wires, gates)) for zgate in sorted(zgates, reverse=True)
    )
    return int(res, 2)


def p2(puzzle_file):
    _, gates = parse_puzzle(puzzle_file)
    zgates = set(filter(lambda k: k.startswith("z"), gates))
    last_zgate = f"z{len(zgates) - 1}"

    res = set()
    for dest, (op, a, b) in gates.items():
        if (
            ((op != XOR) and dest.startswith("z") and dest != last_zgate)
            or (
                (op == XOR)
                and ("x00" not in (a, b))
                and is_op_in_ladder(dest, OR, gates)
            )
            or (
                (op == AND)
                and ("x00" not in (a, b))
                and is_op_in_ladder(dest, XOR, gates)
            )
            or (
                (op == XOR)
                and all(not w.startswith(("x", "y", "z")) for w in (a, b, dest))
            )
        ):
            res.add(dest)
    return ",".join(sorted(res))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
