#!/usr/bin/env python3
"""
FastAPI + Dapr Service Generator

Generates a complete FastAPI microservice with Dapr integration and AI agent support.
"""

import os
import sys
import argparse
from pathlib import Path


class ServiceGenerator:
    """Generates FastAPI service templates"""

    def __init__(self, service_name: str, port: int = 8000):
        self.service_name = service_name
        self.port = port
        self.base_dir = Path(service_name)

    def create_directory_structure(self):
        """Create project directory structure"""
        directories = [
            self.base_dir / "src",
            self.base_dir / "src" / "agents",
            self.base_dir / "src" / "models",
            self.base_dir / "src" / "services",
            self.base_dir / "src" / "routers",
            self.base_dir / "tests" / "unit",
            self.base_dir / "tests" / "integration",
            self.base_dir / "k8s",
            self.base_dir / "k8s" / "dapr-components",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "__init__.py").touch()

        print(f"✓ Created directory structure for {self.service_name}")

    def generate_main_py(self):
        """Generate main.py"""
        content = f'''"""
{self.service_name.replace("-", " ").title()} Service
FastAPI application with Dapr integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import health, query
from src.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="{self.service_name}",
    version="1.0.0",
    description="AI-powered microservice with Dapr"
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

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {{settings.APP_NAME}}")
    logger.info(f"Dapr HTTP port: {{settings.DAPR_HTTP_PORT}}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {{settings.APP_NAME}}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
'''
        (self.base_dir / "src" / "main.py").write_text(content)
        print("✓ Generated main.py")

    def generate_config_py(self):
        """Generate config.py"""
        content = '''"""
Configuration management
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    APP_NAME: str = "AI Service"
    PORT: int = 8000
    DAPR_HTTP_PORT: int = 3500
    DAPR_GRPC_PORT: int = 50001

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # Kafka
    KAFKA_BROKERS: str = "kafka.kafka.svc.cluster.local:9092"

    # Database
    DATABASE_URL: str = "postgresql://user:pass@postgres:5432/db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
'''
        (self.base_dir / "src" / "config.py").write_text(content)
        print("✓ Generated config.py")

    def generate_health_router(self):
        """Generate health check router"""
        content = '''"""
Health check endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/live", response_model=HealthResponse)
async def liveness():
    """Liveness probe - is the service running?"""
    return {
        "status": "alive",
        "service": "ai-service"
    }


@router.get("/ready", response_model=HealthResponse)
async def readiness():
    """Readiness probe - is the service ready to handle requests?"""
    # Add checks for dependencies here (database, external APIs, etc.)
    return {
        "status": "ready",
        "service": "ai-service"
    }
'''
        (self.base_dir / "src" / "routers" / "health.py").write_text(content)
        print("✓ Generated health router")

    def generate_query_router(self):
        """Generate query router"""
        content = '''"""
Query processing endpoints
"""

from fastapi import APIRouter, HTTPException
from src.models.requests import QueryRequest
from src.models.responses import QueryResponse
from src.services.agent_service import AgentService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
agent_service = AgentService()


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a user query"""
    try:
        logger.info(f"Processing query from student {request.student_id}")

        response = await agent_service.process_query(
            query=request.query,
            student_id=request.student_id,
            context=request.context or {}
        )

        return QueryResponse(
            response=response,
            agent_type="triage",
            student_id=request.student_id
        )

    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
'''
        (self.base_dir / "src" / "routers" / "query.py").write_text(content)
        print("✓ Generated query router")

    def generate_models(self):
        """Generate Pydantic models"""
        # Request models
        requests_content = '''"""
Request models
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    query: str
    student_id: str
    context: Optional[Dict[str, Any]] = None
'''
        (self.base_dir / "src" / "models" / "requests.py").write_text(requests_content)

        # Response models
        responses_content = '''"""
Response models
"""

from pydantic import BaseModel
from typing import Optional


class QueryResponse(BaseModel):
    response: str
    agent_type: str
    student_id: str
'''
        (self.base_dir / "src" / "models" / "responses.py").write_text(responses_content)

        print("✓ Generated models")

    def generate_base_agent(self):
        """Generate base agent class"""
        content = '''"""
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
'''
        (self.base_dir / "src" / "agents" / "base_agent.py").write_text(content)
        print("✓ Generated base agent")

    def generate_agent_service(self):
        """Generate agent service"""
        content = '''"""
Agent service - orchestrates AI agents
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AgentService:
    """Orchestrates AI agent interactions"""

    def __init__(self):
        # Initialize agents here
        pass

    async def process_query(
        self,
        query: str,
        student_id: str,
        context: Dict[str, Any]
    ) -> str:
        """Process a query using appropriate agent"""

        logger.info(f"Processing query: {query[:50]}...")

        # TODO: Implement agent selection and routing
        response = f"Processed query: {query}"

        return response
'''
        (self.base_dir / "src" / "services" / "agent_service.py").write_text(content)
        print("✓ Generated agent service")

    def generate_requirements(self):
        """Generate requirements.txt"""
        content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
