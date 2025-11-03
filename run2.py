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
            node.update([a, b])
    return graph, gates, node


def bfs_distance(graph, start, gates):
    distance = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                if v in gates:
                    return True
                q.append(v)
    return False


def nearest_gate(graph, start, gates):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in sorted(graph[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)

    candidates = [(dist[g], g) for g in sorted(gates) if g in dist]
    if not candidates:
        return None, None

    _, min_gate = min(candidates)
    path = bfs_path(graph, start, min_gate)
    return min_gate, path


def bfs_path(graph, start, min_gate):
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        for v in sorted(graph[u]):
            if v not in parent:
                parent[v] = u
                q.append(v)
                if v == min_gate:
                    q.clear()
                    break

    if min_gate not in parent:
        return []

    path = []
    curr = min_gate
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path


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

        dist = bfs_distance(graph, virus, gates)
        if not dist:
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