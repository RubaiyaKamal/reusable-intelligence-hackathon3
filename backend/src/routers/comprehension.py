"""
Comprehension endpoints for story Q&A and understanding assessment
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.agents.comprehension_agent import ComprehensionAgent
from src.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Comprehension Agent
try:
    comprehension_agent = ComprehensionAgent(openai_api_key=settings.OPENAI_API_KEY)
    logger.info("Comprehension Agent initialized successfully")
except TypeError as te:
    if "'proxies'" in str(te):
        logger.error(f"Proxy configuration error in Comprehension Agent: {te}")
        logger.warning("Comprehension Agent disabled due to proxy configuration issue")
        comprehension_agent = None
    else:
        logger.error(f"Failed to initialize Comprehension Agent: {te}")
        comprehension_agent = None
except Exception as e:
    logger.error(f"Failed to initialize Comprehension Agent: {e}")
    comprehension_agent = None


class QuestionRequest(BaseModel):
    """Request model for answering questions"""
    question: str = Field(..., description="Question about the story")
    story_text: str = Field(..., description="The story text")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level (0-100)")
    provide_hints: bool = Field(default=False, description="Include hints")
    student_id: str = Field(..., description="Student identifier")


class SummaryRequest(BaseModel):
    """Request model for story summary"""
    story_text: str = Field(..., description="The story text")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level")
    length: str = Field(default="medium", description="Summary length (short/medium/detailed)")
    focus: Optional[str] = Field(default=None, description="Focus area (characters/plot/theme)")
    student_id: str = Field(..., description="Student identifier")


class QuestionGenerationRequest(BaseModel):
    """Request model for generating questions"""
    story_text: str = Field(..., description="The story text")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level")
    num_questions: int = Field(default=5, ge=1, le=10, description="Number of questions")
    difficulty: str = Field(default="mixed", description="Question difficulty (easy/medium/hard/mixed)")
    student_id: str = Field(..., description="Student identifier")


class QuestionResponse(BaseModel):
    """Response model for question answering"""
    success: bool
    question: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    hints: Optional[List[str]] = None
    question_type: Optional[str] = None
    reading_level: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SummaryResponse(BaseModel):
    """Response model for summary"""
    success: bool
    summary: Optional[str] = None
    key_characters: Optional[List[str]] = None
    main_events: Optional[List[str]] = None
    theme: Optional[str] = None
    reading_level: Optional[str] = None
    length: Optional[str] = None
    error: Optional[str] = None


class QuestionGenerationResponse(BaseModel):
    """Response model for question generation"""
    success: bool
    questions: Optional[List[Dict[str, str]]] = None
    total_questions: Optional[int] = None
    reading_level: Optional[str] = None
    difficulty: Optional[str] = None
    error: Optional[str] = None


class ComprehensionStatsResponse(BaseModel):
    """Response model for comprehension statistics"""
    total_questions: int
    questions_by_type: Dict[str, int]
    summaries_generated: int


@router.post("/answer", response_model=QuestionResponse)
def answer_question(request: QuestionRequest):
    """
    Answer a question about a story

    This endpoint provides:
    - Accurate answers based on story content
    - Explanations for inferential questions
    - Optional hints to guide learning
    - Question type classification
    """
    if not comprehension_agent:
        raise HTTPException(
            status_code=503,
            detail="Comprehension Agent is not available"
        )

    try:
        logger.info(
            f"Answering question for student {request.student_id} "
            f"at reading level {request.reading_level}"
        )

        result = comprehension_agent.answer_question(
            question=request.question,
            story_text=request.story_text,
            reading_level=request.reading_level,
            provide_hints=request.provide_hints
        )

        return QuestionResponse(**result)

    except Exception as e:
        logger.error(f"Question answering failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    """
    Generate a summary of a story

    This endpoint creates:
    - Clear, concise summaries
    - Key character identification
    - Main event highlights
    - Theme extraction
    """
    if not comprehension_agent:
        raise HTTPException(
            status_code=503,
            detail="Comprehension Agent is not available"
        )

    try:
        logger.info(
            f"Generating {request.length} summary for student {request.student_id}"
        )

        result = comprehension_agent.generate_summary(
            story_text=request.story_text,
            reading_level=request.reading_level,
            length=request.length,
            focus=request.focus
        )

        return SummaryResponse(**result)

    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-questions", response_model=QuestionGenerationResponse)
def generate_questions(request: QuestionGenerationRequest):
    """
    Generate comprehension questions for a story

    Creates questions that test:
    - Literal comprehension (who, what, when, where)
    - Inferential understanding (why, how)
    - Evaluative thinking (opinions, judgments)
    """
    if not comprehension_agent:
        raise HTTPException(
            status_code=503,
            detail="Comprehension Agent is not available"
        )

    try:
        logger.info(
            f"Generating {request.num_questions} questions for student {request.student_id}"
        )

        result = comprehension_agent.generate_questions(
            story_text=request.story_text,
            reading_level=request.reading_level,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )

        return QuestionGenerationResponse(**result)

    except Exception as e:
        logger.error(f"Question generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=ComprehensionStatsResponse)
def get_comprehension_stats():
    """
    Get comprehension agent statistics

    Returns:
    - Total questions answered
    - Distribution by question type
    - Number of summaries generated
    """
    if not comprehension_agent:
        raise HTTPException(
            status_code=503,
            detail="Comprehension Agent is not available"
        )

    try:
        stats = comprehension_agent.get_stats()
        return ComprehensionStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
