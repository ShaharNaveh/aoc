import collections
import pathlib


def mix(lst: list[int], multiplier: int = 1, times: int = 1) -> int:
    items = list(enumerate(map(lambda n: n * multiplier, lst)))
    items_len = len(items)
    deque = collections.deque(items)
    zero_item = None

    for _ in range(times):
        for item in items:
            num = item[1]
            if (zero_item is None) and (num == 0):
                zero_item = item

            deque.rotate(-deque.index(item))
            deque.popleft()

            rotate = num % (items_len - 1)
            deque.rotate(-rotate)
            deque.appendleft(item)

    deque.rotate(-deque.index(zero_item))
    return sum(deque[i * 1000 % items_len][1] for i in range(1, 4))


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return mix(list(iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return mix(list(iter_puzzle(puzzle_file)), 811_589_153, 10)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
