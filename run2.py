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

def nearest_gate(graph, gates, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in sorted(graph[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    candidates = [(dist[g], g) for g in gates if g in dist]
    if not candidates:
        return None, None

    min_dist = min(d for d, _ in candidates)
    min_gate = min(g for d, g in candidates if d == min_dist)
    path = bfs_path(graph, start, min_gate)
    return min_gate, path


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
        for node in sorted(graph.keys()):
            gate_links = [g for g in graph[node] if g.isupper()]
            if len(gate_links) > 1:
                keep = min(gate_links)
                for g in gate_links:
                    if g != keep:
                        result.append(f"{g}-{node}")
                        graph[g].discard(node)
                        graph[node].discard(g)
                        if not graph[g]:
                            gates.discard(g)

        for g in sorted(graph[virus]):
            if g.isupper():
                result.append(f"{g}-{virus}")
                graph[g].discard(virus)
                graph[virus].discard(g)
                if not graph[g]:
                    gates.discard(g)

        min_gate, path = nearest_gate(graph, gates, virus)
        if not min_gate or len(path) < 2:
            reachable = set([virus])
            q = deque([virus])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in reachable:
                        reachable.add(v)
                        q.append(v)

            for node in sorted(reachable):
                for g in sorted(graph[node]):
                    if g.isupper() and f"{g}-{node}" not in result:
                        result.append(f"{g}-{node}")
            break

        near = path[-2]
        result.append(f"{min_gate}-{near}")
        graph[min_gate].discard(near)
        graph[near].discard(min_gate)
        if not graph[min_gate]:
            gates.discard(min_gate)

        virus = path[1] if len(path) > 2 else virus

    result = sorted(result)
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
