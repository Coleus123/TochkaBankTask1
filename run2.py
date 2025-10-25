import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    graph = defaultdict(set)
    for node1, node2 in edges:
        graph[node1].add(node2)
        graph[node2].add(node1)

    gateways = sorted([i for i in graph if i.isupper()])
    virus = 'a'
    result = []
    def bfs(start):
        distance = {start: 0}
        parent = {}
        letter = deque([start])
        while letter:
            node = letter.popleft()
            for neighbour in sorted(graph[node]):
                if neighbour not in distance:
                    distance[neighbour] = distance[node] + 1
                    parent[neighbour] = node
                    letter.append(neighbour)
        return distance, parent
    while True:
        distance, parent = bfs(virus)
        reachable = [(gateway, distance[gateway])
                     for gateway in gateways
                     if gateway in distance]
        if not reachable:
            break
        reachable.sort(key=lambda x: (x[1], x[0]))
        gateway, _ = reachable[0]
        result.append('-'.join((gateway, parent[gateway])))
        graph[gateway].remove(parent[gateway])
        graph[parent[gateway]].remove(gateway)
        distance, parent = bfs(virus)
        reachable = [(gateway, distance[gateway])
                     for gateway in gateways
                     if gateway in distance]
        if not reachable:
            break
        reachable.sort(key=lambda x: (x[1], x[0]))
        gateway, _ = reachable[0]
        path = [gateway]
        current = gateway
        while current != virus:
            current = parent[current]
            path.append(current)
        path.reverse()
        virus = path[1]
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