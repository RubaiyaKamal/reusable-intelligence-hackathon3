"""
Request models
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    query: str
    student_id: str
    context: Optional[Dict[str, Any]] = None
