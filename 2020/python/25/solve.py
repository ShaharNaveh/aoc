import pathlib


def iter_loop_sizes():
    val = 1
    while True:
        val = (val * 7) % 20201227
        yield val


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(map(int, inp.splitlines()))


def p1(puzzle_file):
    pub_keys = parse_puzzle(puzzle_file)
    loop_size, device_pubkey = next(
        (loop_size, pub_key)
        for loop_size, pub_key in enumerate(iter_loop_sizes(), 1)
        if pub_key in pub_keys
    )

    subject = next(pub_key for pub_key in pub_keys if pub_key != device_pubkey)

    key = 1
    for _ in range(loop_size):
        key = (key * subject) % 20201227

    return key


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
