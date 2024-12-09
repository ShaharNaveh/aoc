import itertools
import pathlib

def defrag(lst):
    _lst = lst.copy()
    while "." in _lst:
        if (char := _lst.pop()) == ".":
            continue
        index = _lst.index(".")
        _lst[index] = char
    return _lst

def defrag_p2(lst):
    _lst = lst.copy()
    file_idx_stop = len(_lst) -1
    while file_idx_stop >= 0:
        file_id = _lst[file_idx_stop]
        if file_id == ".":
            file_idx_stop -= 1
            continue
        file_slc = slice(file_idx_stop, file_idx_stop + 1)
        while True:
            new_file_slc = slice(file_slc.start - 1, file_slc.stop)
            if len(set(_lst[new_file_slc])) != 1:
                break
            file_slc = new_file_slc
        window_len = file_slc.stop - file_slc.start
        search_area = _lst[:file_slc.start]
        for offset in range(len(search_area) - window_len + 1):
            free_slc = slice(offset, offset + window_len)
            if search_area[free_slc].count(".") == window_len:
                break
        else:
            free_slc = None

        if free_slc:
            _lst[file_slc], _lst[free_slc] = _lst[free_slc], _lst[file_slc]

        file_idx_stop -= window_len
    return _lst

def parse_puzzle(puzzle):
    parsed = []
    for file_id, file_meta in enumerate(itertools.batched(puzzle, 2)):
        if len(file_meta) == 2:
            file_block, free_block = file_meta
        else:
            file_block, free_block = file_meta[0], 0

        parsed += [file_id] * file_block
        parsed += ["."] * free_block
    return parsed

def load_puzzle(path):
    inp = path.read_text().strip()
    return list(map(int, list(inp)))

def p1(path):
    puzzle = load_puzzle(path)
    parsed = parse_puzzle(puzzle)
    lst = defrag(parsed)
    checksum = sum(pos * file_id for pos, file_id in enumerate(lst))
    print(checksum)

def p2(path):
    puzzle = load_puzzle(path)
    parsed = parse_puzzle(puzzle)
    lst = defrag_p2(parsed)
    checksum = sum(pos * file_id for pos, file_id in enumerate(lst) if file_id != ".")
    print(checksum)

puzzle_file = pathlib.Path(__file__).parent / "input.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(puzzle_file)
p2(puzzle_file)
