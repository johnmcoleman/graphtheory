from schemas import GraphData, AlgorithmStep


def _build_adjacency(graph_data: GraphData, directed: bool):
    adj: dict[str, list[tuple[str, str]]] = {n.id: [] for n in graph_data.nodes}
    for e in graph_data.edges:
        adj[e.source].append((e.target, e.id))
        if not directed:
            adj[e.target].append((e.source, e.id))
    return adj


def run_dfs(
    graph_data: GraphData,
    start_node: str,
    end_node: str | None = None,
    directed: bool = False,
) -> dict:
    adj = _build_adjacency(graph_data, directed)
    visited_nodes: list[str] = []
    visited_edges: list[str] = []
    predecessors: dict[str, str | None] = {start_node: None}
    edge_to: dict[str, str | None] = {start_node: None}
    stack = [start_node]
    steps: list[AlgorithmStep] = []
    step_num = 0

    steps.append(
        AlgorithmStep(
            step=step_num,
            description=f"Start DFS from node {start_node}",
            visited_nodes=[],
            visited_edges=[],
            current_node=start_node,
            highlight_nodes=[start_node],
            queue_or_stack=[start_node],
        )
    )

    while stack:
        node = stack.pop()
        if node in visited_nodes:
            continue
        visited_nodes.append(node)

        if edge_to.get(node):
            visited_edges.append(edge_to[node])

        step_num += 1
        steps.append(
            AlgorithmStep(
                step=step_num,
                description=f"Visit node {node} (popped from stack)",
                visited_nodes=list(visited_nodes),
                visited_edges=list(visited_edges),
                current_node=node,
                highlight_nodes=[node],
                queue_or_stack=list(stack),
            )
        )

        if end_node and node == end_node:
            path = _reconstruct_path(predecessors, end_node)
            path_edges = _reconstruct_path_edges(edge_to, predecessors, end_node)
            step_num += 1
            steps.append(
                AlgorithmStep(
                    step=step_num,
                    description=f"Found target node {end_node}! Path: {' → '.join(path)}",
                    visited_nodes=list(visited_nodes),
                    visited_edges=list(visited_edges),
                    current_node=end_node,
                    highlight_nodes=path,
                    highlight_edges=path_edges,
                    path=path,
                    queue_or_stack=list(stack),
                )
            )
            return {
                "algorithm": "dfs",
                "steps": [s.model_dump() for s in steps],
                "result": {
                    "path": path,
                    "visited_count": len(visited_nodes),
                    "found": True,
                },
            }

        # Add neighbors in reverse order so first neighbor is processed first
        neighbors = adj.get(node, [])
        for neighbor, edge_id in reversed(neighbors):
            if neighbor not in visited_nodes:
                if neighbor not in predecessors:
                    predecessors[neighbor] = node
                    edge_to[neighbor] = edge_id
                stack.append(neighbor)
                step_num += 1
                steps.append(
                    AlgorithmStep(
                        step=step_num,
                        description=f"Push neighbor {neighbor} onto stack",
                        visited_nodes=list(visited_nodes),
                        visited_edges=list(visited_edges),
                        current_node=node,
                        highlight_nodes=[neighbor],
                        highlight_edges=[edge_id],
                        queue_or_stack=list(stack),
                    )
                )

    result: dict = {"visited_count": len(visited_nodes), "found": False}
    if end_node and end_node in visited_nodes:
        path = _reconstruct_path(predecessors, end_node)
        result["path"] = path
        result["found"] = True

    return {
        "algorithm": "dfs",
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
