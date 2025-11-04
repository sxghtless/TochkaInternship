import sys
from collections import defaultdict, deque


def build_graph(edges):
    graph = defaultdict(set)
    gates = set()
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        if a.isupper():
            gates.add(a)
        if b.isupper():
            gates.add(b)
    return graph, gates


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


def nearest_gate(graph, start, gates):
    dist = bfs_distance(graph, start)
    candidates = [(dist[g], g) for g in gates if g in dist]
    if not candidates:
        return None, None

    _, target_gate = min(candidates)

    next_node = None
    min_next_dist = float('inf')

    for neighbor in sorted(graph[start]):
        if neighbor in dist:
            neighbor_dist = bfs_distance(graph, neighbor).get(target_gate, float('inf'))
            if neighbor_dist < min_next_dist:
                min_next_dist = neighbor_dist
                next_node = neighbor

    return target_gate, next_node


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph, gates = build_graph(edges)
    virus = 'a'
    result = []

    while gates:
        dist = bfs_distance(graph, virus)
        reachable_gates = [g for g in gates if g in dist]

        if not reachable_gates:
            break

        adjacent_gates = [neighbor for neighbor in graph[virus] if neighbor in gates]

        if adjacent_gates:
            gate_to_cut = sorted(adjacent_gates)[0]
            result.append(f"{gate_to_cut}-{virus}")
            graph[gate_to_cut].discard(virus)
            graph[virus].discard(gate_to_cut)

            if not any(n for n in graph[gate_to_cut] if not n.isupper()):
                gates.remove(gate_to_cut)

            continue

        target_gate, next_node = nearest_gate(graph, virus, gates)

        if not target_gate:
            break

        gate_neighbors = sorted([n for n in graph[target_gate] if not n.isupper()])

        if gate_neighbors:
            result.append(f"{target_gate}-{gate_neighbors[0]}")
            graph[target_gate].discard(gate_neighbors[0])
            graph[gate_neighbors[0]].discard(target_gate)

            if not any(n for n in graph[target_gate] if not n.isupper()):
                gates.remove(target_gate)

        if next_node:
            virus = next_node

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