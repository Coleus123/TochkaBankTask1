import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for node1, node2 in edges:
        graph[node1].add(node2)
        graph[node2].add(node1)
    gateways = sorted([node for node in graph if node.isupper()])
    virus_pos = 'a'
    result = []
    def find_virus_move():
        """Находит следующий ход вируса"""
        distances = {}
        queue = deque([(virus_pos, 0)])
        visited = {virus_pos}
        while queue:
            node, dist = queue.popleft()
            distances[node] = dist
            for neighbor in sorted(graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        closest_gateways = []
        min_dist = float('inf')
        for gateway in gateways:
            if gateway in distances:
                if distances[gateway] < min_dist:
                    min_dist = distances[gateway]
                    closest_gateways = [gateway]
                elif distances[gateway] == min_dist:
                    closest_gateways.append(gateway)
        if not closest_gateways:
            return None
        target_gateway = sorted(closest_gateways)[0]
        parent = {}
        queue = deque([target_gateway])
        visited = {target_gateway}
        while queue:
            node = queue.popleft()
            if node == virus_pos:
                break
            for neighbor in sorted(graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)
        path = []
        current = virus_pos
        while current != target_gateway:
            path.append(current)
            current = parent[current]
        path.append(target_gateway)
        return path[1] if len(path) > 1 else path[0]

    def get_available_gate_edges():
        """Возвращает все доступные для отключения коридоры со шлюзами"""
        gate_edges = []
        for gateway in gateways:
            for neighbor in sorted(graph[gateway]):
                gate_edges.append(f"{gateway}-{neighbor}")
        return sorted(gate_edges)
    while True:
        immediate_threat = None
        for gateway in sorted(gateways):
            if gateway in graph[virus_pos]:
                immediate_threat = f"{gateway}-{virus_pos}"
                break
        if immediate_threat:
            result.append(immediate_threat)
            gateway, node = immediate_threat.split('-')
            graph[gateway].remove(node)
            graph[node].remove(gateway)
            continue
        next_virus_move = find_virus_move()
        if next_virus_move is None:
            break
        available_edges = get_available_gate_edges()
        if not available_edges:
            break
        edge_to_cut = available_edges[0]
        result.append(edge_to_cut)
        gateway, node = edge_to_cut.split('-')
        graph[gateway].remove(node)
        graph[node].remove(gateway)
        virus_pos = next_virus_move
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