import copy
import dataclasses
import itertools
import pathlib
import re


type Groups = list["Group"]


@dataclasses.dataclass(kw_only=True, slots=True)
class Group:
    team: str
    units: int
    hp: int
    ap: int
    attack_type: str
    weak: frozenset[str]
    immune: frozenset[str]
    initiative: int
    boost: int = 0

    def attacked_by(self, other):
        lost_units = other.dealt_damage(self) // self.hp
        self.units -= lost_units

    def dealt_damage(self, other) -> int:
        if self.attack_type in other.immune:
            return 0
        damage_mul = 1 + int(self.attack_type in other.weak)
        return self.effective_power * damage_mul

    @property
    def effective_power(self) -> int:
        return self.units * (self.ap + self.boost)

    @property
    def is_alive(self) -> bool:
        return self.units > 0

    @classmethod
    def from_str(cls, team: str, raw: str):
        units, hp, weak_immune, ap, attack_type, initiative = re.findall(
            r"(\d+) units each with (\d+) hit points (\(.*\))? ?with an attack that does (\d+) (\w+) damage at initiative (\d+)",
            raw,
        )[0]

        units, hp, ap, initiative = map(int, (units, hp, ap, initiative))
        weak = immune = frozenset()
        for part in weak_immune[1:-1].split("; "):
            if part.startswith("weak to"):
                weak = frozenset(part.removeprefix("weak to ").split(", "))
            else:
                immune = frozenset(part.removeprefix("immune to ").split(", "))

        return cls(
            team=team,
            units=units,
            hp=hp,
            ap=ap,
            attack_type=attack_type,
            weak=weak,
            immune=immune,
            initiative=initiative,
        )


def find_target_selections(groups: Groups) -> list[tuple[Group, Group]]:
    target_selections = []
    targeted = []

    for group in sorted(
        groups, reverse=True, key=lambda grp: (grp.effective_power, grp.initiative)
    ):
        if not group.is_alive:
            continue
        defending_group = max(
            (
                grp
                for grp in groups
                if grp.is_alive and (group.team != grp.team) and (grp not in targeted)
            ),
            default=None,
            key=lambda g: (group.dealt_damage(g), g.effective_power, g.initiative),
        )

        if (defending_group is None) or (not group.dealt_damage(defending_group)):
            continue
        targeted.append(defending_group)
        target_selections.append((group, defending_group))

    return target_selections


def attack(groups: Groups):
    target_selections = find_target_selections(groups)
    for group in sorted(groups, reverse=True, key=lambda grp: grp.initiative):
        if not group.is_alive:
            continue
        attacking, defending = next(
            (
                (attack, defend)
                for attack, defend in target_selections
                if attack.is_alive and (attack.initiative == group.initiative)
            ),
            (None, None),
        )
        if (attacking is None) or (not defending.is_alive):
            continue

        defending.attacked_by(attacking)


def fight(groups: Groups) -> Groups:
    groups = copy.deepcopy(groups)
    while True:
        before_total_units = total_alive_units(groups)
        attack(groups)
        if before_total_units == total_alive_units(groups):
            return groups
        alive_teams = {group.team for group in groups if group.is_alive}
        if len(alive_teams) != 2:
            return groups
        if not find_target_selections(groups):
            return groups


def total_alive_units(groups: Groups) -> int:
    return sum(group.units for group in groups if group.is_alive)


def parse_puzzle(puzzle_file) -> Groups:
    inp = puzzle_file.read_text().strip()
    immune_system, infection = inp.split("\n" * 2)
    return [
        Group.from_str(team, line)
        for team, chunk in (("immune_system", immune_system), ("infection", infection))
        for line in chunk.splitlines()[1:]
    ]


def p1(puzzle_file):
    return total_alive_units(fight(parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    groups = parse_puzzle(puzzle_file)
    for boost in itertools.count(1):
        boosted = copy.deepcopy(groups)
        for group in boosted:
            if group.team == "infection":
                continue
            group.boost = boost
        survived = fight(boosted)
        if any(group.team == "infection" for group in survived if group.is_alive):
            continue
        return total_alive_units(survived)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
