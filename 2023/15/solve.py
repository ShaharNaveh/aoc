import collections
import functools
import pathlib

def hash_str(s: str) -> int:
    return functools.reduce(
        lambda cur, nxt: ((cur + nxt) * 17 ) & 0xFF, map(ord, s), 0
    )

def find_index_in_boxes(label: str, boxes: list[tuple[str, int]]) -> int | None:
    for idx, box in enumerate(boxes):
        if label == box[0]:
            return idx
    return None

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.split(",")

def p1(puzzle_file):
    return sum(map(hash_str, iter_puzzle(puzzle_file)))

def p2(puzzle_file):
    hashmap = collections.defaultdict(list)

    for step in iter_puzzle(puzzle_file):
        if step.endswith("-"):
            label = step[:-1]

            box = hash_str(label)
            box_idx = find_index_in_boxes(label, hashmap[box])
            if box_idx is not None:
                hashmap[box].pop(box_idx)
            continue

        op_idx = step.index("=")
        label, num = step[:op_idx], int(step[op_idx + 1:])

        box = hash_str(label)
        box_idx = find_index_in_boxes(label, hashmap[box])

        if box_idx is not None:
            hashmap[box][box_idx] = (label, num)
        else:
            hashmap[box].append((label, num))


    return sum(
        (box_num + 1) * slot_num * focal_len
        for box_num, boxes in hashmap.items()
        for slot_num, (_, focal_len) in enumerate(boxes, start=1)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
