import sys
from heapq import heappush, heappop

energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
room_position = [2, 4, 6, 8]
forbidden_pos = set(room_position)
type = "ABCD"

def parse_input(lines: list[str]):
    hallway = tuple(lines[1][1:-1])
    depth = len(lines) - 3
    rooms = [[] for _ in range(4)]
    for level in range(2, 2 + depth):
        line = lines[level]
        rooms[0].append(line[3])
        rooms[1].append(line[5])
        rooms[2].append(line[7])
        rooms[3].append(line[9])
    rooms = tuple(tuple(r) for r in rooms)
    return hallway, rooms

def is_goal(rooms):
    for i, room in enumerate(rooms):
        if any(c != type[i] for c in room):
            return False
    return True

def possible_moves(state):
    hallway, rooms = state
    moves = []
    depth = len(rooms[0])
    for pos, ch in enumerate(hallway):
        if ch == '.':
            continue
        target = type.index(ch)
        room = rooms[target]
        if any(c != '.' and c != ch for c in room):
            continue
        start, end = pos, room_position[target]
        step = 1 if end > start else -1
        if any(hallway[p] != '.' for p in range(start + step, end + step, step)):
            continue
        for d in range(depth - 1, -1, -1):
            if room[d] == '.':
                dist = abs(start - end) + d + 1
                cost = energy[ch] * dist
                new_hall = list(hallway)
                new_hall[pos] = '.'
                new_room = [list(r) for r in rooms]
                new_room[target][d] = ch
                moves.append(((tuple(new_hall), tuple(tuple(x) for x in new_room)), cost))
                break

    for r, room in enumerate(rooms):
        for d, ch in enumerate(room):
            if ch != '.':
                break
        else:
            continue
        if all(c == type[r] for c in room[d:]) and type.index(ch) == r:
            continue
        start = room_position[r]

        for p in range(start - 1, -1, -1):
            if hallway[p] != '.':
                break
            if p in forbidden_pos:
                continue
            dist = abs(start - p) + d + 1
            cost = energy[ch] * dist
            new_hall = list(hallway)
            new_hall[p] = ch
            new_room = [list(r) for r in rooms]
            new_room[r][d] = '.'
            moves.append(((tuple(new_hall), tuple(tuple(x) for x in new_room)), cost))

        for p in range(start + 1, len(hallway)):
            if hallway[p] != '.':
                break
            if p in forbidden_pos:
                continue
            dist = abs(start - p) + d + 1
            cost = energy[ch] * dist
            new_hall = list(hallway)
            new_hall[p] = ch
            new_room = [list(r) for r in rooms]
            new_room[r][d] = '.'
            moves.append(((tuple(new_hall), tuple(tuple(x) for x in new_room)), cost))

    return moves

def dijkstra(start):
    best = {start: 0}
    heap = [(0, start)]

    while heap:
        cost, state = heappop(heap)
        if cost != best[state]:
            continue
        hall, rms = state
        if is_goal(rms):
            return cost
        for next_state, step_cost in possible_moves(state):
            new_cost = cost + step_cost
            if new_cost < best.get(next_state, 10**12):
                best[next_state] = new_cost
                heappush(heap, (new_cost, next_state))
    return 0

def solve(lines: list[str]) -> int:
    hallway, rooms = parse_input(lines)
    start = (hallway, rooms)
    return dijkstra(start)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
