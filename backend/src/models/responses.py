"""
Response models
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class QueryResponse(BaseModel):
    response: str
    agent_type: str
    student_id: str


class RoutingResponse(BaseModel):
    """Response from router agent with routing decision"""
    agent: str
    agent_port: int
    engagement: str
    confidence: float
    query: str
    user_id: str
    metadata: Dict[str, Any]


class AgentStatsResponse(BaseModel):
    """Router statistics response"""
    total_queries: int
    distribution: Dict[str, float]
    most_used_agent: Optional[str] = None
