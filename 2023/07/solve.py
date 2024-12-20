import collections
import functools
import pathlib

BASE_REPLACE = {
    "A": "Z",
    "K": "Y",
    "T": "B",
}


def cmp(v1, v2):
    if v1 > v2:
        return 1
    elif v1 < v2:
        return -1
    else:
        return 0

def cmp_hands(hand1, hand2, cmp_func):
    h1, h2 = hand1[0], hand2[0]
    cmp_h1, cmp_h2 = cmp_func(h1), cmp_func(h2)
    cmp_res = cmp(cmp_h1, cmp_h2)
    if cmp_res != 0:
        return cmp_res
    return cmp(h1, h2)

def p1_eval(hand: str):
    return tuple(sorted(collections.Counter(hand).values(), reverse=True))

def p2_eval(hand: str):
    if (jokers_count := hand.count("!")) == 5:
        return (5, )
    new_hand = hand.replace("!", "")
    hand_counter = sorted(collections.Counter(new_hand).values(), reverse=True)
    hand_counter[0] += jokers_count
    return tuple(hand_counter)

def solve(txt: str, cmp_func: callable):
    hands = [line.split() for line in txt.splitlines()]

    key = functools.partial(cmp_hands, cmp_func=cmp_func)
    hands_s = sorted(hands, key=functools.cmp_to_key(key))

    return sum(
        int(bid) * rank for rank, (_, bid) in enumerate(hands_s, start=1)
    )

def p1(puzzle_file):
    inp = puzzle_file.read_text().strip()
    txt = inp
    for frm, to in BASE_REPLACE.items():
        txt = txt.replace(frm, to)
    return solve(txt, p1_eval)

def p2(puzzle_file):
    replace = BASE_REPLACE | {"J": "!"}

    inp = puzzle_file.read_text().strip()
    txt = inp
    for frm, to in replace.items():
        txt = txt.replace(frm, to)
    
    return solve(txt, p2_eval)

puzzle_file = pathlib.Path(__file__).parent / "input.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_input.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
