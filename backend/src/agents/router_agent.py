"""
Router Agent - Intelligent query router with intent classification and engagement detection
"""

from typing import Dict, Any, Optional, Tuple
from enum import Enum
import logging
import re
from openai import OpenAI

logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    """Available specialist agents"""
    STORY = "story"
    COMPREHENSION = "comprehension"
    VOCABULARY = "vocabulary"
    QUIZ = "quiz"
    PROGRESS = "progress"
    UNKNOWN = "unknown"


class EngagementLevel(str, Enum):
    """User engagement states"""
    EXCITED = "excited"
    CURIOUS = "curious"
    NEUTRAL = "neutral"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    BORED = "bored"


class RouterAgent:
    """
    Intelligent router that classifies intent and detects engagement
    to route queries to the most appropriate specialist agent
    """

    def __init__(self, openai_api_key: str):
        """
        Initialize the router agent

        Args:
            openai_api_key: OpenAI API key for GPT-4 classification
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.routing_stats = {
            "total_queries": 0,
            "routes": {agent.value: 0 for agent in AgentType}
        }

        # Intent patterns for quick classification
        self.intent_patterns = {
            AgentType.STORY: [
                r"tell me a story",
                r"story about",
                r"once upon a time",
                r"create a story",
                r"continue the story",
                r"what happens next"
            ],
            AgentType.COMPREHENSION: [
                r"what happened",
                r"why did",
                r"who is",
                r"summarize",
                r"explain the story",
                r"what was the"
            ],
            AgentType.VOCABULARY: [
                r"what does .* mean",
                r"what is a ",
                r"define",
                r"meaning of",
                r"vocabulary",
                r"don't understand the word"
            ],
            AgentType.QUIZ: [
                r"quiz me",
                r"test me",
                r"ask me questions",
                r"check my understanding",
                r"practice questions"
            ],
            AgentType.PROGRESS: [
                r"how am i doing",
                r"my progress",
                r"reading level",
                r"show my stats",
                r"how much have i learned"
            ]
        }

        # Engagement detection patterns
        self.engagement_patterns = {
            EngagementLevel.EXCITED: [
                r"wow", r"amazing", r"awesome", r"love", r"more", r"tell me more",
                r"!", r"cool", r"fantastic"
            ],
            EngagementLevel.CONFUSED: [
                r"don't understand", r"confused", r"what", r"huh", r"unclear",
                r"\?{2,}", r"i'm lost", r"doesn't make sense"
            ],
            EngagementLevel.FRUSTRATED: [
                r"frustrated", r"hard", r"difficult", r"can't", r"stuck",
                r"give up", r"too hard", r"i don't get it"
            ],
            EngagementLevel.BORED: [
                r"boring", r"bored", r"not interesting", r"something else",
                r"tired of", r"different"
            ],
            EngagementLevel.CURIOUS: [
                r"why", r"how", r"wonder", r"curious", r"interesting",
                r"tell me about", r"what if"
            ]
        }

    def route_query(
        self,
        query: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route a query to the appropriate specialist agent

        Args:
            query: User's query text
            user_id: Unique user identifier
            context: Additional context (reading level, history, etc.)

        Returns:
            Routing decision with agent, engagement, confidence, and metadata
        """
        self.routing_stats["total_queries"] += 1

        # Step 1: Quick pattern-based classification
        pattern_agent = self._classify_by_patterns(query)

        # Step 2: Detect engagement level
        engagement = self._detect_engagement(query, context)

        # Step 3: Use GPT-4 for complex cases
        if pattern_agent == AgentType.UNKNOWN:
            gpt_agent, confidence = self._classify_with_gpt4(query, context)
            agent = gpt_agent
        else:
            agent = pattern_agent
            confidence = 0.85  # Pattern-based confidence

        # Step 4: Adjust routing based on engagement
        agent, adjusted_confidence = self._adjust_for_engagement(
            agent, engagement, confidence, context
        )

        # Step 5: Log routing decision
        self.routing_stats["routes"][agent.value] += 1
        logger.info(
            f"Routed query to {agent.value} agent "
            f"(confidence: {adjusted_confidence:.2f}, "
            f"engagement: {engagement.value})"
        )

        return {
            "agent": agent.value,
            "agent_port": self._get_agent_port(agent),
            "engagement": engagement.value,
            "confidence": adjusted_confidence,
            "query": query,
            "user_id": user_id,
            "metadata": {
                "pattern_match": pattern_agent != AgentType.UNKNOWN,
                "requires_adaptation": engagement in [
                    EngagementLevel.CONFUSED,
                    EngagementLevel.FRUSTRATED
                ]
            }
        }

    def _classify_by_patterns(self, query: str) -> AgentType:
        """
        Quick classification using regex patterns

        Args:
            query: User query text

        Returns:
            Matched agent type or UNKNOWN
        """
        query_lower = query.lower()

        for agent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    logger.debug(f"Pattern match: {pattern} -> {agent_type.value}")
                    return agent_type

        return AgentType.UNKNOWN

    def _classify_with_gpt4(
        self,
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> Tuple[AgentType, float]:
        """
        Use GPT-4 to classify ambiguous queries

        Args:
            query: User query text
            context: Additional context

        Returns:
            Tuple of (agent_type, confidence_score)
        """
        try:
            system_prompt = """You are an intelligent routing system for a children's reading platform.

Classify the user's query into ONE of these categories:
- story: User wants to hear/create a story
- comprehension: User has questions about story content
- vocabulary: User wants word definitions/explanations
- quiz: User wants to test their understanding
- progress: User wants to see their reading stats

Respond with ONLY the category name and a confidence score (0-1) separated by a pipe.
Example: "story|0.95" """

            user_prompt = f"Query: {query}"

            if context and "reading_level" in context:
                user_prompt += f"\nReading Level: {context['reading_level']}"

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=20
            )

            result = response.choices[0].message.content.strip()
            agent_str, confidence_str = result.split("|")

            agent = AgentType(agent_str.strip())
            confidence = float(confidence_str.strip())

            logger.info(f"GPT-4 classification: {agent.value} (confidence: {confidence:.2f})")
            return agent, confidence

        except Exception as e:
            logger.error(f"GPT-4 classification failed: {e}")
            # Fallback to story agent for safety
            return AgentType.STORY, 0.5

    def _detect_engagement(
        self,
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> EngagementLevel:
        """
        Detect user's engagement level from query and context

        Args:
            query: User query text
            context: Additional context (previous failures, response time, etc.)

        Returns:
            Detected engagement level
        """
        query_lower = query.lower()

        # Check context signals first
        if context:
            # Repeated failures indicate frustration
            if context.get("consecutive_failures", 0) >= 3:
                return EngagementLevel.FRUSTRATED

            # Quick responses indicate excitement
            if context.get("response_time_seconds", 100) < 5:
                return EngagementLevel.EXCITED

        # Pattern-based detection
        for level, patterns in self.engagement_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    logger.debug(f"Engagement pattern match: {pattern} -> {level.value}")
                    return level

        return EngagementLevel.NEUTRAL

    def _adjust_for_engagement(
        self,
        agent: AgentType,
        engagement: EngagementLevel,
        confidence: float,
        context: Optional[Dict[str, Any]]
    ) -> Tuple[AgentType, float]:
        """
        Adjust routing based on engagement level

        Args:
            agent: Initially selected agent
            engagement: Detected engagement level
            confidence: Initial confidence score
            context: Additional context

        Returns:
            Tuple of (adjusted_agent, adjusted_confidence)
        """
        # If user is confused/frustrated, route to simpler content
        if engagement in [EngagementLevel.CONFUSED, EngagementLevel.FRUSTRATED]:
            # Boost vocabulary agent for confusion
            if agent == AgentType.COMPREHENSION:
                logger.info("Confusion detected: routing to vocabulary for simpler explanation")
                return AgentType.VOCABULARY, confidence * 0.9

        # If user is bored, suggest more engaging content
        if engagement == EngagementLevel.BORED:
            logger.info("Boredom detected: routing to story for engagement")
            return AgentType.STORY, confidence * 0.9

        # If user is excited, maintain current routing
        return agent, confidence

    def _get_agent_port(self, agent: AgentType) -> int:
        """
        Get the port number for a specialist agent

        Args:
            agent: Agent type

        Returns:
            Port number
        """
        port_mapping = {
            AgentType.STORY: 8002,
            AgentType.COMPREHENSION: 8003,
            AgentType.VOCABULARY: 8004,
            AgentType.QUIZ: 8005,
            AgentType.PROGRESS: 8006,
            AgentType.UNKNOWN: 8001  # Route back to self for clarification
        }
        return port_mapping.get(agent, 8001)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics

        Returns:
            Dictionary with routing metrics
        """
        total = self.routing_stats["total_queries"]
        if total == 0:
            return {"total_queries": 0, "distribution": {}}

        distribution = {
            agent: (count / total) * 100
            for agent, count in self.routing_stats["routes"].items()
        }

        return {
            "total_queries": total,
            "distribution": distribution,
            "most_used_agent": max(
                self.routing_stats["routes"].items(),
                key=lambda x: x[1]
            )[0]
        }
