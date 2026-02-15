from schemas import GraphData, AlgorithmStep

INF = float("inf")


def run_bellman_ford(
    graph_data: GraphData,
    start_node: str,
    end_node: str | None = None,
    directed: bool = False,
) -> dict:
    node_ids = [n.id for n in graph_data.nodes]
    n = len(node_ids)

    # Build edge list
    edges: list[tuple[str, str, float, str]] = []
    for e in graph_data.edges:
        edges.append((e.source, e.target, e.weight, e.id))
        if not directed:
            edges.append((e.target, e.source, e.weight, e.id))

    distances: dict[str, float] = {nid: INF for nid in node_ids}
    distances[start_node] = 0
    predecessors: dict[str, str | None] = {nid: None for nid in node_ids}
    edge_to: dict[str, str | None] = {nid: None for nid in node_ids}

    steps: list[AlgorithmStep] = []
    visited_edges: list[str] = []
    step_num = 0

    def dist_display():
        return {k: (v if v != INF else "∞") for k, v in distances.items()}

    steps.append(
        AlgorithmStep(
            step=step_num,
            description=f"Initialize Bellman-Ford from node {start_node}. Set distance to {start_node} = 0, all others = ∞. Will perform {n - 1} relaxation rounds.",
            visited_nodes=[start_node],
            visited_edges=[],
            current_node=start_node,
            highlight_nodes=[start_node],
            distances=dist_display(),
        )
    )

    has_negative_cycle = False

    for i in range(1, n):
        relaxed_any = False
        step_num += 1
        steps.append(
            AlgorithmStep(
                step=step_num,
                description=f"--- Round {i} of {n - 1} ---",
                visited_nodes=[nid for nid in node_ids if distances[nid] != INF],
                visited_edges=list(visited_edges),
                current_node=None,
                distances=dist_display(),
                predecessors={
                    k: v for k, v in predecessors.items() if v is not None
                },
            )
        )

        for u, v, w, eid in edges:
            if distances[u] == INF:
                continue
            new_dist = distances[u] + w
            if new_dist < distances[v]:
                old_dist = distances[v]
                distances[v] = new_dist
                predecessors[v] = u
                edge_to[v] = eid
                if eid not in visited_edges:
                    visited_edges.append(eid)
                relaxed_any = True
                step_num += 1
                old_str = old_dist if old_dist != INF else "∞"
                steps.append(
                    AlgorithmStep(
                        step=step_num,
                        description=f"Relax edge {u} → {v}: {old_str} → {new_dist} (weight {w})",
                        visited_nodes=[
                            nid for nid in node_ids if distances[nid] != INF
                        ],
                        visited_edges=list(visited_edges),
                        current_node=u,
                        highlight_nodes=[v],
                        highlight_edges=[eid],
                        distances=dist_display(),
                        predecessors={
                            k: v_
                            for k, v_ in predecessors.items()
                            if v_ is not None
                        },
                    )
                )

        if not relaxed_any:
            step_num += 1
            steps.append(
                AlgorithmStep(
                    step=step_num,
                    description=f"No relaxations in round {i} — algorithm converged early!",
                    visited_nodes=[
                        nid for nid in node_ids if distances[nid] != INF
                    ],
                    visited_edges=list(visited_edges),
                    current_node=None,
                    distances=dist_display(),
                )
            )
            break

    # Check for negative cycles
    for u, v, w, eid in edges:
        if distances[u] != INF and distances[u] + w < distances[v]:
            has_negative_cycle = True
            step_num += 1
            steps.append(
                AlgorithmStep(
                    step=step_num,
                    description=f"⚠ Negative cycle detected! Edge {u} → {v} can still be relaxed.",
                    visited_nodes=[nid for nid in node_ids if distances[nid] != INF],
                    visited_edges=list(visited_edges),
                    current_node=u,
                    highlight_nodes=[u, v],
                    highlight_edges=[eid],
                    distances=dist_display(),
                )
            )
            break

    result: dict = {
        "distances": {k: v for k, v in distances.items() if v != INF},
        "visited_count": len([nid for nid in node_ids if distances[nid] != INF]),
        "negative_cycle": has_negative_cycle,
        "found": False,
    }

    if end_node and distances.get(end_node, INF) != INF and not has_negative_cycle:
        path = _reconstruct_path(predecessors, end_node)
        path_edges = _reconstruct_path_edges(edge_to, predecessors, end_node)
        result["path"] = path
        result["distance"] = distances[end_node]
        result["found"] = True
        step_num += 1
        steps.append(
            AlgorithmStep(
                step=step_num,
                description=f"Shortest path to {end_node}: {' → '.join(path)} (distance = {distances[end_node]})",
                visited_nodes=[nid for nid in node_ids if distances[nid] != INF],
                visited_edges=list(visited_edges),
                current_node=end_node,
                highlight_nodes=path,
                highlight_edges=path_edges,
                distances=dist_display(),
                path=path,
            )
        )

    return {
        "algorithm": "bellman_ford",
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
