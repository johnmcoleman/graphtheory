import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Graph
from schemas import GraphCreate, GraphUpdate, GraphResponse, GraphData

router = APIRouter(prefix="/api/graphs", tags=["graphs"])


def _graph_to_response(graph: Graph) -> GraphResponse:
    return GraphResponse(
        id=graph.id,
        name=graph.name,
        description=graph.description,
        graph_data=GraphData.model_validate(json.loads(graph.graph_data)),
        share_token=graph.share_token,
        created_at=graph.created_at,
        updated_at=graph.updated_at,
    )


@router.post("/", response_model=GraphResponse)
def create_graph(graph_in: GraphCreate, db: Session = Depends(get_db)):
    graph = Graph(
        name=graph_in.name,
        description=graph_in.description,
        graph_data=graph_in.graph_data.model_dump_json(),
    )
    db.add(graph)
    db.commit()
    db.refresh(graph)
    return _graph_to_response(graph)


@router.get("/", response_model=list[GraphResponse])
def list_graphs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    graphs = db.query(Graph).offset(skip).limit(limit).all()
    return [_graph_to_response(g) for g in graphs]


@router.get("/{graph_id}", response_model=GraphResponse)
def get_graph(graph_id: str, db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return _graph_to_response(graph)


@router.put("/{graph_id}", response_model=GraphResponse)
def update_graph(
    graph_id: str, graph_in: GraphUpdate, db: Session = Depends(get_db)
):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    if graph_in.name is not None:
        graph.name = graph_in.name
    if graph_in.description is not None:
        graph.description = graph_in.description
    if graph_in.graph_data is not None:
        graph.graph_data = graph_in.graph_data.model_dump_json()
    db.commit()
    db.refresh(graph)
    return _graph_to_response(graph)


@router.delete("/{graph_id}")
def delete_graph(graph_id: str, db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    db.delete(graph)
    db.commit()
    return {"detail": "Graph deleted"}


@router.get("/share/{share_token}", response_model=GraphResponse)
def get_graph_by_share_token(share_token: str, db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.share_token == share_token).first()
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return _graph_to_response(graph)
