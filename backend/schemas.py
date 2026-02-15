from pydantic import BaseModel
from datetime import datetime


class NodeData(BaseModel):
    id: str
    label: str | None = None
    x: float | None = None
    y: float | None = None


class EdgeData(BaseModel):
    id: str
    source: str
    target: str
    weight: float = 1.0
    directed: bool = False


class GraphData(BaseModel):
    nodes: list[NodeData]
    edges: list[EdgeData]


class GraphCreate(BaseModel):
    name: str = "Untitled Graph"
    description: str | None = None
    graph_data: GraphData


class GraphUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    graph_data: GraphData | None = None


class GraphResponse(BaseModel):
    id: str
    name: str
    description: str | None
    graph_data: GraphData
    share_token: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlgorithmRequest(BaseModel):
    graph_data: GraphData
    algorithm: str  # bfs, dfs, dijkstra, bellman_ford
    start_node: str
    end_node: str | None = None
    directed: bool = False


class AlgorithmStep(BaseModel):
    step: int
    description: str
    visited_nodes: list[str]
    visited_edges: list[str]  # edge ids
    current_node: str | None = None
    highlight_nodes: list[str] = []
    highlight_edges: list[str] = []
    distances: dict[str, float | str] | None = None  # for shortest path algos
    predecessors: dict[str, str | None] | None = None
    queue_or_stack: list[str] | None = None
    path: list[str] | None = None  # final path for shortest path algos


class AlgorithmResponse(BaseModel):
    algorithm: str
    steps: list[AlgorithmStep]
    result: dict
