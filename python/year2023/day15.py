import collections
import functools

from utils import Day, run


def hash_str(s: str) -> int:
    return functools.reduce(lambda cur, nxt: ((cur + nxt) * 17) & 0xFF, map(ord, s), 0)


def find_index_in_boxes(label: str, boxes: list[tuple[str, int]]) -> int | None:
    for idx, box in enumerate(boxes):
        if label == box[0]:
            return idx
    return None


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.split(",")


class Day15(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(map(hash_str, parsed))

    def part2(self, parsed):
        hashmap = collections.defaultdict(list)

        for step in parsed:
            if step.endswith("-"):
                label = step[:-1]

                box = hash_str(label)
                box_idx = find_index_in_boxes(label, hashmap[box])
                if box_idx is not None:
                    hashmap[box].pop(box_idx)
                continue

            op_idx = step.index("=")
            label, num = step[:op_idx], int(step[op_idx + 1 :])

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


if __name__ == "__main__":
    run(Day15)
