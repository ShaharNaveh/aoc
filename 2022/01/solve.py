import pathlib

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    buf = []
    for line in inp.splitlines():
        if line == "":
            yield buf
            buf.clear()
        else:
            buf.append(int(line))
    yield buf



def p1(puzzle_file):
    return max(map(sum, iter_puzzle(puzzle_file)))

def p2(puzzle_file):
    return sum(
        sorted(
            map(
                sum, iter_puzzle(puzzle_file)
            ),
            reverse=True)[:3]
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
