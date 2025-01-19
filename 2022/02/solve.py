import enum
import pathlib

@enum.unique
class Hand(enum.IntEnum):
    Rock = enum.auto()
    Paper = enum.auto()
    Scissors = enum.auto()

    @classmethod
    def from_str(cls, char: str):
        return {
            "A": cls.Rock,
            "B": cls.Paper,
            "C": cls.Scissors,
            "X": cls.Rock,
            "Y": cls.Paper,
            "Z": cls.Scissors,
        }[char]

    def __invert__(self):
        return {
            Hand.Rock: Hand.Paper,
            Hand.Paper: Hand.Scissors,
            Hand.Scissors: Hand.Rock
        }[self]

@enum.unique
class MatchOutcome(enum.IntEnum):
    Win = 6
    Draw = 3
    Loss = 0

    @classmethod
    def from_hands(cls, opponent: Hand, player: Hand):
        if player == opponent:
            return cls.Draw

        return cls.Win if opponent == ~player else cls.Loss

    @classmethod
    def from_str(cls, char: str):
        return {
            "X": cls.Loss,
            "Y": cls.Draw,
            "Z": cls.Win,
        }[char]

def simulate(col1: str, col2: str, *, is_p2: bool = False) -> int:
    opponent = Hand.from_str(col1)
    if is_p2:
        match_outcome = MatchOutcome.from_str(col2)
        match match_outcome:
            case MatchOutcome.Draw:
                return match_outcome + opponent
            case MatchOutcome.Loss:
                return match_outcome + ~~opponent
            case MatchOutcome.Win:
                return match_outcome + ~opponent

    player = Hand.from_str(col2)
    return MatchOutcome.from_hands(player, opponent) + player

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(str.split, inp.splitlines())

def p1(puzzle_file):
    return sum(simulate(col1, col2) for col1, col2 in iter_puzzle(puzzle_file))

def p2(puzzle_file):
    return sum(
        simulate(col1, col2, is_p2=True) for col1, col2 in iter_puzzle(puzzle_file)
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
