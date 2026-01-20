"""
Vocabulary Agent - Provides word definitions, examples, and vocabulary building
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class ExplanationStyle(str, Enum):
    """Different explanation styles for vocabulary"""
    SIMPLE = "simple"  # Very basic, young children
    DETAILED = "detailed"  # More comprehensive
    CONTEXTUAL = "contextual"  # Based on story context
    VISUAL = "visual"  # With analogies and imagery


class VocabularyAgent:
    """
    Provides word definitions, examples, and helps build vocabulary
    with age-appropriate explanations
    """

    def __init__(self, openai_api_key: str):
        """
        Initialize the Vocabulary Agent

        Args:
            openai_api_key: OpenAI API key for GPT-4
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.vocabulary_stats = {
            "total_lookups": 0,
            "words_explained": set(),
            "explanations_by_style": {style.value: 0 for style in ExplanationStyle}
        }

    def explain_word(
        self,
        word: str,
        reading_level: int = 50,
        context: Optional[str] = None,
        style: str = "detailed",
        include_examples: bool = True,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Explain a word with age-appropriate definition

        Args:
            word: The word to explain
            reading_level: Reading level (0-100)
            context: Optional sentence/paragraph context
            style: Explanation style (simple/detailed/contextual/visual)
            include_examples: Include usage examples
            user_context: Additional user context

        Returns:
            Dictionary with definition, examples, and related words
        """
        try:
            self.vocabulary_stats["total_lookups"] += 1
            self.vocabulary_stats["words_explained"].add(word.lower())

            if style in [s.value for s in ExplanationStyle]:
                self.vocabulary_stats["explanations_by_style"][style] += 1

            # Determine explanation approach based on reading level
            level_category = self._get_level_category(reading_level)

            # Create explanation prompt
            prompt = self._create_explanation_prompt(
                word=word,
                level_category=level_category,
                context=context,
                style=style,
                include_examples=include_examples
            )

            logger.info(f"Explaining word '{word}' at {level_category} level")

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(level_category, style)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=400
            )

            explanation_text = response.choices[0].message.content.strip()

            # Parse the response
            parts = self._parse_explanation(explanation_text)

            # Get related words
            related_words = self._get_related_words(word, level_category)

            return {
                "success": True,
                "word": word,
                "definition": parts.get("definition", explanation_text),
                "simple_explanation": parts.get("simple", ""),
                "examples": parts.get("examples", []),
                "synonyms": related_words.get("synonyms", []),
                "antonyms": related_words.get("antonyms", []),
                "related_words": related_words.get("related", []),
                "reading_level": level_category,
                "metadata": {
                    "word_length": len(word),
                    "explanation_style": style,
                    "context_provided": context is not None
                }
            }

        except Exception as e:
            logger.error(f"Word explanation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "word": word,
                "fallback_definition": self._get_fallback_definition(word)
            }

    def explain_phrase(
        self,
        phrase: str,
        reading_level: int = 50,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Explain a phrase or idiom

        Args:
            phrase: The phrase to explain
            reading_level: Reading level (0-100)
            context: Optional context where phrase appears

        Returns:
            Dictionary with phrase explanation
        """
        try:
            level_category = self._get_level_category(reading_level)

            prompt = f"""Explain this phrase or expression: "{phrase}"

Provide:
1. What it means
2. Why it's used
3. A simple example

Keep the explanation appropriate for {level_category} readers."""

            if context:
                prompt += f"\n\nContext where it appears: {context}"

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You explain phrases and idioms to children at {level_category} reading level."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=300
            )

            explanation = response.choices[0].message.content.strip()

            return {
                "success": True,
                "phrase": phrase,
                "explanation": explanation,
                "reading_level": level_category
            }

        except Exception as e:
            logger.error(f"Phrase explanation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def build_vocabulary_list(
        self,
        story_text: str,
        reading_level: int = 50,
        max_words: int = 10
    ) -> Dict[str, Any]:
        """
        Extract challenging vocabulary from a story

        Args:
            story_text: The story text
            reading_level: Reading level (0-100)
            max_words: Maximum words to include

        Returns:
            Dictionary with vocabulary words and brief definitions
        """
        try:
            level_category = self._get_level_category(reading_level)

            prompt = f"""From this story, identify the {max_words} most educational vocabulary words for a {level_category} reader.

Story:
{story_text[:1000]}...

For each word, provide:
1. The word
2. A one-sentence definition
3. Why it's useful to know

Format as: WORD | definition | importance"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a vocabulary educator helping children build their word knowledge."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )

            vocabulary_text = response.choices[0].message.content.strip()
            words = self._parse_vocabulary_list(vocabulary_text)

            return {
                "success": True,
                "vocabulary_words": words,
                "reading_level": level_category,
                "total_words": len(words)
            }

        except Exception as e:
            logger.error(f"Vocabulary list building failed: {e}")
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

    def _get_system_prompt(self, level_category: str, style: str) -> str:
        """Get system prompt based on level and style"""
        base = "You are a vocabulary teacher helping children understand words."

        level_guidance = {
            "beginner": "Use very simple words. Imagine explaining to a 4-6 year old.",
            "early": "Use clear, simple language. Imagine explaining to a 6-8 year old.",
            "intermediate": "Use accessible language with some complex words. Imagine explaining to an 8-10 year old.",
            "advanced": "Use rich vocabulary and nuanced explanations. Imagine explaining to a 10+ year old."
        }

        style_guidance = {
            "simple": "Keep it very brief and clear.",
            "detailed": "Provide a thorough but accessible explanation.",
            "contextual": "Focus on how the word is used in context.",
            "visual": "Use vivid imagery and analogies to explain."
        }

        return f"{base}\n\n{level_guidance.get(level_category, '')}\n{style_guidance.get(style, '')}"

    def _create_explanation_prompt(
        self,
        word: str,
        level_category: str,
        context: Optional[str],
        style: str,
        include_examples: bool
    ) -> str:
        """Create the explanation prompt"""
        prompt = f"Explain the word '{word}'"

        if context:
            prompt += f"\n\nContext: {context}"

        prompt += "\n\nProvide:"
        prompt += "\n1. DEFINITION: A clear definition"
        prompt += "\n2. SIMPLE: An even simpler way to say it"

        if include_examples:
            prompt += "\n3. EXAMPLES: 2-3 example sentences"

        return prompt

    def _parse_explanation(self, explanation_text: str) -> Dict[str, Any]:
        """Parse the explanation response"""
        result = {}

        lines = explanation_text.split('\n')
        current_section = None
        examples = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.upper().startswith("DEFINITION:") or line.startswith("1."):
                current_section = "definition"
                result["definition"] = line.split(":", 1)[1].strip() if ":" in line else line[2:].strip()
            elif line.upper().startswith("SIMPLE:") or line.startswith("2."):
                current_section = "simple"
                result["simple"] = line.split(":", 1)[1].strip() if ":" in line else line[2:].strip()
            elif line.upper().startswith("EXAMPLES:") or line.startswith("3."):
                current_section = "examples"
            elif current_section == "examples" and line:
                examples.append(line.strip("- "))

        if examples:
            result["examples"] = examples

        # If parsing failed, use the whole text as definition
        if not result:
            result["definition"] = explanation_text

        return result

    def _get_related_words(
        self,
        word: str,
        level_category: str
    ) -> Dict[str, List[str]]:
        """Get related words (synonyms, antonyms, etc.)"""
        try:
            prompt = f"""For the word "{word}", provide:
