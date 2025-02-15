import collections
import pathlib


def walk(caves, *, is_p2: bool = False) -> int:
    paths = set()
    todo = [("start", [])]
    while todo:
        cur, path = todo.pop()
        npath = path + [cur]

        if cur == "end":
            paths.add(tuple(npath))
            continue

        for con in caves[cur]:
            if con == "start":
                continue

            if con[0].islower() and (con in npath):
                small_caves = [cave for cave in npath if cave[0].islower()]
                if is_p2 and max(collections.Counter(small_caves).values()) >= 2:
                    continue
                elif not is_p2:
                    continue
            todo.append((con, npath.copy()))

    return len(paths)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    caves = collections.defaultdict(set)
    for line in inp.splitlines():
        l, r = line.split("-")
        caves[l].add(r)
        caves[r].add(l)
    return dict(caves)


def p1(puzzle_file):
    return walk(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return walk(parse_puzzle(puzzle_file), is_p2=True)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
