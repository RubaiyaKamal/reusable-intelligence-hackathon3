"""
Vocabulary endpoints for word definitions and vocabulary building
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.agents.vocabulary_agent import VocabularyAgent
from src.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Vocabulary Agent
try:
    vocabulary_agent = VocabularyAgent(openai_api_key=settings.OPENAI_API_KEY)
    logger.info("Vocabulary Agent initialized successfully")
except TypeError as te:
    if "'proxies'" in str(te):
        logger.error(f"Proxy configuration error in Vocabulary Agent: {te}")
        logger.warning("Vocabulary Agent disabled due to proxy configuration issue")
        vocabulary_agent = None
    else:
        logger.error(f"Failed to initialize Vocabulary Agent: {te}")
        vocabulary_agent = None
except Exception as e:
    logger.error(f"Failed to initialize Vocabulary Agent: {e}")
    vocabulary_agent = None


class WordExplanationRequest(BaseModel):
    """Request model for word explanation"""
    word: str = Field(..., description="Word to explain")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level (0-100)")
    context: Optional[str] = Field(default=None, description="Context where word appears")
    style: str = Field(default="detailed", description="Explanation style (simple/detailed/contextual/visual)")
    include_examples: bool = Field(default=True, description="Include usage examples")
    student_id: str = Field(..., description="Student identifier")


class PhraseExplanationRequest(BaseModel):
    """Request model for phrase explanation"""
    phrase: str = Field(..., description="Phrase or idiom to explain")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level")
    context: Optional[str] = Field(default=None, description="Context where phrase appears")
    student_id: str = Field(..., description="Student identifier")


class VocabularyListRequest(BaseModel):
    """Request model for vocabulary list building"""
    story_text: str = Field(..., description="Story text to extract vocabulary from")
    reading_level: int = Field(default=50, ge=0, le=100, description="Reading level")
    max_words: int = Field(default=10, ge=1, le=20, description="Maximum words to extract")
    student_id: str = Field(..., description="Student identifier")


class WordExplanationResponse(BaseModel):
    """Response model for word explanation"""
    success: bool
    word: Optional[str] = None
    definition: Optional[str] = None
    simple_explanation: Optional[str] = None
    examples: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    antonyms: Optional[List[str]] = None
    related_words: Optional[List[str]] = None
    reading_level: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    fallback_definition: Optional[str] = None


class PhraseExplanationResponse(BaseModel):
    """Response model for phrase explanation"""
    success: bool
    phrase: Optional[str] = None
    explanation: Optional[str] = None
    reading_level: Optional[str] = None
    error: Optional[str] = None


class VocabularyListResponse(BaseModel):
    """Response model for vocabulary list"""
    success: bool
    vocabulary_words: Optional[List[Dict[str, str]]] = None
    reading_level: Optional[str] = None
    total_words: Optional[int] = None
    error: Optional[str] = None


class VocabularyStatsResponse(BaseModel):
    """Response model for vocabulary statistics"""
    total_lookups: int
    unique_words_explained: int
    explanations_by_style: Dict[str, int]


@router.post("/explain", response_model=WordExplanationResponse)
def explain_word(request: WordExplanationRequest):
    """
    Explain a word with age-appropriate definition

    This endpoint provides:
    - Clear, level-appropriate definition
    - Simpler alternative explanation
    - Usage examples
    - Related words (synonyms, antonyms)
    """
    if not vocabulary_agent:
        raise HTTPException(
            status_code=503,
            detail="Vocabulary Agent is not available"
        )

    try:
        logger.info(
            f"Explaining word '{request.word}' for student {request.student_id} "
            f"at reading level {request.reading_level}"
        )

        result = vocabulary_agent.explain_word(
            word=request.word,
            reading_level=request.reading_level,
            context=request.context,
            style=request.style,
            include_examples=request.include_examples
        )

        return WordExplanationResponse(**result)

    except Exception as e:
        logger.error(f"Word explanation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-phrase", response_model=PhraseExplanationResponse)
def explain_phrase(request: PhraseExplanationRequest):
    """
    Explain a phrase or idiom

    This endpoint explains:
    - Phrases
    - Idioms
    - Common expressions
    - Figurative language
    """
    if not vocabulary_agent:
        raise HTTPException(
            status_code=503,
            detail="Vocabulary Agent is not available"
        )

    try:
        logger.info(f"Explaining phrase '{request.phrase}' for student {request.student_id}")

        result = vocabulary_agent.explain_phrase(
            phrase=request.phrase,
            reading_level=request.reading_level,
            context=request.context
        )

        return PhraseExplanationResponse(**result)

    except Exception as e:
        logger.error(f"Phrase explanation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build-list", response_model=VocabularyListResponse)
def build_vocabulary_list(request: VocabularyListRequest):
    """
    Build a vocabulary list from story text

    Extracts the most educational words from a story and provides:
    - Word
    - Brief definition
    - Why it's important to know
    """
    if not vocabulary_agent:
        raise HTTPException(
            status_code=503,
            detail="Vocabulary Agent is not available"
        )

    try:
        logger.info(
            f"Building vocabulary list for student {request.student_id} "
            f"with {request.max_words} words"
        )

        result = vocabulary_agent.build_vocabulary_list(
            story_text=request.story_text,
            reading_level=request.reading_level,
            max_words=request.max_words
        )

        return VocabularyListResponse(**result)

    except Exception as e:
        logger.error(f"Vocabulary list building failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=VocabularyStatsResponse)
def get_vocabulary_stats():
    """
    Get vocabulary agent statistics

    Returns:
    - Total word lookups
    - Unique words explained
    - Distribution by explanation style
    """
    if not vocabulary_agent:
        raise HTTPException(
            status_code=503,
            detail="Vocabulary Agent is not available"
        )

    try:
        stats = vocabulary_agent.get_stats()
        return VocabularyStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