openai==1.3.0
aiohttp==3.9.0
python-multipart==0.0.6
'''
        (self.base_dir / "requirements.txt").write_text(content)
        print("✓ Generated requirements.txt")

    def generate_dockerfile(self):
        """Generate Dockerfile"""
        content = f'''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Expose port
EXPOSE {self.port}

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "{self.port}"]
'''
        (self.base_dir / "Dockerfile").write_text(content)
        print("✓ Generated Dockerfile")

    def generate_k8s_deployment(self):
        """Generate Kubernetes deployment"""
        content = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {self.service_name}
  namespace: learnflow
  labels:
    app: {self.service_name}
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "{self.service_name}"
    dapr.io/app-port: "{self.port}"
    dapr.io/log-level: "info"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {self.service_name}
  template:
    metadata:
      labels:
        app: {self.service_name}
    spec:
      containers:
      - name: service
        image: {self.service_name}:latest
        ports:
        - containerPort: {self.port}
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-credentials
              key: api-key
        - name: DAPR_HTTP_PORT
          value: "3500"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: {self.port}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: {self.port}
          initialDelaySeconds: 5
          periodSeconds: 5
'''
        (self.base_dir / "k8s" / "deployment.yaml").write_text(content)
        print("✓ Generated Kubernetes deployment")

    def generate_k8s_service(self):
        """Generate Kubernetes service"""
        content = f'''apiVersion: v1
kind: Service
metadata:
  name: {self.service_name}
  namespace: learnflow
spec:
  selector:
    app: {self.service_name}
  ports:
  - port: 80
    targetPort: {self.port}
  type: ClusterIP
'''
        (self.base_dir / "k8s" / "service.yaml").write_text(content)
        print("✓ Generated Kubernetes service")

    def generate(self):
        """Generate complete service"""
        print(f"🚀 Generating FastAPI + Dapr service: {self.service_name}")
        print()

        self.create_directory_structure()
        self.generate_main_py()
        self.generate_config_py()
        self.generate_health_router()
        self.generate_query_router()
        self.generate_models()
        self.generate_base_agent()
        self.generate_agent_service()
        self.generate_requirements()
        self.generate_dockerfile()
        self.generate_k8s_deployment()
        self.generate_k8s_service()

        print()
        print(f"✓ Service generated successfully: {self.base_dir}")
        print()
        print("Next steps:")
        print(f"  1. cd {self.service_name}")
        print("  2. Add AI agents: python ../scripts/add_agent.py --agent-type concepts")
        print("  3. pip install -r requirements.txt")
        print("  4. python src/main.py")


def main():
    parser = argparse.ArgumentParser(description="Generate FastAPI + Dapr service")
    parser.add_argument("--name", required=True, help="Service name")
    parser.add_argument("--port", type=int, default=8000, help="Application port")

    args = parser.parse_args()

    try:
        generator = ServiceGenerator(args.name, args.port)
        generator.generate()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
