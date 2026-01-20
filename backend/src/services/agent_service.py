"""
Agent service - orchestrates AI agents with intelligent routing
"""

from typing import Dict, Any, Optional
import logging
from src.agents.router_agent import RouterAgent
from src.agents.story_agent import StoryAgent
from src.agents.vocabulary_agent import VocabularyAgent
from src.agents.comprehension_agent import ComprehensionAgent
from src.config import settings

logger = logging.getLogger(__name__)


class AgentService:
    """Orchestrates AI agent interactions using intelligent routing"""

    def __init__(self):
        """Initialize the agent service with router and specialist agents"""
        try:
            # Initialize agents
            if not settings.OPENAI_API_KEY:
                logger.warning("No OpenAI API key found. Router will use pattern matching only.")
                self.router = None
                self.story_agent = None
                self.vocabulary_agent = None
                self.comprehension_agent = None
            else:
                # Initialize agents with error handling for proxy-related issues
                try:
                    self.router = RouterAgent(openai_api_key=settings.OPENAI_API_KEY)
                except TypeError as te:
                    if "'proxies'" in str(te):
                        logger.error(f"Proxy configuration error in RouterAgent: {te}")
                        logger.warning("RouterAgent disabled due to proxy configuration issue")
                        self.router = None
                    else:
                        raise
                except Exception as e:
                    logger.error(f"Failed to initialize RouterAgent: {e}")
                    self.router = None

                try:
                    self.story_agent = StoryAgent(openai_api_key=settings.OPENAI_API_KEY)
                except TypeError as te:
                    if "'proxies'" in str(te):
                        logger.error(f"Proxy configuration error in StoryAgent: {te}")
                        logger.warning("StoryAgent disabled due to proxy configuration issue")
                        self.story_agent = None
                    else:
                        raise
                except Exception as e:
                    logger.error(f"Failed to initialize StoryAgent: {e}")
                    self.story_agent = None

                try:
                    self.vocabulary_agent = VocabularyAgent(openai_api_key=settings.OPENAI_API_KEY)
                except TypeError as te:
                    if "'proxies'" in str(te):
                        logger.error(f"Proxy configuration error in VocabularyAgent: {te}")
                        logger.warning("VocabularyAgent disabled due to proxy configuration issue")
                        self.vocabulary_agent = None
                    else:
                        raise
                except Exception as e:
                    logger.error(f"Failed to initialize VocabularyAgent: {e}")
                    self.vocabulary_agent = None

                try:
                    self.comprehension_agent = ComprehensionAgent(openai_api_key=settings.OPENAI_API_KEY)
                except TypeError as te:
                    if "'proxies'" in str(te):
                        logger.error(f"Proxy configuration error in ComprehensionAgent: {te}")
                        logger.warning("ComprehensionAgent disabled due to proxy configuration issue")
                        self.comprehension_agent = None
                    else:
                        raise
                except Exception as e:
                    logger.error(f"Failed to initialize ComprehensionAgent: {e}")
                    self.comprehension_agent = None

                # Log initialization status
                active_agents = sum([
                    self.router is not None,
                    self.story_agent is not None,
                    self.vocabulary_agent is not None,
                    self.comprehension_agent is not None
                ])
                logger.info(f"Agent initialization complete: {active_agents}/4 agents active")

        except Exception as e:
            logger.error(f"Critical error in agent initialization: {e}")
            self.router = None
            self.story_agent = None
            self.vocabulary_agent = None
            self.comprehension_agent = None

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
            Routing decision with agent, engagement, and metadata
        """
        if not self.router:
            logger.error("Router not initialized")
            return {
                "error": "Router service unavailable",
                "agent": "unknown",
                "agent_port": 8001
            }

        try:
            routing_decision = self.router.route_query(
                query=query,
                user_id=user_id,
                context=context or {}
            )

            logger.info(
                f"Query routed to {routing_decision['agent']} agent "
                f"(engagement: {routing_decision['engagement']}, "
                f"confidence: {routing_decision['confidence']:.2f})"
            )

            return routing_decision

        except Exception as e:
            logger.error(f"Routing failed: {e}")
            return {
                "error": str(e),
                "agent": "unknown",
                "agent_port": 8001
            }

    def process_query(
        self,
        query: str,
        student_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process a query using appropriate agent

        Args:
            query: User's query text
            student_id: User identifier
            context: Additional context

        Returns:
            Response text
        """
        logger.info(f"Processing query: {query[:50]}...")

        # Route the query
        routing = self.route_query(query, student_id, context)

        if "error" in routing:
            return f"Error: {routing['error']}"

        agent = routing['agent']
        engagement = routing['engagement']
        confidence = routing['confidence']

        # Process with appropriate specialist agent
        if agent == "story" and self.story_agent:
            # Generate story
            reading_level = context.get("reading_level", 50) if context else 50
            result = self.story_agent.generate_story(
                story_type="adventure",
                reading_level=reading_level,
                length="medium",
                context=context
            )

            if result["success"]:
                response = f"""Story Agent Response

Title: {result['title']}

{result['story']}

---
Reading Level: {result['reading_level']}
Vocabulary Words: {', '.join(result['vocabulary_words'][:5])}
Estimated Reading Time: {result['metadata']['estimated_reading_time']} minute(s)
"""
            else:
                response = f"Story generation failed: {result.get('error', 'Unknown error')}"

        elif agent == "vocabulary" and self.vocabulary_agent:
            # Extract word from query
            import re
            word_match = re.search(r"what (?:does|is) (?:the word )?['\"]?(\w+)['\"]? mean", query, re.IGNORECASE)
            if word_match:
                word = word_match.group(1)
            else:
                # Try to extract last significant word
                words = query.split()
                word = words[-1].strip("?.!")

            reading_level = context.get("reading_level", 50) if context else 50
            result = self.vocabulary_agent.explain_word(
                word=word,
                reading_level=reading_level,
                context=None
            )

            if result["success"]:
                response = f"""Vocabulary Agent Response

Word: {result['word']}

Definition: {result['definition']}

Simple Explanation: {result['simple_explanation']}

Examples:
{chr(10).join('- ' + ex for ex in result['examples'][:3])}

Synonyms: {', '.join(result['synonyms'][:3])}
"""
            else:
                response = f"Vocabulary explanation failed: {result.get('error', 'Unknown error')}"

        else:
            # For agents not yet implemented
            response = f"""Router Analysis

Query: {query}

Routed To: {agent.upper()} Agent (Port {routing['agent_port']})
Engagement Level: {engagement}
Confidence: {confidence:.1%}

The {agent} agent would handle this request with content adapted to your engagement level.

Note: This agent is currently being implemented.
"""

        return response

    def get_router_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics

        Returns:
            Dictionary with routing metrics
        """
        if not self.router:
            return {"error": "Router not initialized"}

        return self.router.get_stats()
