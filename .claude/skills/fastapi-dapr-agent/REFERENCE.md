# FastAPI + Dapr + Agent Reference Documentation

## Architecture Overview

This skill generates FastAPI microservices that integrate with Dapr for service mesh capabilities and OpenAI Agents SDK for AI-powered functionality.

```
┌─────────────────────────────────────────────────────────┐
│                     Kubernetes Pod                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │  ┌──────────────┐         ┌──────────────┐        │ │
│  │  │   FastAPI    │◄───────►│ Dapr Sidecar │        │ │
│  │  │ Application  │         │  (Port 3500) │        │ │
│  │  │ (Port 8000)  │         └───────┬──────┘        │ │
│  │  └──────┬───────┘                 │               │ │
│  │         │                         │               │ │
│  │   ┌─────▼──────┐            ┌────▼──────┐        │ │
│  │   │ OpenAI     │            │   Kafka   │        │ │
│  │   │ Agents SDK │            │  Pub/Sub  │        │ │
│  │   └────────────┘            └───────────┘        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Service Template Structure

```
service-name/
├── src/
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration management
│   ├── agents/              # AI agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py    # Abstract base class
│   │   ├── concepts_agent.py
│   │   ├── debug_agent.py
│   │   └── triage_agent.py
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py      # Request models
│   │   └── responses.py     # Response models
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── agent_service.py
│   └── routers/             # API routes
│       ├── __init__.py
│       ├── health.py        # Health checks
│       └── query.py         # Query endpoints
├── tests/
│   ├── unit/
│   └── integration/
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Service definition
│   └── dapr-components/     # Dapr components
│       ├── pubsub.yaml
│       └── statestore.yaml
├── requirements.txt
├── Dockerfile
└── README.md
```

## FastAPI Application Template

### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import health, query
from src.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-powered microservice with Dapr"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Dapr HTTP port: {settings.DAPR_HTTP_PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
```

### agents/base_agent.py
```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from openai import OpenAI


class BaseAgent(ABC):
    """Abstract base class for AI agents"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

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
```

### agents/concepts_agent.py
```python
from src.agents.base_agent import BaseAgent
from typing import Dict, Any


class ConceptsAgent(BaseAgent):
    """Agent specialized in explaining Python concepts"""

    SYSTEM_PROMPT = """You are an expert Python tutor. Your role is to:
    1. Explain Python concepts clearly and concisely
    2. Provide code examples when helpful
    3. Adapt explanations to the student's level
    4. Use analogies and real-world examples
    5. Encourage learning through exploration
    """

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        """Process a concept explanation request"""

        student_level = context.get("level", "beginner")
        topic = context.get("topic", "general")

        user_message = f"""
        Student Level: {student_level}
        Topic: {topic}
        Question: {query}

        Please provide a clear explanation with examples.
        """

        response = await self._generate_response(
            system_prompt=self.SYSTEM_PROMPT,
            user_message=user_message,
            temperature=0.7
        )

        return response
```

## Dapr Integration

### Pub/Sub Publishing
```python
import aiohttp
from src.config import settings


async def publish_event(topic: str, data: dict):
    """Publish event to Kafka via Dapr"""
    dapr_url = f"http://localhost:{settings.DAPR_HTTP_PORT}/v1.0/publish/kafka-pubsub/{topic}"

    async with aiohttp.ClientSession() as session:
        async with session.post(dapr_url, json=data) as response:
            if response.status != 200:
                raise Exception(f"Failed to publish event: {await response.text()}")
```

### Pub/Sub Subscription
```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/dapr/subscribe")
async def subscribe():
    """Return subscription configuration"""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "learning.query",
            "route": "/events/query"
        }
    ]

@router.post("/events/query")
async def handle_query(request: Request):
    """Handle incoming query events"""
    data = await request.json()
    # Process event
    return {"status": "success"}
```

### State Management
```python
async def save_state(key: str, value: dict):
    """Save state via Dapr"""
    dapr_url = f"http://localhost:{settings.DAPR_HTTP_PORT}/v1.0/state/statestore"

    async with aiohttp.ClientSession() as session:
        async with session.post(dapr_url, json=[{
            "key": key,
            "value": value
        }]) as response:
            if response.status != 204:
                raise Exception(f"Failed to save state: {await response.text()}")


async def get_state(key: str) -> dict:
    """Retrieve state via Dapr"""
    dapr_url = f"http://localhost:{settings.DAPR_HTTP_PORT}/v1.0/state/statestore/{key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(dapr_url) as response:
            if response.status == 200:
                return await response.json()
            return None
```

## Kubernetes Deployment

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triage-service
  namespace: learnflow
  labels:
    app: triage-service
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "triage-service"
    dapr.io/app-port: "8000"
    dapr.io/log-level: "info"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: triage-service
  template:
    metadata:
      labels:
        app: triage-service
    spec:
      containers:
      - name: service
        image: triage-service:latest
        ports:
        - containerPort: 8000
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
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Dapr Components

### pubsub.yaml
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: learnflow
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "learnflow-services"
  - name: authType
    value: "none"
```

### statestore.yaml
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: learnflow
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=postgres-postgresql.postgres.svc.cluster.local user=learnflow_user password=password dbname=learnflow port=5432 sslmode=disable"
```

## Testing

### Unit Test Example
```python
import pytest
from src.agents.concepts_agent import ConceptsAgent


@pytest.mark.asyncio
async def test_concepts_agent():
    agent = ConceptsAgent(api_key="test-key")

    response = await agent.process(
        query="How do for loops work?",
        context={"level": "beginner", "topic": "loops"}
    )

    assert response is not None
    assert len(response) > 0
```

### Integration Test with Dapr
```python
import pytest
import aiohttp


@pytest.mark.asyncio
async def test_publish_event():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/v1/query",
            json={
                "query": "Explain variables",
                "student_id": "test-123"
            }
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert "response" in data
```

## Best Practices

1. **Async by Default**: Use async/await for all I/O operations
2. **Error Handling**: Wrap external calls in try/except blocks
3. **Logging**: Use structured logging with context
4. **Configuration**: Use environment variables with sensible defaults
5. **Health Checks**: Implement both liveness and readiness probes
6. **Graceful Shutdown**: Handle SIGTERM signals properly
7. **Resource Limits**: Set appropriate memory/CPU limits
8. **Secrets Management**: Never hardcode credentials
9. **Observability**: Add metrics and tracing
10. **Testing**: Write tests before deploying

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dapr Documentation](https://docs.dapr.io/)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
