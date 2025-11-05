from collections import deque, defaultdict
import sys


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    def bfs(start_node, adjacency):
        distance = {start_node: 0}
        queue = deque([start_node])
        while queue:
            current_node = queue.popleft()
            for neighbor in adjacency.get(current_node, ()):
                if neighbor not in distance:
                    distance[neighbor] = distance[current_node] + 1
                    queue.append(neighbor)
        return distance

    def find_closest_gateway(virus_node, adjacency):
        distance = bfs(virus_node, adjacency)
        best_gateway = None
        best_distance = None
        for node, dist in distance.items():
            if node.isupper():
                if best_gateway is None or dist < best_distance or (dist == best_distance and node < best_gateway):
                    best_gateway = node
                    best_distance = dist
        return best_gateway, best_distance

    def next_step_to_gateway(virus_node, adjacency):
        gateway, _ = find_closest_gateway(virus_node, adjacency)
        if gateway is None:
            return None
        distance_from_gateway = bfs(gateway, adjacency)
        if virus_node not in distance_from_gateway:
            return None
        current_distance = distance_from_gateway[virus_node]
        if current_distance <= 1:
            return gateway
        neighbors = sorted(adjacency.get(virus_node, []))
        for neighbor in neighbors:
            if distance_from_gateway.get(neighbor, 10 ** 9) == current_distance - 1:
                return neighbor
        return None
    edge_set = frozenset(tuple(sorted(edge)) for edge in edges)
    virus_start = 'a'
    visited_states = {}
    def search(edges, virus_node):
        state_key = (edges, virus_node)
        if state_key in visited_states:
            return visited_states[state_key]
        adjacency = defaultdict(set)
        for n1, n2 in edges:
            adjacency[n1].add(n2)
            adjacency[n2].add(n1)
        gateway, _ = find_closest_gateway(virus_node, adjacency)
        if gateway is None:
            visited_states[state_key] = []
            return []
        possible_cuts = []
        for n1, n2 in sorted(edges):
            if n1.isupper() and n2.islower():
                possible_cuts.append((n1, n2))
            elif n2.isupper() and n1.islower():
                possible_cuts.append((n2, n1))
        for gateway_node, connected_node in possible_cuts:
            cut_edge = tuple(sorted((gateway_node, connected_node)))
            new_edges = set(edges)
            new_edges.remove(cut_edge)
            new_edges_frozen = frozenset(new_edges)
            new_adjacency = defaultdict(set)
            for x, y in new_edges:
                new_adjacency[x].add(y)
                new_adjacency[y].add(x)
            new_gateway, _ = find_closest_gateway(virus_node, new_adjacency)
            if new_gateway is None:
                visited_states[state_key] = [f"{gateway_node}-{connected_node}"]
                return visited_states[state_key]
            virus_next = next_step_to_gateway(virus_node, new_adjacency)
            if virus_next is None:
                visited_states[state_key] = [f"{gateway_node}-{connected_node}"]
                return visited_states[state_key]
            if virus_next.isupper():
                continue
            result_rest = search(new_edges_frozen, virus_next)
            if result_rest is not None:
                visited_states[state_key] = [f"{gateway_node}-{connected_node}"] + result_rest
                return visited_states[state_key]
        visited_states[state_key] = None
        return None
    result = search(edge_set, virus_start)
    return result if result is not None else []


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1.strip(), node2.strip()))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()