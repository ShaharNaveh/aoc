import collections
import functools
import itertools
import math
import operator
import pathlib


def move(pos: complex, v: complex, bounds: complex):
    npos = pos + v
    return complex(npos.real % bounds.real, npos.imag % bounds.imag)


def simulate(robots, seconds: int, bounds: complex):
    lst = robots.copy()
    for _ in range(seconds):
        for idx, robot in enumerate(lst):
            lst[idx] = robot | {"pos": move(**robot, bounds=bounds)}
    return lst


def parse_puzzle(path):
    inp = path.read_text().strip()
    for line in inp.splitlines():
        pos_block, v_block = line.split()

        entry = {"pos": pos_block, "v": v_block}
        for key, block in entry.items():
            entry[key] = complex(*map(int, block.split("=")[-1].split(",")))
        yield entry


def calc_safety(robots, bounds):
    x_mid = bounds.real // 2
    y_mid = bounds.imag // 2
    quadrants = collections.defaultdict(int)
    for pos in map(operator.itemgetter("pos"), robots):
        x, y = pos.real, pos.imag
        if (x == x_mid) or (y == y_mid):
            continue

        if (x < x_mid) and (y < y_mid):
            key = 0
        elif (x > x_mid) and (y < y_mid):
            key = 1
        elif (x < x_mid) and (y > y_mid):
            key = 2
        else:
            key = 3
        quadrants[key] += 1

    return functools.reduce(operator.mul, quadrants.values())


def calc_entropy(positions):
    counter = collections.Counter(positions)
    total = sum(counter.values())
    entropy = -sum(
        (count / total) * math.log2(count / total) for count in counter.values()
    )
    return entropy


def p1(path, bounds):
    robots = list(parse_puzzle(path))
    simulated = simulate(robots, seconds=100, bounds=bounds)
    res = calc_safety(simulated, bounds=bounds)
    return res


def p2(path, bounds):
    robots = list(parse_puzzle(path))

    lst = [list(map(operator.itemgetter("pos"), robots))]
    for _ in range(1, 100_000):
        robots = simulate(robots, seconds=1, bounds=bounds)
        lst.append(list(map(operator.itemgetter("pos"), robots)))

    return max(
        ((calc_entropy(positions), idx) for idx, positions in enumerate(lst)),
        key=operator.itemgetter(0),
    )[1]


puzzle_file = (pathlib.Path(__file__).parent / "puzzle.txt", 101 + 103j)
# puzzle_file = (pathlib.Path(__file__).parent / "test_puzzle.txt", 11 + 7j)

print(p1(*puzzle_file))
print(p2(*puzzle_file))
