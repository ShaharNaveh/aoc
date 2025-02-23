import pathlib


def play_combat(deck1: list[int], deck2: list[int]) -> tuple[list[int], list[int]]:
    while deck1 and deck2:
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if card1 > card2:
            deck1.extend([card1, card2])
        else:
            deck2.extend([card2, card1])
    return deck1, deck2


def play_recursive_combat(
    deck1: list[int], deck2: list[int]
) -> tuple[list[int], list[int]]:
    seen = set()
    while deck1 and deck2:
        if (key := tuple(deck1)) in seen:
            return deck1, []
        seen.add(key)

        card1, card2 = deck1.pop(0), deck2.pop(0)
        if (card1 <= len(deck1)) and (card2 <= len(deck2)):
            if play_recursive_combat(deck1[:card1].copy(), deck2[:card2].copy())[0]:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        else:
            if card1 > card2:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])

    return deck1, deck2


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from (
        list(map(int, raw_player.splitlines()[1:]))
        for raw_player in inp.split("\n" * 2)
    )


def find_deck_score(decks) -> int:
    return sum(
        card * idx for deck in decks for idx, card in enumerate(reversed(deck), 1)
    )


def p1(puzzle_file):
    return find_deck_score(play_combat(*iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return find_deck_score(play_recursive_combat(*iter_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
