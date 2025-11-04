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


def bfs_path(graph, start, target):
    parent = {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == target:
            break
        for v in sorted(graph[u]):
            if v not in parent:
                parent[v] = u
                q.append(v)

    if target not in parent:
        return []

    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path


def nearest_gate(graph, start, gates):
    dist = bfs_distance(graph, start)
    candidates = [(dist[g], g) for g in sorted(gates) if g in dist]
    if not candidates:
        return None, None

    min_dist = min(d for d, _ in candidates)
    target_gate = min(g for d, g in candidates if d == min_dist)

    return target_gate, bfs_path(graph, start, target_gate)


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph, gates = build_graph(edges)
    virus = 'a'
    result = []

    while gates:
        target_gate, path = nearest_gate(graph, virus, gates)
        if not target_gate or len(path) < 2:
            break

        node_before_gate = path[-2]

        result.append(f"{target_gate}-{node_before_gate}")
        graph[target_gate].discard(node_before_gate)
        graph[node_before_gate].discard(target_gate)

        if not graph[target_gate]:
            gates.remove(target_gate)

        dist_after = bfs_distance(graph, virus)
        candidates_after = [(dist_after[g], g) for g in sorted(gates) if g in dist_after]
        if not candidates_after:
            break

        min_d_after = min(d for d, _ in candidates_after)
        min_gate_after = min(g for d, g in candidates_after if d == min_d_after)
        path_after = bfs_path(graph, virus, min_gate_after)

        if len(path_after) > 1:
            virus = path_after[1]
        else:
            break

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
