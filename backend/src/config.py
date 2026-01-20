"""
Configuration management
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    APP_NAME: str = "StoryForge Router Service"
    PORT: int = 8000
    DAPR_HTTP_PORT: int = 3500
    DAPR_GRPC_PORT: int = 50001

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # Router Configuration
    ENABLE_GPT4_ROUTING: bool = True
    ROUTER_CONFIDENCE_THRESHOLD: float = 0.7

    # Kafka
    KAFKA_BROKERS: str = "kafka.kafka.svc.cluster.local:9092"

    # Database
    DATABASE_URL: str = "postgresql://user:pass@postgres:5432/db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
