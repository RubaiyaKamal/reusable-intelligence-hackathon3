"""
Comprehension Agent - Answers questions about stories and assesses understanding
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class QuestionType(str, Enum):
    """Types of comprehension questions"""
    LITERAL = "literal"  # Who, what, when, where
    INFERENTIAL = "inferential"  # Why, how, implicit meaning
    EVALUATIVE = "evaluative"  # Opinion, judgment
    SUMMARY = "summary"  # Overall understanding


class ComprehensionAgent:
    """
    Answers questions about stories and assesses reading comprehension
    """

    def __init__(self, openai_api_key: str):
        """
        Initialize the Comprehension Agent

        Args:
            openai_api_key: OpenAI API key for GPT-4
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.comprehension_stats = {
            "total_questions": 0,
            "questions_by_type": {qtype.value: 0 for qtype in QuestionType},
            "summaries_generated": 0
        }

    def answer_question(
        self,
        question: str,
        story_text: str,
        reading_level: int = 50,
        provide_hints: bool = False,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question about a story

        Args:
            question: The question to answer
            story_text: The story text
            reading_level: Reading level (0-100)
            provide_hints: Include hints to help student
            context: Additional context

        Returns:
            Dictionary with answer and metadata
        """
        try:
            self.comprehension_stats["total_questions"] += 1

            level_category = self._get_level_category(reading_level)
            question_type = self._classify_question(question)

            self.comprehension_stats["questions_by_type"][question_type.value] += 1

            prompt = self._create_answer_prompt(
                question=question,
                story_text=story_text,
                level_category=level_category,
                question_type=question_type,
                provide_hints=provide_hints
            )

            logger.info(f"Answering {question_type.value} question at {level_category} level")

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(level_category)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=400
            )

            answer_text = response.choices[0].message.content.strip()

            # Parse answer
            parsed = self._parse_answer(answer_text, provide_hints)

            return {
                "success": True,
                "question": question,
                "answer": parsed.get("answer", answer_text),
                "explanation": parsed.get("explanation", ""),
                "hints": parsed.get("hints", []) if provide_hints else [],
                "question_type": question_type.value,
                "reading_level": level_category,
                "metadata": {
                    "story_length": len(story_text.split()),
                    "answer_confidence": "high"
                }
            }

        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }

    def generate_summary(
        self,
        story_text: str,
        reading_level: int = 50,
        length: str = "medium",
        focus: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a summary of a story

        Args:
            story_text: The story text
            reading_level: Reading level (0-100)
            length: Summary length (short/medium/detailed)
            focus: Optional focus area (characters/plot/theme)

        Returns:
            Dictionary with summary
        """
        try:
            self.comprehension_stats["summaries_generated"] += 1

            level_category = self._get_level_category(reading_level)

            prompt = self._create_summary_prompt(
                story_text=story_text,
                level_category=level_category,
                length=length,
                focus=focus
            )

            logger.info(f"Generating {length} summary at {level_category} level")

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You help students understand stories by creating clear summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=self._get_summary_tokens(length)
            )

            summary_text = response.choices[0].message.content.strip()

            # Extract key elements
            elements = self._extract_story_elements(summary_text)

            return {
                "success": True,
                "summary": summary_text,
                "key_characters": elements.get("characters", []),
                "main_events": elements.get("events", []),
                "theme": elements.get("theme", ""),
                "reading_level": level_category,
                "length": length
            }

        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def generate_questions(
        self,
        story_text: str,
        reading_level: int = 50,
        num_questions: int = 5,
        difficulty: str = "mixed"
    ) -> Dict[str, Any]:
        """
        Generate comprehension questions for a story

        Args:
            story_text: The story text
            reading_level: Reading level (0-100)
            num_questions: Number of questions to generate
            difficulty: Question difficulty (easy/medium/hard/mixed)

        Returns:
            Dictionary with questions
        """
        try:
            level_category = self._get_level_category(reading_level)

            prompt = f"""Based on this story, create {num_questions} comprehension questions at {difficulty} difficulty for {level_category} readers.

Story:
{story_text[:1500]}...

For each question, provide:
1. The question
2. The correct answer
3. Why this tests comprehension

Include a mix of literal, inferential, and evaluative questions.

Format each as:
Q: [question]
A: [answer]
WHY: [reasoning]
---"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You create comprehension questions to assess story understanding."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=600
            )

            questions_text = response.choices[0].message.content.strip()
            questions = self._parse_questions(questions_text)

            return {
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "reading_level": level_category,
                "difficulty": difficulty
            }

        except Exception as e:
            logger.error(f"Question generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _get_level_category(self, reading_level: int) -> str:
        """Convert numeric reading level to category"""
        if reading_level < 25:
            return "beginner"
        elif reading_level < 50:
            return "early"
        elif reading_level < 75:
            return "intermediate"
        else:
            return "advanced"

    def _classify_question(self, question: str) -> QuestionType:
        """Classify the type of question"""
        question_lower = question.lower()

        # Literal questions
        if any(word in question_lower for word in ["who", "what", "when", "where", "how many"]):
            return QuestionType.LITERAL

        # Summary questions
        if any(phrase in question_lower for phrase in ["summarize", "what happened", "retell", "main idea"]):
            return QuestionType.SUMMARY

        # Evaluative questions
        if any(word in question_lower for word in ["should", "think", "feel", "opinion", "agree", "best"]):
            return QuestionType.EVALUATIVE

        # Inferential questions (why, how, could, might)
        return QuestionType.INFERENTIAL

    def _get_system_prompt(self, level_category: str) -> str:
        """Get system prompt based on level"""
        base = "You help students understand stories by answering their questions clearly and accurately."

        level_guidance = {
            "beginner": "Use very simple language. Imagine explaining to a 4-6 year old.",
            "early": "Use clear, simple language. Imagine explaining to a 6-8 year old.",
            "intermediate": "Use accessible language. Imagine explaining to an 8-10 year old.",
            "advanced": "Use rich language and nuanced explanations. Imagine explaining to a 10+ year old."
        }

        return f"{base}\n\n{level_guidance.get(level_category, '')}"

    def _create_answer_prompt(
        self,
        question: str,
        story_text: str,
        level_category: str,
        question_type: QuestionType,
        provide_hints: bool
    ) -> str:
        """Create the answer prompt"""
        prompt = f"""Story:
{story_text[:1500]}...

