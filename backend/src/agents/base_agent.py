"""
Base agent implementation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from openai import OpenAI
from src.config import settings


class BaseAgent(ABC):
    """Abstract base class for AI agents"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    @abstractmethod
    async def process(self, query: str, context: Dict[str, Any]) -> str:
        """Process a query and return a response"""
        pass

    async def _generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
