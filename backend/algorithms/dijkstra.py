import heapq

from schemas import GraphData, AlgorithmStep

INF = float("inf")


def _build_adjacency(graph_data: GraphData, directed: bool):
    adj: dict[str, list[tuple[str, float, str]]] = {n.id: [] for n in graph_data.nodes}
    for e in graph_data.edges:
        adj[e.source].append((e.target, e.weight, e.id))
        if not directed:
            adj[e.target].append((e.source, e.weight, e.id))
    return adj


def run_dijkstra(
    graph_data: GraphData,
    start_node: str,
    end_node: str | None = None,
    directed: bool = False,
) -> dict:
    adj = _build_adjacency(graph_data, directed)
    node_ids = [n.id for n in graph_data.nodes]

    distances: dict[str, float] = {n: INF for n in node_ids}
    distances[start_node] = 0
    predecessors: dict[str, str | None] = {n: None for n in node_ids}
    edge_to: dict[str, str | None] = {n: None for n in node_ids}
    visited_nodes: list[str] = []
    visited_edges: list[str] = []
    steps: list[AlgorithmStep] = []
    step_num = 0

    def dist_display():
        return {k: (v if v != INF else "∞") for k, v in distances.items()}

    steps.append(
        AlgorithmStep(
            step=step_num,
            description=f"Initialize Dijkstra from node {start_node}. Set distance to {start_node} = 0, all others = ∞",
            visited_nodes=[],
            visited_edges=[],
            current_node=start_node,
            highlight_nodes=[start_node],
            distances=dist_display(),
        )
    )

    # Priority queue: (distance, node)
    pq: list[tuple[float, str]] = [(0, start_node)]

    while pq:
        dist, node = heapq.heappop(pq)

        if node in visited_nodes:
            continue

        visited_nodes.append(node)
        if edge_to[node]:
            visited_edges.append(edge_to[node])

        step_num += 1
        steps.append(
            AlgorithmStep(
                step=step_num,
                description=f"Extract node {node} with distance {dist}",
                visited_nodes=list(visited_nodes),
                visited_edges=list(visited_edges),
                current_node=node,
                highlight_nodes=[node],
                distances=dist_display(),
                predecessors={k: v for k, v in predecessors.items() if v is not None},
            )
        )

        if end_node and node == end_node:
            path = _reconstruct_path(predecessors, end_node)
            path_edges = _reconstruct_path_edges(edge_to, predecessors, end_node)
            step_num += 1
            steps.append(
                AlgorithmStep(
                    step=step_num,
                    description=f"Reached target {end_node}! Shortest distance = {distances[end_node]}. Path: {' → '.join(path)}",
                    visited_nodes=list(visited_nodes),
                    visited_edges=list(visited_edges),
                    current_node=end_node,
                    highlight_nodes=path,
                    highlight_edges=path_edges,
                    distances=dist_display(),
                    path=path,
                )
            )
            return {
                "algorithm": "dijkstra",
                "steps": [s.model_dump() for s in steps],
                "result": {
                    "path": path,
                    "distance": distances[end_node],
                    "found": True,
                },
            }

        for neighbor, weight, edge_id in adj.get(node, []):
            if neighbor in visited_nodes:
                continue
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                old_dist = distances[neighbor]
                distances[neighbor] = new_dist
                predecessors[neighbor] = node
                edge_to[neighbor] = edge_id
                heapq.heappush(pq, (new_dist, neighbor))
                step_num += 1
                old_str = old_dist if old_dist != INF else "∞"
                steps.append(
                    AlgorithmStep(
                        step=step_num,
                        description=f"Relax edge {node} → {neighbor}: {old_str} → {new_dist} (via weight {weight})",
                        visited_nodes=list(visited_nodes),
                        visited_edges=list(visited_edges),
                        current_node=node,
                        highlight_nodes=[neighbor],
                        highlight_edges=[edge_id],
                        distances=dist_display(),
                        predecessors={
                            k: v for k, v in predecessors.items() if v is not None
                        },
                    )
                )

    result: dict = {
        "distances": {k: v for k, v in distances.items() if v != INF},
        "visited_count": len(visited_nodes),
        "found": False,
    }
    if end_node and distances.get(end_node, INF) != INF:
        path = _reconstruct_path(predecessors, end_node)
        result["path"] = path
        result["distance"] = distances[end_node]
        result["found"] = True

    return {
        "algorithm": "dijkstra",
        "steps": [s.model_dump() for s in steps],
        "result": result,
    }


def _reconstruct_path(predecessors: dict, end_node: str) -> list[str]:
    path = []
    current: str | None = end_node
    while current is not None:
        path.append(current)
        current = predecessors.get(current)
    path.reverse()
    return path


def _reconstruct_path_edges(
    edge_to: dict, predecessors: dict, end_node: str
) -> list[str]:
    edges = []
    current: str | None = end_node
    while current is not None and edge_to.get(current) is not None:
        edges.append(edge_to[current])
        current = predecessors.get(current)
    edges.reverse()
    return edges
