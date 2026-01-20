"""
StoryForge API Service
FastAPI application with intelligent multi-agent routing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import health, query, router, story, vocabulary, comprehension
from src.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="storyforge-api",
    version="1.0.0",
    description="AI-powered children's reading platform with multi-agent routing"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(router.router, prefix="/api/v1/router", tags=["router"])
app.include_router(story.router, prefix="/api/v1/story", tags=["story"])
app.include_router(vocabulary.router, prefix="/api/v1/vocabulary", tags=["vocabulary"])
app.include_router(comprehension.router, prefix="/api/v1/comprehension", tags=["comprehension"])

@app.on_event("startup")
def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"DAPR_HTTP_PORT: {settings.DAPR_HTTP_PORT}")

@app.on_event("shutdown")
def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
