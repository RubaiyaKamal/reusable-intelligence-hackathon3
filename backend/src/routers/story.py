"""
Story endpoints for story generation and continuation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.agents.story_agent import StoryAgent
from src.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Story Agent
try:
    story_agent = StoryAgent(openai_api_key=settings.OPENAI_API_KEY)
    logger.info("Story Agent initialized successfully")
except TypeError as te:
    if "'proxies'" in str(te):
        logger.error(f"Proxy configuration error in Story Agent: {te}")
        logger.warning("Story Agent disabled due to proxy configuration issue")
        story_agent = None
    else:
        logger.error(f"Failed to initialize Story Agent: {te}")
        story_agent = None
except Exception as e:
    logger.error(f"Failed to initialize Story Agent: {e}")
    story_agent = None


class StoryGenerationRequest(BaseModel):
    """Request model for story generation"""
    story_type: str = Field(default="adventure", description="Type of story to generate")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level (0-100)")
    length: str = Field(default="medium", description="Story length (short/medium/long)")
    theme: Optional[str] = Field(default=None, description="Specific theme or topic")
    characters: Optional[List[str]] = Field(default=None, description="Character names or types")
    moral_lesson: Optional[str] = Field(default=None, description="Lesson to embed in story")
    student_id: str = Field(..., description="Student identifier")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class StoryContinuationRequest(BaseModel):
    """Request model for story continuation"""
    previous_story: str = Field(..., description="The story so far")
    user_input: Optional[str] = Field(default=None, description="Direction for continuation")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level")
    student_id: str = Field(..., description="Student identifier")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class StoryResponse(BaseModel):
    """Response model for story generation"""
    success: bool
    story: Optional[str] = None
    title: Optional[str] = None
    story_type: Optional[str] = None
    reading_level: Optional[str] = None
    length: Optional[str] = None
    vocabulary_words: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    fallback_story: Optional[str] = None


class StoryContinuationResponse(BaseModel):
    """Response model for story continuation"""
    success: bool
    continuation: Optional[str] = None
    full_story: Optional[str] = None
    reading_level: Optional[str] = None
    error: Optional[str] = None


class StoryStatsResponse(BaseModel):
    """Response model for story statistics"""
    total_stories: int
    stories_by_type: Dict[str, int]
    stories_by_level: Dict[str, int]


@router.post("/generate", response_model=StoryResponse)
def generate_story(request: StoryGenerationRequest):
    """
    Generate a new story based on parameters

    This endpoint creates an age-appropriate story with:
    - Adaptive vocabulary based on reading level
    - Engaging plot and characters
    - Optional moral lessons
    - Educational value
    """
    if not story_agent:
        raise HTTPException(
            status_code=503,
            detail="Story Agent is not available"
        )

    try:
        logger.info(
            f"Generating {request.story_type} story for student {request.student_id} "
            f"at reading level {request.reading_level}"
        )

        result = story_agent.generate_story(
            story_type=request.story_type,
            reading_level=request.reading_level,
            length=request.length,
            theme=request.theme,
            characters=request.characters,
            moral_lesson=request.moral_lesson,
            context=request.context
        )

        return StoryResponse(**result)

    except Exception as e:
        logger.error(f"Story generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/continue", response_model=StoryContinuationResponse)
def continue_story(request: StoryContinuationRequest):
    """
    Continue an existing story

    Takes the previous story content and generates a natural continuation,
    optionally incorporating user direction.
    """
    if not story_agent:
        raise HTTPException(
            status_code=503,
            detail="Story Agent is not available"
        )

    try:
        logger.info(f"Continuing story for student {request.student_id}")

        result = story_agent.continue_story(
            previous_story=request.previous_story,
            user_input=request.user_input,
            reading_level=request.reading_level,
            context=request.context
        )

        return StoryContinuationResponse(**result)

    except Exception as e:
        logger.error(f"Story continuation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
def get_story_types():
    """
    Get available story types

    Returns:
        List of available story genres
    """
    if not story_agent:
        raise HTTPException(
            status_code=503,
            detail="Story Agent is not available"
        )

    return {
        "story_types": story_agent.get_available_story_types(),
        "description": "Available story genres for generation"
    }


@router.get("/stats", response_model=StoryStatsResponse)
def get_story_stats():
    """
    Get story generation statistics

    Returns:
    - Total stories generated
    - Distribution by story type
    - Distribution by reading level
    """
    if not story_agent:
        raise HTTPException(
            status_code=503,
            detail="Story Agent is not available"
        )

    try:
        stats = story_agent.get_stats()
        return StoryStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
