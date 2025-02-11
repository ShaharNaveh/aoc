import functools
import pathlib


@functools.cache
def find_neighs(pos: complex) -> tuple[complex, ...]:
    return tuple(
        pos + offset for offset in (-1 - 1j, -1j, 1 - 1j, -1, 0, 1, -1 + 1j, 1j, 1 + 1j)
    )


def is_npos_light(
    neighs: tuple[complex, ...],
    image: dict[complex, bool],
    algo: frozenset[int],
    fallback: bool,
) -> bool:
    return (
        int("".join("1" if image.get(pos, fallback) else "0" for pos in neighs), 2)
        in algo
    )


def enhance(algo: frozenset[int], image: dict[complex, bool], times: int = 2) -> int:
    fallback = False
    swap = 0 in algo
    for _ in range(times):
        nimage = {}
        for pixel in image:
            for neigh in find_neighs(pixel):
                if neigh in nimage:
                    continue
                nimage[neigh] = is_npos_light(find_neighs(neigh), image, algo, fallback)
        image = nimage
        if swap:
            fallback = not fallback

    lights = {k for k, v in image.items() if v}
    return len(lights)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_algo, raw_image = inp.split("\n" * 2)

    algo = frozenset(idx for idx, char in enumerate(raw_algo) if char == "#")
    image = {
        complex(x, y): char == "#"
        for y, row in enumerate(raw_image.splitlines())
        for x, char in enumerate(row)
    }
    return algo, image


def p1(puzzle_file):
    return enhance(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return enhance(*parse_puzzle(puzzle_file), 50)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