1. 3 synonyms (words with similar meaning)
2. 2 antonyms (words with opposite meaning)
3. 2 related words

Keep all words appropriate for {level_category} readers.
Format: synonyms: word1, word2, word3 | antonyms: word1, word2 | related: word1, word2"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You provide related words for vocabulary building."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )

            result_text = response.choices[0].message.content.strip()

            # Parse the result
            related = {"synonyms": [], "antonyms": [], "related": []}

            if "synonyms:" in result_text.lower():
                syn_part = result_text.lower().split("synonyms:")[1].split("|")[0]
                related["synonyms"] = [w.strip() for w in syn_part.split(",")]

            if "antonyms:" in result_text.lower():
                ant_part = result_text.lower().split("antonyms:")[1].split("|")[0]
                related["antonyms"] = [w.strip() for w in ant_part.split(",")]

            if "related:" in result_text.lower():
                rel_part = result_text.lower().split("related:")[1]
                related["related"] = [w.strip() for w in rel_part.split(",")]

            return related

        except Exception as e:
            logger.warning(f"Could not get related words: {e}")
            return {"synonyms": [], "antonyms": [], "related": []}

    def _parse_vocabulary_list(self, vocab_text: str) -> List[Dict[str, str]]:
        """Parse vocabulary list from response"""
        words = []
        lines = vocab_text.split('\n')

        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    words.append({
                        "word": parts[0],
                        "definition": parts[1],
                        "importance": parts[2]
                    })

        return words

    def _get_fallback_definition(self, word: str) -> str:
        """Provide a simple fallback definition"""
        return f"'{word}' is a word you might see in stories. Ask a teacher or parent to help explain what it means!"

    def get_stats(self) -> Dict[str, Any]:
        """Get vocabulary agent statistics"""
        return {
            "total_lookups": self.vocabulary_stats["total_lookups"],
            "unique_words_explained": len(self.vocabulary_stats["words_explained"]),
            "explanations_by_style": self.vocabulary_stats["explanations_by_style"]
        }
