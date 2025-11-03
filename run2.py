import sys
from collections import defaultdict, deque


def build_graph(edges):
    graph = defaultdict(set)
    gates = set()
    node = set()
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        if a.isupper():
            gates.add(a)
            node.add(b)
        elif b.isupper():
            gates.add(b)
            node.add(a)
        else:
            node.add(a)
            node.add(b)
    return graph, gates, node


def bfs_distance(graph, start):
    distance = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                q.append(v)
    return distance


def nearest_gate(graph, start, gates):
    dist = bfs_distance(graph, start)
    candidates = [(dist[g], g) for g in gates if g in dist]
    if not candidates:
        return None, None
    min_distance = min(d for d, _ in candidates)
    min_gate = min(g for d, g in candidates if d == min_distance)

    parent = {start: None}
    q = deque([start])
    found = False
    while q and not found:
        u = q.popleft()
        for v in sorted(graph[u]):
            if v not in parent:
                parent[v] = u
                q.append(v)
                if v == min_gate:
                    found = True
                    break
    path = []
    curr = min_gate
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return min_gate, path


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph, gates, node = build_graph(edges)
    virus = 'a'
    result = []

    while True:
        min_gate, path = nearest_gate(graph, virus, gates)
        if not min_gate or len(path) < 2:
            break

        near = path[-2]
        cut = f"{min_gate}-{near}"
        result.append(cut)
        graph[min_gate].remove(near)
        graph[near].remove(min_gate)

        if not graph[min_gate]:
            gates.remove(min_gate)

        if len(path) > 2:
            virus = path[1]
        else:
            break

    remaining = []
    for g in sorted(gates):
        for n in sorted(graph[g]):
            remaining.append(f"{g}-{n}")
    result.extend(remaining)
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