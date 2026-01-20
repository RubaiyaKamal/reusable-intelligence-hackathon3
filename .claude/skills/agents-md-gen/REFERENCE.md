# AGENTS.MD Generator - Reference Documentation

## Overview
The AGENTS.md file is a structured documentation format designed specifically for AI coding agents. It provides context about repository structure, conventions, and workflows that enable agents to work autonomously.

## AGENTS.md Format Specification

### Required Sections

#### 1. Repository Overview
Brief description of the project, its purpose, and primary goals.

```markdown
# Repository Name

**Purpose**: Brief description of what this repository contains

**Type**: (e.g., Microservice, Frontend App, Library, Infrastructure)

**Primary Language**: (e.g., Python, TypeScript, Go)
```

#### 2. Directory Structure
Visual tree representation of important directories and files.

```markdown
## Directory Structure

```
/
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── scripts/          # Automation scripts
└── .claude/          # Claude Code skills
```
```

#### 3. Technology Stack
List all major technologies, frameworks, and tools used.

```markdown
## Technology Stack

- **Runtime**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Message Queue**: Kafka
- **Containerization**: Docker
- **Orchestration**: Kubernetes
```

#### 4. Development Conventions
Coding standards, naming conventions, and best practices.

```markdown
## Development Conventions

### Code Style
- Follow PEP 8 for Python
- Use type hints
- Maximum line length: 100 characters

### Naming Conventions
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE

### Testing
- Unit tests required for all business logic
- Minimum 80% code coverage
- Integration tests for API endpoints
```

#### 5. Getting Started
Step-by-step instructions for setting up the development environment.

```markdown
## Getting Started

### Prerequisites
- Python 3.11+
- Docker Desktop
- kubectl

### Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start services: `docker-compose up -d`
4. Run migrations: `python scripts/migrate.py`
5. Run tests: `pytest`
```

#### 6. Common Tasks
Frequently performed development tasks with exact commands.

```markdown
## Common Tasks

### Run Development Server
```bash
uvicorn main:app --reload --port 8000
```

### Run Tests
```bash
pytest tests/ -v --cov=src
```

### Build Docker Image
```bash
docker build -t app-name:latest .
```

### Deploy to Kubernetes
```bash
kubectl apply -f k8s/
```
```

#### 7. Architecture Decisions
Key architectural choices and rationale.

```markdown
## Architecture Decisions

### Event-Driven Architecture
We use Kafka for asynchronous communication between services to ensure loose coupling and scalability.

### Stateless Services
All services are designed to be stateless, storing state in PostgreSQL or Redis, enabling horizontal scaling.

### API Gateway Pattern
Kong API Gateway handles authentication, rate limiting, and routing to microservices.
```

## Best Practices

### For AI Agents Reading AGENTS.md

1. **Always read AGENTS.md first** before making changes to a repository
2. **Follow conventions** specified in the file
3. **Use exact commands** provided for common tasks
4. **Reference architecture decisions** when making design choices

### For Humans Writing AGENTS.md

1. **Keep it concise** - agents have token limits
2. **Be prescriptive** - provide exact commands, not descriptions
3. **Update regularly** - keep in sync with actual codebase
4. **Include examples** - show, don't just tell
5. **Link to deeper docs** - use AGENTS.md as an index

## Example AGENTS.md

```markdown
# LearnFlow Triage Service

**Purpose**: AI-powered query routing service that directs student questions to specialized tutoring agents

**Type**: Microservice (FastAPI + Dapr)

**Primary Language**: Python 3.11

## Directory Structure

```
/
├── src/
│   ├── main.py              # FastAPI application
│   ├── agents/              # AI agent implementations
│   ├── models/              # Pydantic models
│   └── services/            # Business logic
├── tests/
│   ├── unit/
│   └── integration/
├── k8s/                     # Kubernetes manifests
├── .claude/skills/          # Reusable skills
└── scripts/                 # Deployment scripts
```

## Technology Stack

- **Runtime**: Python 3.11
- **Framework**: FastAPI 0.104
- **AI SDK**: OpenAI Agents SDK
- **Service Mesh**: Dapr 1.12
- **Database**: PostgreSQL (via Dapr state store)
- **Messaging**: Kafka (via Dapr pub/sub)
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Development Conventions

### Code Style
- PEP 8 compliance (enforced by black and flake8)
- Type hints required for all functions
- Docstrings in Google style

### Agent Patterns
- Each agent in `src/agents/` implements `BaseAgent` interface
- Use dependency injection for agent selection
- All agent calls must be async

### API Endpoints
- RESTful conventions
- `/health` for liveness/readiness probes
- `/api/v1/*` for versioned APIs

### Testing
- Minimum 80% coverage
- Mock external dependencies (Dapr, Kafka)
- Use pytest fixtures for agent instances

## Getting Started

### Prerequisites
- Python 3.11+
- Docker Desktop
- Minikube running
- Dapr CLI installed

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start local Dapr sidecar
dapr run --app-id triage-service --app-port 8000 --dapr-http-port 3500

# Run application
uvicorn src.main:app --reload --port 8000
```

### Run Tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## Common Tasks

### Deploy to Kubernetes
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### View Logs
```bash
kubectl logs -f deployment/triage-service -n learnflow
```

### Test Agent Routing
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do for loops work?", "student_id": "123"}'
```

## Architecture Decisions

### Multi-Agent System
We use specialized agents (Concepts, Debug, Exercise) instead of a monolithic AI to provide focused, high-quality responses.

### Dapr for Service Mesh
Dapr provides language-agnostic pub/sub, state management, and service invocation, avoiding vendor lock-in.

### Asynchronous Processing
All agent calls are async to handle high concurrency and prevent blocking.

## Environment Variables

```bash
OPENAI_API_KEY=sk-...          # Required for AI agents
DAPR_HTTP_PORT=3500            # Dapr sidecar port
POSTGRES_CONN_STRING=...       # Database connection
KAFKA_BROKERS=kafka:9092       # Message broker
```

## Related Documentation
- [API Documentation](./docs/api.md)
- [Agent Design](./docs/agents.md)
- [Deployment Guide](./docs/deployment.md)
```

## Script Integration

The `generate_agents_md.py` script automates AGENTS.md creation by:

1. **Analyzing Repository**
   - Scans directory structure
   - Identifies tech stack from dependency files
   - Extracts conventions from linters/formatters

2. **Template Population**
   - Uses predefined templates for each section
   - Injects discovered data
   - Formats output as markdown

3. **Validation**
   - Checks all required sections present
   - Validates markdown syntax
   - Ensures file paths are accurate

## Token Efficiency

AGENTS.md should be concise (~2000-3000 tokens) to avoid consuming agent context. Use:
- **Bullet points** over paragraphs
- **Code blocks** over explanations
- **Links** to deeper documentation
- **Tables** for structured data

## Maintenance

Update AGENTS.md when:
- Adding new services/modules
- Changing tech stack
- Updating conventions
- Modifying deployment process
- Making architectural decisions
