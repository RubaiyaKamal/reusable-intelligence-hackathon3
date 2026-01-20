# AGENTS.md - StoryForge Project

> AI Agent Guide for StoryForge - AI-Powered Children's Reading Platform

---

## 📋 Repository Overview

**Project**: StoryForge
**Type**: AI-Powered Educational Platform
**Purpose**: Multi-agent children's reading comprehension and literacy platform

StoryForge is a production-ready application built using **Skills-based development** following Hackathon III: Reusable Intelligence guidelines. The project demonstrates the **MCP Code Execution pattern** with token-efficient autonomous deployment.

---

## 🏗️ Directory Structure

```
reusable-intelligence-hackathon3/
├── .claude/                      # Skills library (MCP Code Execution pattern)
│   ├── skills/
│   │   ├── agents-md-gen/       # Generate AGENTS.md files
│   │   ├── docker-compose-deploy/ # Deploy with Docker Compose
│   │   ├── kafka-k8s-setup/     # Kafka deployment
│   │   ├── postgres-k8s-setup/  # PostgreSQL deployment
│   │   ├── fastapi-dapr-agent/  # FastAPI + Dapr services
│   │   ├── nextjs-k8s-deploy/   # Next.js deployment
│   │   ├── prometheus-grafana-setup/ # Monitoring
│   │   └── [25+ other skills]/  # Education-specific skills
│   └── commands/                # Command definitions
├── backend/                     # FastAPI backend with AI agents
│   ├── src/
│   │   ├── agents/             # AI specialist agents
│   │   │   ├── router_agent.py        # Intent classification
│   │   │   ├── story_agent.py         # Story generation
│   │   │   ├── vocabulary_agent.py    # Word definitions
│   │   │   └── comprehension_agent.py # Q&A
│   │   ├── routers/            # API endpoints
│   │   ├── services/           # Business logic
│   │   ├── models/             # Pydantic models
│   │   ├── config.py           # Configuration
│   │   └── main.py             # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js 14 app directory
│   ├── components/            # React components
│   ├── public/                # Static assets
│   ├── Dockerfile
│   └── package.json
├── k8s/                        # Kubernetes deployment files
│   ├── deploy-postgres.sh     # PostgreSQL K8s deployment
│   ├── deploy-kafka.sh        # Kafka K8s deployment
│   ├── deploy-monitoring.sh   # Prometheus/Grafana deployment
│   ├── storyforge-schema.sql  # Database schema
│   └── create-kafka-topics.sh # Kafka topics initialization
├── monitoring/                 # Monitoring configuration
│   ├── prometheus.yml         # Prometheus config
│   └── grafana/
│       ├── dashboards/        # Grafana dashboards
│       └── datasources/       # Data source configs
├── history/                    # Prompt History Records (PHR)
│   ├── prompts/
│   │   ├── general/          # General prompts
│   │   └── [feature-name]/   # Feature-specific prompts
│   └── adr/                   # Architecture Decision Records
├── .specify/                   # Spec-Kit Plus framework
│   ├── templates/             # Specification templates
│   ├── scripts/               # Helper scripts
│   └── memory/
│       └── constitution.md    # Project principles
├── docker-compose.yml          # Simple development setup
├── docker-compose.production.yml # Full production stack
├── .env                        # Environment variables
├── PROJECT_DESIGN.md           # Architecture overview
├── DEPLOYMENT_COMPLETE.md      # Deployment documentation
└── AGENTS.md                   # This file

```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **AI/ML**: OpenAI GPT-4 (openai 1.3.0)
- **Database**: PostgreSQL 14+ (psycopg2-binary)
- **Message Queue**: Apache Kafka 7.5.0 (Confluent)
- **Cache**: Redis 7
- **Async**: Python asyncio
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Runtime**: Node 18-alpine
- **Package Manager**: npm
- **Styling**: Tailwind CSS
- **UI Components**: React 18

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (optional)
- **Package Manager**: Helm 3.x
- **Monitoring**: Prometheus + Grafana
- **Message Broker**: Kafka + Zookeeper
- **Storage**: Persistent Volumes

### Development Tools
- **AI Agents**: Claude Code, Goose
- **Pattern**: MCP Code Execution with Skills
- **Spec Framework**: Spec-Kit Plus
- **Version Control**: Git

---

## 📐 Development Conventions

### Code Style
- **Python**: PEP 8, Black formatter, type hints
- **TypeScript/JavaScript**: ESLint, Prettier
- **Imports**: Absolute imports preferred
- **Comments**: Docstrings for all public functions (Google style)

