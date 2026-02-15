from fastapi import APIRouter, HTTPException

from schemas import AlgorithmRequest
from algorithms import ALGORITHMS

router = APIRouter(prefix="/api/algorithms", tags=["algorithms"])


@router.post("/run")
def run_algorithm(req: AlgorithmRequest):
    if req.algorithm not in ALGORITHMS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown algorithm: {req.algorithm}. Available: {list(ALGORITHMS.keys())}",
        )

    node_ids = {n.id for n in req.graph_data.nodes}
    if req.start_node not in node_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Start node '{req.start_node}' not found in graph",
        )
    if req.end_node and req.end_node not in node_ids:
        raise HTTPException(
            status_code=400,
            detail=f"End node '{req.end_node}' not found in graph",
        )

    algo_fn = ALGORITHMS[req.algorithm]
    result = algo_fn(
        graph_data=req.graph_data,
        start_node=req.start_node,
        end_node=req.end_node,
        directed=req.directed,
    )
    return result


@router.get("/list")
def list_algorithms():
    return {
        "algorithms": [
            {
                "id": "bfs",
                "name": "Breadth-First Search",
                "description": "Explores all neighbors at the current depth before moving deeper. Finds shortest path in unweighted graphs.",
                "category": "traversal",
                "supports_weights": False,
                "supports_directed": True,
            },
            {
                "id": "dfs",
                "name": "Depth-First Search",
                "description": "Explores as far as possible along each branch before backtracking. Useful for topological sorting and cycle detection.",
                "category": "traversal",
                "supports_weights": False,
                "supports_directed": True,
            },
            {
                "id": "dijkstra",
                "name": "Dijkstra's Algorithm",
                "description": "Finds the shortest path from a source to all other nodes. Works with non-negative edge weights.",
                "category": "shortest_path",
                "supports_weights": True,
                "supports_directed": True,
            },
            {
                "id": "bellman_ford",
                "name": "Bellman-Ford Algorithm",
                "description": "Finds shortest paths from a source node, handling negative edge weights. Can detect negative cycles.",
                "category": "shortest_path",
                "supports_weights": True,
                "supports_directed": True,
            },
        ]
    }
