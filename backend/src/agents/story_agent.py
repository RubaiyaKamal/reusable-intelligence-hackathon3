"""
Story Agent - Generates age-appropriate stories with adaptive vocabulary
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class StoryType(str, Enum):
    """Available story genres"""
    ADVENTURE = "adventure"
    FRIENDSHIP = "friendship"
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    ANIMAL = "animal"
    SCIENCE = "science"
    CUSTOM = "custom"


class ReadingLevel(str, Enum):
    """Reading level categories"""
    BEGINNER = "beginner"  # Ages 4-6
    EARLY = "early"  # Ages 6-8
    INTERMEDIATE = "intermediate"  # Ages 8-10
    ADVANCED = "advanced"  # Ages 10+


class StoryAgent:
    """
    Generates engaging, age-appropriate stories with adaptive vocabulary
    and educational value
    """

    def __init__(self, openai_api_key: str):
        """
        Initialize the Story Agent

        Args:
            openai_api_key: OpenAI API key for GPT-4
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.story_stats = {
            "total_stories": 0,
            "stories_by_type": {story_type.value: 0 for story_type in StoryType},
            "stories_by_level": {level.value: 0 for level in ReadingLevel}
        }

        # Story templates for different types
        self.story_themes = {
            StoryType.ADVENTURE: [
                "a brave explorer discovering a hidden land",
                "a journey to find a magical treasure",
                "a quest to save a village from danger",
                "an expedition to climb the tallest mountain"
            ],
            StoryType.FRIENDSHIP: [
                "two unlikely friends helping each other",
                "a new kid making friends at school",
                "friends working together to solve a problem",
                "a friendship tested by a misunderstanding"
            ],
            StoryType.FANTASY: [
                "a magical world with talking animals",
                "a child who discovers they have magical powers",
                "a fairy tale kingdom with a twist",
                "a portal to an enchanted realm"
            ],
            StoryType.MYSTERY: [
                "a missing object that needs to be found",
                "strange events in a quiet neighborhood",
                "a puzzle that only clever thinking can solve",
                "a secret that changes everything"
            ],
            StoryType.ANIMAL: [
                "animals in the wild facing a challenge",
                "a pet's perspective on family life",
                "forest creatures preparing for winter",
                "a lost animal finding their way home"
            ],
            StoryType.SCIENCE: [
                "exploring the wonders of space",
                "discovering how things work",
                "a science experiment gone wonderfully right",
                "learning about nature through adventure"
            ]
        }

    def generate_story(
        self,
        story_type: str = "adventure",
        reading_level: int = 50,
        length: str = "medium",
        theme: Optional[str] = None,
        characters: Optional[List[str]] = None,
        moral_lesson: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a new story

        Args:
            story_type: Type of story (adventure, friendship, etc.)
            reading_level: Reading level (0-100, where 0=beginner, 100=advanced)
            length: Story length (short, medium, long)
            theme: Optional specific theme
            characters: Optional list of character names/types
            moral_lesson: Optional lesson to embed
            context: Additional context (user preferences, etc.)

        Returns:
            Dictionary with story content and metadata
        """
        try:
            self.story_stats["total_stories"] += 1

            # Determine reading level category
            level = self._get_reading_level_category(reading_level)
            self.story_stats["stories_by_level"][level.value] += 1

            # Track story type
            if story_type in [t.value for t in StoryType]:
                self.story_stats["stories_by_type"][story_type] += 1

            # Create story prompt
            prompt = self._create_story_prompt(
                story_type=story_type,
                level=level,
                length=length,
                theme=theme,
                characters=characters,
                moral_lesson=moral_lesson
            )

            # Generate story with GPT-4
            logger.info(f"Generating {story_type} story at {level.value} level")

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(level)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Higher creativity for stories
                max_tokens=self._get_max_tokens(length)
            )

            story_text = response.choices[0].message.content.strip()

            # Extract title if present
            title = self._extract_title(story_text)

            # Get vocabulary words
            vocab_words = self._extract_vocabulary(story_text, level)

            return {
                "success": True,
                "story": story_text,
                "title": title,
                "story_type": story_type,
                "reading_level": level.value,
                "length": length,
                "vocabulary_words": vocab_words,
                "metadata": {
                    "word_count": len(story_text.split()),
                    "estimated_reading_time": self._estimate_reading_time(story_text),
                    "moral_lesson": moral_lesson,
                    "characters": characters or []
                }
            }

        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_story": self._get_fallback_story(story_type, level)
            }

    def continue_story(
        self,
        previous_story: str,
        user_input: Optional[str] = None,
        reading_level: int = 50,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Continue an existing story

        Args:
            previous_story: The story so far
            user_input: Optional user direction for continuation
            reading_level: Reading level (0-100)
            context: Additional context

        Returns:
            Dictionary with continuation and metadata
        """
        try:
            level = self._get_reading_level_category(reading_level)

            prompt = f"""Continue this story naturally and engagingly:

{previous_story}

"""
            if user_input:
                prompt += f"\nUser wants: {user_input}\n"

            prompt += "Continue the story (2-3 paragraphs):"

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(level)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=500
            )

            continuation = response.choices[0].message.content.strip()

            return {
                "success": True,
                "continuation": continuation,
                "full_story": previous_story + "\n\n" + continuation,
                "reading_level": level.value
            }

        except Exception as e:
            logger.error(f"Story continuation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _get_reading_level_category(self, reading_level: int) -> ReadingLevel:
        """Convert numeric reading level to category"""
        if reading_level < 25:
            return ReadingLevel.BEGINNER
        elif reading_level < 50:
            return ReadingLevel.EARLY
        elif reading_level < 75:
            return ReadingLevel.INTERMEDIATE
        else:
            return ReadingLevel.ADVANCED

    def _get_system_prompt(self, level: ReadingLevel) -> str:
        """Get system prompt based on reading level"""
        base_prompt = "You are an expert children's story writer creating engaging, educational content."

        level_guidance = {
            ReadingLevel.BEGINNER: """
- Use simple words (3-5 letters mostly)
- Short sentences (5-8 words)
- Present tense
- Clear, concrete concepts
- Repetition for learning
- Age appropriate: 4-6 years old
""",
            ReadingLevel.EARLY: """
- Use common words with some new vocabulary
- Medium sentences (8-12 words)
- Mix of present and past tense
- Introduce simple abstract concepts
- Some descriptive language
- Age appropriate: 6-8 years old
""",
            ReadingLevel.INTERMEDIATE: """
- Use varied vocabulary with challenging words
- Longer sentences (12-15 words)
- Complex sentence structures
- Abstract thinking encouraged
- Rich descriptive language
- Age appropriate: 8-10 years old
""",
            ReadingLevel.ADVANCED: """
- Use sophisticated vocabulary
- Complex sentences with clauses
- Multiple perspectives or timelines
- Deep themes and symbolism
- Literary devices (metaphors, foreshadowing)
- Age appropriate: 10+ years old
"""
        }

        return base_prompt + "\n\nGuidelines for this story:" + level_guidance[level]

    def _create_story_prompt(
        self,
        story_type: str,
        level: ReadingLevel,
        length: str,
        theme: Optional[str],
        characters: Optional[List[str]],
        moral_lesson: Optional[str]
    ) -> str:
        """Create the story generation prompt"""
        prompt = f"Write a {length} {story_type} story"

        if theme:
            prompt += f" about {theme}"
        elif story_type in [t.value for t in StoryType] and story_type != "custom":
            # Use a theme from templates
            import random
            themes = self.story_themes.get(StoryType(story_type), [])
            if themes:
                prompt += f" about {random.choice(themes)}"

        if characters:
            prompt += f" featuring these characters: {', '.join(characters)}"

        if moral_lesson:
            prompt += f"\n\nImportant: Naturally weave in this lesson: {moral_lesson}"

        # Add length guidance
        length_words = {
            "short": "200-300 words",
            "medium": "400-600 words",
            "long": "700-1000 words"
        }
        prompt += f"\n\nTarget length: {length_words.get(length, '400-600 words')}"

        prompt += "\n\nFormat: Start with a clear title, then the story."

        return prompt

    def _get_max_tokens(self, length: str) -> int:
        """Get max tokens based on story length"""
        token_limits = {
            "short": 400,
            "medium": 800,
            "long": 1200
        }
        return token_limits.get(length, 800)

    def _extract_title(self, story_text: str) -> str:
        """Extract title from story text"""
        lines = story_text.split('\n')
        if lines and len(lines[0]) < 100:
            # First line is likely the title
            title = lines[0].strip('#').strip('*').strip('"').strip()
            if len(title) < 100:
                return title
        return "Untitled Story"

    def _extract_vocabulary(self, story_text: str, level: ReadingLevel) -> List[str]:
        """Extract challenging vocabulary words"""
        # Simple vocabulary extraction (in production, use NLP)
        words = story_text.split()
        challenging_words = [
            word.strip('.,!?"').lower()
            for word in words
            if len(word) > 7 and word.isalpha()
        ]

        # Return unique words, limited by reading level
        limit = {
            ReadingLevel.BEGINNER: 3,
            ReadingLevel.EARLY: 5,
            ReadingLevel.INTERMEDIATE: 8,
            ReadingLevel.ADVANCED: 10
        }

        return list(set(challenging_words))[:limit[level]]

    def _estimate_reading_time(self, story_text: str) -> int:
        """Estimate reading time in minutes"""
        words = len(story_text.split())
        # Average reading speed: 200 words/minute for children
        return max(1, round(words / 200))

    def _get_fallback_story(self, story_type: str, level: ReadingLevel) -> str:
        """Provide a simple fallback story if generation fails"""
        return f"""The Little Adventure

Once upon a time, there was a curious child who loved to explore.

One sunny day, they discovered something amazing in their backyard - a tiny door hidden under a big leaf!

When they opened it, they found a whole new world of tiny creatures having a party.

The creatures welcomed them with open arms and they all became the best of friends.

The end.

(This is a simple fallback story. Please try again for a more personalized story!)"""

    def get_stats(self) -> Dict[str, Any]:
        """Get story generation statistics"""
        return {
            "total_stories": self.story_stats["total_stories"],
            "stories_by_type": self.story_stats["stories_by_type"],
            "stories_by_level": self.story_stats["stories_by_level"]
        }

    def get_available_story_types(self) -> List[str]:
        """Get list of available story types"""
        return [story_type.value for story_type in StoryType]
