import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime

from database import Base


def generate_share_token():
    return uuid.uuid4().hex[:10]


class Graph(Base):
    __tablename__ = "graphs"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String, nullable=False, default="Untitled Graph")
    description = Column(String, nullable=True)
    graph_data = Column(Text, nullable=False)  # JSON: {nodes: [...], edges: [...]}
    share_token = Column(String, unique=True, default=generate_share_token, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
