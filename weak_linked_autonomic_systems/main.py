from collections import defaultdict, deque


def load_graph(filename):
    graph = defaultdict(set)
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            u, v = int(parts[0]), int(parts[1])
            graph[u].add(v)
            graph[v].add(u)
    return graph


def bfs_alternative_path(graph, a, b, max_depth=6):
    """Ищет путь a->...->b, не используя прямое ребро a-b на первом шаге."""
    visited = {a}
    queue = deque()
    for nb in graph[a]:
        if nb != b:
            visited.add(nb)
            queue.append((nb, [a, nb]))
    while queue:
        node, path = queue.popleft()
        if node == b:
            return path
        if len(path) - 1 > max_depth:
            continue
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return None


def find_weakly_linked(graph, min_degree=10):
    candidates = sorted(
        [v for v in graph if len(graph[v]) >= min_degree], key=lambda v: -len(graph[v])
    )
    for a in candidates:
        for b in graph[a]:
            if len(graph[b]) < min_degree:
                continue
            alt = bfs_alternative_path(graph, a, b)
            if alt:
                return a, b, alt
    return None


def main():
    filename = "./data/as20000102.txt"
    graph = load_graph(filename)

    print(f"Файл: {filename}")
    print(f"Вершин: {len(graph)}")
    print(f"Рёбер: {sum(len(s) for s in graph.values()) // 2}")

    result = find_weakly_linked(graph, min_degree=10)
    if result:
        a, b, path = result
        print(f"\nНайдена слабо связанная пара вершин:")
        print(f"  A = {a}, степень = {len(graph[a])}")
        print(f"  B = {b}, степень = {len(graph[b])}")
        print(f"  Прямое ребро: {a} -- {b}")
        print(f"  Альтернативный путь (длина {len(path) - 1}):")
        print(f"    {' -> '.join(map(str, path))}")
        print(f"\nОбе степени >= 10: {len(graph[a])} >= 10, {len(graph[b])} >= 10 ✓")
    else:
        print("Пара не найдена")


if __name__ == "__main__":
    main()
