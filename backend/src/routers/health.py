"""
Health check endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/live", response_model=HealthResponse)
def liveness():
    """Liveness probe - is the service running?"""
    return {
        "status": "alive",
        "service": "ai-service"
    }


@router.get("/ready", response_model=HealthResponse)
def readiness():
    """Readiness probe - is the service ready to handle requests?"""
    # Add checks for dependencies here (database, external APIs, etc.)
    return {
        "status": "ready",
        "service": "ai-service"
    }
