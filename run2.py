import sys
from collections import defaultdict, deque


def bfs_distance(graph, start):
    distance = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in sorted(graph[u]):
            if v not in distance:
                distance[v] = distance[u] + 1
                q.append(v)
    return distance


def nearest_gate(graph, gates, start):
    dist = bfs_distance(graph, start)
    candidates = [(dist[g], g) for g in gates if g in dist]
    if not candidates:
        return None
    min_dist = min(d for d, _ in candidates)
    min_gate = min(g for d, g in candidates if d == min_dist)
    return min_gate

def next_step_towards(graph, start, target):
    distance = bfs_distance(graph, target)
    neighbors = [v for v in graph[start] if v in distance and not v.isupper()]
    if not neighbors:
        return start
    min_dist = min(distance[v] for v in neighbors)
    candidates = [v for v in neighbors if distance[v] == min_dist]
    return min(candidates)

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    gates = set()
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        if a.isupper():
            gates.add(a)
        if b.isupper():
            gates.add(b)

    virus = 'a'
    result = []

    while gates:
        gate = nearest_gate(graph, gates, virus)
        if not gate:
            break

        candidates = [v for v in graph[gate] if not v.isupper()]
        if not candidates:
            gates.discard(gate)
            continue
        node_to_cut = min(candidates)
        result.append(f"{gate}-{node_to_cut}")
        graph[gate].discard(node_to_cut)
        graph[node_to_cut].discard(gate)
        if not graph[gate]:
            gates.discard(gate)

        if virus in graph and any(v not in gates for v in graph[virus]):
            virus = next_step_towards(graph, virus, gate)

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()