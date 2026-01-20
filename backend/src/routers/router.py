"""
Router endpoints for agent routing and statistics
"""

from fastapi import APIRouter, HTTPException
from src.models.requests import QueryRequest
from src.models.responses import RoutingResponse, AgentStatsResponse
from src.services.agent_service import AgentService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
agent_service = AgentService()


@router.post("/route", response_model=RoutingResponse)
def route_query(request: QueryRequest):
    """
    Route a query to the appropriate specialist agent

    This endpoint analyzes the user's query and determines:
    - Which specialist agent should handle it
    - The user's engagement level
    - Routing confidence score
    """
    try:
        logger.info(f"Routing query from user {request.student_id}")

        routing_decision = agent_service.route_query(
            query=request.query,
            user_id=request.student_id,
            context=request.context
        )

        if "error" in routing_decision:
            raise HTTPException(status_code=500, detail=routing_decision["error"])

        return RoutingResponse(**routing_decision)

    except Exception as e:
        logger.error(f"Routing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=AgentStatsResponse)
def get_router_stats():
    """
    Get routing statistics

    Returns:
    - Total number of queries routed
    - Distribution of queries across agents
    - Most frequently used agent
    """
    try:
        stats = agent_service.get_router_stats()

        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])

        return AgentStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
