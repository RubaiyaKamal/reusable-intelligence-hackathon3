"""
Query processing endpoints
"""

from fastapi import APIRouter, HTTPException
from src.models.requests import QueryRequest
from src.models.responses import QueryResponse
from src.services.agent_service import AgentService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
agent_service = AgentService()


@router.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    """Process a user query"""
    try:
        logger.info(f"Processing query from student {request.student_id}")

        response = agent_service.process_query(
            query=request.query,
            student_id=request.student_id,
            context=request.context or {}
        )

        return QueryResponse(
            response=response,
            agent_type="triage",
            student_id=request.student_id
        )

    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