### Skills Development (MCP Code Execution Pattern)
All skills follow this structure:
```
.claude/skills/<skill-name>/
├── SKILL.md              # ~100 tokens - Minimal instructions
├── REFERENCE.md          # 0 tokens - Loaded on-demand
└── scripts/
    ├── deploy.py         # 0 tokens - Execution scripts
    ├── verify.py         # 0 tokens - Verification
    └── ...               # Additional helpers
```

**Key Principles**:
- SKILL.md contains only essential instructions (~100 tokens)
- Scripts execute outside agent context (0 tokens loaded)
- Only final results enter agent context (~10-50 tokens)
- **Token savings**: 99.7% reduction vs direct MCP

### API Development
- **Endpoints**: RESTful conventions
- **Versioning**: `/api/v1/` prefix
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Error Handling**: Consistent error responses with status codes
- **Health Checks**: `/health/live` and `/health/ready`

### Database
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Migrations**: Alembic (not currently implemented)
- **Naming**: snake_case for tables/columns
- **Primary Keys**: UUID preferred
- **Timestamps**: created_at, updated_at on all tables

### Git Workflow
- **Branches**: feature/*, bugfix/*, hotfix/*
- **Commits**: Conventional Commits format
  ```
  type(scope): description

  Claude: implemented feature using <skill-name> skill
  Goose: deployed service using <skill-name> skill
  ```
- **PRs**: Required for main branch

---

## 🚀 Getting Started

### Prerequisites
```bash
# Check installations
docker --version          # Docker 20+
docker-compose --version  # Docker Compose 2+
python --version         # Python 3.12+
node --version           # Node 18+
kubectl version          # Kubernetes client (optional)
helm version             # Helm 3.x (optional)
```

### Quick Start (Docker Compose)
```bash
# 1. Clone repository
git clone <repository-url>
cd reusable-intelligence-hackathon3

# 2. Set environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Deploy full stack using the skill
python .claude/skills/docker-compose-deploy/scripts/deploy.py --file docker-compose.production.yml

# 4. Verify deployment
python .claude/skills/docker-compose-deploy/scripts/verify.py

# 5. Check health
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

### Access Services
- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8001/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9091

---

## 🎯 Common Tasks

### Using Skills (MCP Code Execution Pattern)

#### Deploy PostgreSQL to Kubernetes
```bash
cd .claude/skills/postgres-k8s-setup
./scripts/deploy.sh
python scripts/verify.py
```

#### Deploy Kafka to Kubernetes
```bash
cd .claude/skills/kafka-k8s-setup
./scripts/deploy.sh
python scripts/verify.py
./scripts/create-topics.sh
```

#### Deploy Monitoring Stack
```bash
cd .claude/skills/prometheus-grafana-setup
./scripts/deploy.sh
python scripts/verify.py
```

#### Deploy Application with Docker Compose
```bash
# From project root
python .claude/skills/docker-compose-deploy/scripts/deploy.py --file docker-compose.production.yml --build
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

### Backend Development
```bash
# Run backend locally
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000

# Test agents
python test_router.py
python test_story_agent.py

# View logs
docker logs storyforge-backend -f
```

### Frontend Development
```bash
# Run frontend locally
cd frontend
npm install
npm run dev

# Build for production
npm run build

# View logs
docker logs storyforge-frontend -f
```

### Database Operations
```bash
# Access PostgreSQL
docker exec -it storyforge-postgres psql -U storyforge_user -d storyforge_db

# View tables
\dt

# View schema
\d students
\d stories

# Run custom query
SELECT * FROM students LIMIT 10;
```

### Kafka Operations
```bash
# List topics
docker exec -it storyforge-kafka kafka-topics --list --bootstrap-server localhost:9092

# Create topic
docker exec -it storyforge-kafka kafka-topics --create --topic test --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

# Consume messages
docker exec -it storyforge-kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic story.generated --from-beginning

# Produce messages
docker exec -it storyforge-kafka kafka-console-producer --bootstrap-server localhost:9092 --topic story.generated
```

### Monitoring
```bash
# View Prometheus targets
curl http://localhost:9091/api/v1/targets

# Query metrics
curl 'http://localhost:9091/api/v1/query?query=up'

# Access Grafana
open http://localhost:3001  # admin/admin
```

---

## 🏛️ Architecture Decisions

### 1. Skills-Based Development with MCP Code Execution
**Decision**: Use Skills with MCP Code Execution pattern instead of direct MCP server integration

**Rationale**:
- 99.7% reduction in token usage
- Scripts execute outside agent context
- Reusable across Claude Code, Goose, and Codex
- Industry standard format (SKILL.md)

**Trade-offs**:
- More upfront setup (create skills)
- Need to maintain scripts separate from instructions

### 2. Multi-Agent Architecture
**Decision**: 4 specialist agents (Router, Story, Vocabulary, Comprehension)

**Rationale**:
- Each agent focuses on specific domain
- Better prompt engineering per domain
- Easier to test and maintain
- Scalable horizontally

**Trade-offs**:
- More complex orchestration
- Router agent is single point of failure

### 3. Event-Driven with Kafka
**Decision**: Use Kafka for async communication between agents

**Rationale**:
- Decouples services
- Enables event replay
- Supports high throughput
- Built-in durability

**Trade-offs**:
- Added operational complexity
- Requires Zookeeper
- Learning curve

### 4. Docker Compose for Local, Kubernetes for Production
**Decision**: Provide both deployment options

**Rationale**:
- Docker Compose for easy local development
- Kubernetes for production scalability
- Skills work with both platforms

**Trade-offs**:
- Maintain two configurations
- Different behaviors possible

### 5. PostgreSQL for Data, Redis for Cache
**Decision**: Use PostgreSQL as primary database, Redis for caching

**Rationale**:
- PostgreSQL: ACID, complex queries, relationships
- Redis: Fast reads, session storage, rate limiting

**Trade-offs**:
- Two systems to monitor
- Data consistency challenges

---

## 📚 Key Files for AI Agents

### Configuration
- `.env` - Environment variables (OPENAI_API_KEY, DATABASE_URL)
- `backend/src/config.py` - Application configuration
- `monitoring/prometheus.yml` - Metrics configuration

### Schemas & Models
- `k8s/storyforge-schema.sql` - Database schema (8 tables + 3 views)
- `backend/src/models/requests.py` - API request models
- `backend/src/models/responses.py` - API response models

### Agent Implementations
- `backend/src/agents/router_agent.py` - 380 lines - Intent classification
- `backend/src/agents/story_agent.py` - 420 lines - Story generation
- `backend/src/agents/vocabulary_agent.py` - 380 lines - Definitions
- `backend/src/agents/comprehension_agent.py` - 360 lines - Q&A

### Skills (25+ Skills Available)
All skills follow MCP Code Execution pattern:
- `agents-md-gen` - Generate AGENTS.md files
- `docker-compose-deploy` - Deploy with Docker Compose ⭐
- `kafka-k8s-setup` - Kafka deployment
- `postgres-k8s-setup` - PostgreSQL deployment
- `fastapi-dapr-agent` - FastAPI microservices
- `nextjs-k8s-deploy` - Next.js deployment
- `prometheus-grafana-setup` - Monitoring setup
- And 18+ more education-specific skills

---

## 🔒 Security Considerations

- OpenAI API keys stored in `.env` (never commit)
- PostgreSQL credentials auto-generated or environment-based
- CORS configured for frontend origin only
- Rate limiting (TODO in production)
- Input sanitization on API endpoints
- JWT authentication (TODO for production)

---

## 📊 Monitoring & Observability

### Metrics (Prometheus)
- Backend API response times
- Agent performance metrics
- Kafka consumer lag
- Database connection pool
- Redis cache hit rate

### Dashboards (Grafana)
- Application overview
- Agent performance
- Infrastructure health
- Kafka topics

### Logging
- Structured logging with timestamps
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized via Docker logs

---

## 🧪 Testing

### Backend Tests
```bash
python test_router.py         # Router agent tests
python test_story_agent.py    # Story agent tests
```

### Health Checks
```bash
curl http://localhost:8001/health/live
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

---

## 🤝 Contributing

### For Hackathon III Judges
- Review `.claude/skills/` for Skills implementation
- Check `DEPLOYMENT_COMPLETE.md` for deployment evidence
- Test skills: `python .claude/skills/<skill-name>/scripts/deploy.py`
- Verify token efficiency (SKILL.md ~100 tokens vs 50k+ direct MCP)

### Creating New Skills
1. Create directory: `.claude/skills/<skill-name>/`
2. Add `SKILL.md` with ~100 token instructions
3. Add `scripts/` with executable Python/Bash scripts
4. Add `REFERENCE.md` for detailed documentation
5. Test with: `python scripts/deploy.py`

---

## 📞 Support & Resources

### Documentation
- `PROJECT_DESIGN.md` - Architecture overview
- `DEPLOYMENT_COMPLETE.md` - Deployment guide
- `STORYFORGE_COMPLETE.md` - Implementation details
- `QUICK_START.md` - Quick start guide

### External Resources
- [Hackathon III Guidelines](hackathon-docs)
- [MCP Code Execution Pattern](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [AAIF Standards](https://aaif.io/)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Goose Documentation](https://block.github.io/goose/)

---

**Built with ❤️ for Hackathon III: Reusable Intelligence**

Following the MCP Code Execution pattern for token-efficient autonomous deployment.

**StoryForge** - Empowering children through AI-powered reading experiences 📚✨
