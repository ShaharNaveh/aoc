import heapq
import pathlib
import typing


CHARS = "ABCD"
ROOMS = {char: i * 2 for i, char in enumerate(CHARS, 1)}
COSTS = {char: 10**i for i, char in enumerate(CHARS)}


class Branch(typing.NamedTuple):
    cost: int = 0
    rooms: tuple[tuple[str | None, ...], ...] = ()
    hallway: tuple[str | None, ...] = (None,) * 11

    def __lt__(self, other: "Branch") -> bool:
        return self.cost < other.cost


def organize(start: tuple[tuple[str | None, ...], ...]) -> int:
    room_size = len(start[0])
    end = tuple((char,) * room_size for char in CHARS)

    pq = [Branch(rooms=start)]
    seen = set()
    while pq:
        cost, rooms, hallway = heapq.heappop(pq)
        if rooms == end:
            return cost

        if (rooms, hallway) in seen:
            continue
        seen.add((rooms, hallway))

        # Room -> Hallway
        for room_idx, room in enumerate(rooms):
            if room == end[room_idx]:
                continue

            top_idx, top_amphipod = next(
                ((i, amphipod) for i, amphipod in enumerate(room) if amphipod),
                (None, None),
            )
            if None in (top_idx, top_amphipod):
                continue

            for hallway_idx in (0, *range(1, 10, 2), 10):
                slc = slice(
                    min(room_idx * 2 + 2, hallway_idx),
                    max(room_idx * 2 + 2, hallway_idx) + 1,
                )

                if any(slot is not None for slot in hallway[slc]):
                    continue

                ncost = cost + COSTS[top_amphipod] * (
                    top_idx + abs(room_idx * 2 + 2 - hallway_idx) + 1
                )
                nrooms = tuple(
                    tuple(
                        None
                        if ((nroom_idx == room_idx) and (nroom_slot_idx == top_idx))
                        else top_namphipod
                        for nroom_slot_idx, top_namphipod in enumerate(nroom)
                    )
                    for nroom_idx, nroom in enumerate(rooms)
                )
                nhallway = tuple(
                    top_amphipod if nhallway_idx == hallway_idx else hallway_amphipod
                    for nhallway_idx, hallway_amphipod in enumerate(hallway)
                )
                heapq.heappush(pq, Branch(cost=ncost, rooms=nrooms, hallway=nhallway))

        # Hallway -> Room
        for hallway_idx in (0, *range(1, 10, 2), 10):
            if (amphipod := hallway[hallway_idx]) is None:
                continue

            if hallway_idx > ROOMS[amphipod]:
                path = hallway[ROOMS[amphipod] : hallway_idx]
            else:
                path = hallway[hallway_idx + 1 : ROOMS[amphipod] + 1]

            if any(x is not None for x in path):
                continue

            room_idx = ord(amphipod) - ord(CHARS[0])
            room = rooms[room_idx]

            if any(roomate not in (None, amphipod) for roomate in room):
                continue

            bottom_room_idx = 0
            while (bottom_room_idx < len(room)) and (room[bottom_room_idx] is None):
                bottom_room_idx += 1
            bottom_room_idx -= 1

            if room[bottom_room_idx] is not None:
                continue

            ncost = cost + COSTS[amphipod] * (
                bottom_room_idx + abs(ROOMS[amphipod] - hallway_idx) + 1
            )
            nrooms = tuple(
                tuple(
                    amphipod
                    if ((nroom_idx == room_idx) and (nroom_slot_idx == bottom_room_idx))
                    else top_amphipod
                    for nroom_slot_idx, top_amphipod in enumerate(nroom)
                )
                for nroom_idx, nroom in enumerate(rooms)
            )
            nhallway = tuple(
                None if nhallway_idx == hallway_idx else hallway_amphipod
                for nhallway_idx, hallway_amphipod in enumerate(hallway)
            )
            heapq.heappush(pq, Branch(cost=ncost, rooms=nrooms, hallway=nhallway))


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(
        room
        for room in tuple(
            tuple(char for char in col if char in CHARS)
            for col in zip(*inp.splitlines())
        )
        if room
    )


def p1(puzzle_file):
    return organize(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