Question: {question}

Provide a clear, accurate answer based on the story."""

        if provide_hints:
            prompt += "\n\nAlso provide 2-3 hints to help the student find the answer themselves."

        if question_type == QuestionType.INFERENTIAL:
            prompt += "\n\nExplain your reasoning since this requires inference."

        return prompt

    def _create_summary_prompt(
        self,
        story_text: str,
        level_category: str,
        length: str,
        focus: Optional[str]
    ) -> str:
        """Create the summary prompt"""
        length_guidance = {
            "short": "2-3 sentences",
            "medium": "1 paragraph (4-6 sentences)",
            "detailed": "2-3 paragraphs with key details"
        }

        prompt = f"""Summarize this story in {length_guidance.get(length, 'medium length')} for {level_category} readers.

Story:
{story_text}

"""

        if focus:
            prompt += f"Focus particularly on: {focus}\n"

        prompt += "Include: main characters, key events, and the story's outcome."

        return prompt

    def _get_summary_tokens(self, length: str) -> int:
        """Get token limit for summary"""
        limits = {
            "short": 100,
            "medium": 200,
            "detailed": 400
        }
        return limits.get(length, 200)

    def _parse_answer(self, answer_text: str, include_hints: bool) -> Dict[str, Any]:
        """Parse answer response"""
        result = {}

        if "ANSWER:" in answer_text.upper():
            parts = answer_text.split("ANSWER:", 1)
            if len(parts) > 1:
                answer_part = parts[1].strip()

                if "EXPLANATION:" in answer_part.upper():
                    ans, exp = answer_part.split("EXPLANATION:", 1)
                    result["answer"] = ans.strip()
                    result["explanation"] = exp.strip()
                else:
                    result["answer"] = answer_part

        if not result:
            result["answer"] = answer_text

        if include_hints and "HINTS:" in answer_text.upper():
            hints_part = answer_text.upper().split("HINTS:")[1]
            hints = [h.strip() for h in hints_part.split("\n") if h.strip() and not h.strip().startswith("ANSWER")]
            result["hints"] = hints[:3]

        return result

    def _extract_story_elements(self, summary_text: str) -> Dict[str, Any]:
        """Extract story elements from summary"""
        # Simple extraction (in production, use NLP)
        return {
            "characters": [],
            "events": [],
            "theme": ""
        }

    def _parse_questions(self, questions_text: str) -> List[Dict[str, str]]:
        """Parse generated questions"""
        questions = []
        current_q = {}

        for line in questions_text.split('\n'):
            line = line.strip()
            if line.startswith("Q:"):
                if current_q:
                    questions.append(current_q)
                current_q = {"question": line[2:].strip()}
            elif line.startswith("A:") and current_q:
                current_q["answer"] = line[2:].strip()
            elif line.startswith("WHY:") and current_q:
                current_q["reasoning"] = line[4:].strip()
            elif line == "---" and current_q:
                questions.append(current_q)
                current_q = {}

        if current_q:
            questions.append(current_q)

        return questions

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehension agent statistics"""
        return {
            "total_questions": self.comprehension_stats["total_questions"],
            "questions_by_type": self.comprehension_stats["questions_by_type"],
            "summaries_generated": self.comprehension_stats["summaries_generated"]
        }
