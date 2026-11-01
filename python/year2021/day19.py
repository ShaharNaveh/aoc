import collections
import itertools
import operator
import re
import typing
import unittest

from utils import Day, aoc_main


class Vec3(typing.NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self: "Vec3", other: "Vec3") -> "Vec3":
        return type(self)(*itertools.starmap(operator.sub, zip(self, other)))

    def manhattan(self: "Vec3", other: "Vec3") -> int:
        return sum(abs(dist) for dist in self - other)

    @classmethod
    def from_str(cls, raw: str):
        return cls(*map(int, raw.split(",")))


def find_common(s0, s1) -> tuple[tuple[Vec3, ...], Vec3] | None:
    coord = []
    aligned = []
    found = set()
    for s0_dim in range(3):
        s0_vals = [beacon[s0_dim] for beacon in s0]
        for signed_int, s1_dim in itertools.product((1, -1), range(3)):
            if s1_dim in found:
                continue
            s1_vals = [beacon[s1_dim] * signed_int for beacon in s1]
            diffs = [
                s0_val - s1_val
                for s0_val, s1_val in itertools.product(s0_vals, s1_vals)
            ]
            diff, overlap_count = collections.Counter(diffs).most_common(1)[0]
            if overlap_count >= 12:
                break
        else:
            return None
        found.add(s1_dim)
        aligned.append([s1_val + diff for s1_val in s1_vals])
        coord.append(diff)
    return tuple(Vec3(*pos) for pos in zip(*aligned)), Vec3(*coord)


def solve(scanners):
    scanner0, *unaligned = scanners
    beacons = set()
    aligned = [scanner0]
    scanner_coords = {Vec3(0, 0, 0)}
    while aligned:
        s0 = aligned.pop()
        buf = []
        for s1 in unaligned:
            common = find_common(s0, s1)
            if common is None:
                buf.append(s1)
                continue
            s0_aligned, scanner_coord = common
            aligned.append(s0_aligned)
            scanner_coords.add(scanner_coord)
        unaligned = buf
        beacons.update(s0)
    return beacons, scanner_coords


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from (
        tuple(map(Vec3.from_str, raw_beacons.splitlines()))
        for raw_beacons in re.split(r"\s*--- scanner \d+ ---\s*", inp)
        if raw_beacons
    )


class Day19(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        beacons, _ = solve(parsed)
        return len(beacons)

    def part2(self, parsed):
        _, coords = solve(parsed)
        return max(a.manhattan(b) for a, b in itertools.combinations(coords, 2))


TEST_PUZZLE = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day19()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 79)

    def test_part2_test_puzzle(self):
        d = Day19()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 3621)


if __name__ == "__main__":
    aoc_main(Day19)
