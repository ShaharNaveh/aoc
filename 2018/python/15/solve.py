import copy
import dataclasses
import heapq
import itertools
import operator
import pathlib


type Units = tuple["Unit", ...]
type Walkable = frozenset["Pos"]


class Pos(complex):
    def __lt__(self, other) -> bool:
        return (self.imag, self.real) < (other.imag, other.real)

    def __add__(self, other):
        return Pos(super().__add__(other))

    __radd__ = __add__


@dataclasses.dataclass(slots=True)
class Unit:
    team: str
    pos: Pos
    hp: int = 200
    ap: int = 3

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0

    def __lt__(self, other) -> bool:
        return (self.hp, self.pos) < (other.hp, other.pos)


def iter_neighbors(pos: Pos):
    yield from (pos + offset for offset in (-1j, -1, 1, 1j))


def parse_puzzle(puzzle_file) -> tuple[Units, Walkable]:
    inp = puzzle_file.read_text().strip()

    units, walkable = [], set()
    for y, row in enumerate(inp.splitlines()):
        for x, tile in enumerate(row.strip()):
            if tile == "#":
                continue
            pos = Pos(x, y)
            walkable.add(pos)
            if tile != ".":
                units.append(Unit(tile, pos))

    return tuple(units), frozenset(walkable)


def find_shortest_paths(
    start: Pos, destenations: set[Pos], walkable: Walkable
) -> tuple[tuple[Pos, ...], ...]:
    paths = ()
    best = float("inf")
    pq = [(0, (start,))]
    visited = set()
    while pq:
        steps, path = heapq.heappop(pq)
        if (path_len := len(path)) > best:
            return paths

        pos = path[-1]
        if pos in destenations:
            paths += (path,)
            best = path_len
            continue

        if pos in visited:
            continue
        visited.add(pos)

        for npos in iter_neighbors(pos):
            if npos not in walkable:
                continue
            heapq.heappush(pq, (steps + 1, path + (npos,)))
    return paths


def find_target(pos: Pos, targets: set[Pos], walkable: Walkable) -> Pos | None:
    if not targets:
        return None

    if pos in targets:
        return pos

    paths = find_shortest_paths(pos, targets, walkable)
    return min(map(operator.itemgetter(-1), paths), default=None)


def find_move(pos: Pos, target: Pos, walkable: Walkable) -> Pos | None:
    if pos == target:
        return pos
    paths = find_shortest_paths(pos, {target}, walkable)
    return min(map(operator.itemgetter(1), paths), default=None)


def find_npos(unit: Unit, units: Units, walkable: Walkable) -> Pos | None:
    targets = {
        target.pos
        for target in units
        if (target.team != unit.team) and (not target.is_dead)
    }
    if not targets:
        return None
    walkable -= {x.pos for x in units if (x != unit) and (not x.is_dead)}
    in_range = walkable & {
        neighbor for pos in targets for neighbor in iter_neighbors(pos)
    }
    target = find_target(unit.pos, in_range, walkable)
    if target is None:
        return unit.pos
    return find_move(unit.pos, target, walkable)


def find_attack_target(unit: Unit, units: Units) -> Unit | None:
    neighbors = set(iter_neighbors(unit.pos))
    return min(
        (
            enemy
            for enemy in units
            if (enemy.team != unit.team)
            and (not enemy.is_dead)
            and (enemy.pos in neighbors)
        ),
        default=None,
    )


def do_round(units: Units, walkable: Walkable) -> tuple[Units, bool]:
    for unit in sorted(units, key=operator.attrgetter("pos")):
        if unit.is_dead:
            continue
        npos = find_npos(unit, units, walkable)
        if npos is None:
            return units, False
        unit.pos = npos
        target = find_attack_target(unit, units)
        if not target:
            continue
        target.hp -= unit.ap

    return units, True


def simulate(units: Units, walkable: Walkable) -> tuple[int, Units]:
    rounds = 0

    while True:
        units, is_full_round = do_round(units, walkable)
        if not is_full_round:
            break
        rounds += 1

    total_hp = sum(unit.hp for unit in units if not unit.is_dead)
    outcome = rounds * total_hp
    return outcome, units


def p1(puzzle_file):
    return simulate(*parse_puzzle(puzzle_file))[0]


def p2(puzzle_file):
    ounits, walkable = parse_puzzle(puzzle_file)
    elf_count = sum(unit.team == "E" for unit in ounits)
    for elf_ap in itertools.count(4):
        units = tuple(
            dataclasses.replace(unit, ap=elf_ap) if unit.team == "E" else unit
            for unit in copy.deepcopy(ounits)
        )
        outcome, won_units = simulate(units, walkable)
        if sum(unit.team == "E" for unit in won_units if not unit.is_dead) == elf_count:
            return outcome


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
