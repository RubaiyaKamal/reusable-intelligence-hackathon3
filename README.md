# StoryForge - AI-Powered Children's Reading Platform

> **Hackathon III: Reusable Intelligence & Cloud-Native Mastery**
>
> A production-ready educational platform built using **Skills-based development** with the **MCP Code Execution pattern**.

[![Docker Compose](https://img.shields.io/badge/docker--compose-ready-blue)](docker-compose.production.yml)
[![Kubernetes](https://img.shields.io/badge/kubernetes-ready-326CE5)](k8s/)
[![ArgoCD](https://img.shields.io/badge/argocd-gitops-orange)](k8s/argocd/)
[![Skills](https://img.shields.io/badge/skills-25+-green)](.claude/skills/)

---

## 🎯 Project Overview

**StoryForge** is an AI-powered children's reading comprehension and literacy platform featuring:

- 🤖 **4 Specialist AI Agents**: Router, Story, Vocabulary, Comprehension
- 📚 **Interactive Reading Experience**: Age-appropriate stories and exercises
- 👨‍🏫 **Teacher Dashboard**: Class management and progress tracking
- 📊 **Real-time Analytics**: Student engagement and mastery tracking
- ☁️ **Cloud-Native**: Kubernetes-ready with Docker Compose for local dev

---

## ⚡ Quick Start

### Local Development (Docker Compose)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd reusable-intelligence-hackathon3

# 2. Set environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Deploy using the skill (MCP Code Execution pattern)
python .claude/skills/docker-compose-deploy/scripts/deploy.py \
  --file docker-compose.production.yml

# 4. Verify deployment
python .claude/skills/docker-compose-deploy/scripts/verify.py

# 5. Check health
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

**Access**:
- Frontend: http://localhost:3002
- Backend API: http://localhost:8001/docs
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9091

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   KUBERNETES CLUSTER                    │
│  ┌────────────────────────────────────────────────┐    │
│  │              APPLICATION LAYER                  │    │
│  │  ┌──────────┐              ┌──────────┐        │    │
│  │  │ Frontend │◄────────────►│ Backend  │        │    │
│  │  │ Next.js  │   REST API   │ FastAPI  │        │    │
│  │  │  :3000   │              │  :8000   │        │    │
│  │  └──────────┘              └────┬─────┘        │    │
│  │                                  │              │    │
│  └──────────────────────────────────┼──────────────┘    │
│                                     │                   │
│  ┌──────────────────────────────────┼──────────────┐    │
│  │             DATA LAYER            ▼              │    │
│  │  ┌──────────┐ ┌────────┐ ┌────────────────┐    │    │
│  │  │PostgreSQL│ │ Redis  │ │ Kafka + ZK     │    │    │
│  │  │  :5432   │ │ :6379  │ │ :9092 / :2181  │    │    │
│  │  └──────────┘ └────────┘ └────────────────┘    │    │
│  └────────────────────────────────────────────────┘    │
│                                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │          MONITORING LAYER                      │    │
│  │  ┌───────────┐              ┌────────┐        │    │
│  │  │Prometheus │◄─────────────┤Grafana │        │    │
│  │  │  :9090    │  Datasource  │ :3000  │        │    │
│  │  └───────────┘              └────────┘        │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Multi-Agent Architecture

```
User Query
    │
    ▼
┌────────────────────┐
│   Router Agent     │  Intent Classification
│   Port 8001        │  Engagement Detection
└────────┬───────────┘
         │
    ┌────┴────┬────────┬───────────┐
    ▼         ▼        ▼           ▼
┌────────┐┌────────┐┌──────────┐┌──────────┐
│ Story  ││Vocab   ││Comprehen.││Progress  │
│ Agent  ││Agent   ││Agent     ││Agent     │
│ :8002  ││:8004   ││:8003     ││:8006     │
└────────┘└────────┘└──────────┘└──────────┘
    │         │        │           │
    └─────────┴────────┴───────────┘
              │
              ▼
       ┌─────────────┐
       │ Kafka Bus   │
       │ 8 Topics    │
       └─────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **AI**: OpenAI GPT-4 (openai 1.3.0)
- **Database**: PostgreSQL 14+
- **Cache**: Redis 7
- **Message Queue**: Apache Kafka 7.5.0

### Frontend
- **Framework**: Next.js 14
- **Runtime**: Node 18
- **Styling**: Tailwind CSS

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Orchestration**: Kubernetes
- **GitOps**: ArgoCD
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

### Development
- **AI Agents**: Claude Code, Goose
- **Pattern**: MCP Code Execution with Skills
- **Framework**: Spec-Kit Plus (SDD)

---

## 📚 Key Features

### For Students
- 📖 Interactive story reading with AI-generated content
- 🎯 Vocabulary building with contextual explanations
- 🧠 Comprehension exercises and quizzes
- 📈 Progress tracking and mastery levels
- 🏆 Achievements and reading streaks

### For Teachers
- 👥 Class management dashboard
- 📊 Student progress analytics
- ⚠️ Real-time struggle alerts
- 📝 Assignment creation and management
- 📧 Communication tools

### For Developers
- 🎯 **Skills-based Development**: 25+ reusable Skills
- 💰 **Token Efficiency**: 99.7% reduction vs direct MCP
- 🔄 **GitOps Ready**: ArgoCD + GitHub Actions
- 🐳 **Container Native**: Docker Compose + Kubernetes
- 📊 **Observable**: Prometheus + Grafana monitoring

---

## 🎓 Skills Library (MCP Code Execution Pattern)

This project demonstrates the **MCP Code Execution pattern** with **25+ reusable Skills**:

### Core Skills
- `docker-compose-deploy` - Deploy multi-service stacks
- `k8s-cloud-deploy` - Deploy to AWS/GCP/Azure/Oracle
- `kafka-k8s-setup` - Kafka deployment
- `postgres-k8s-setup` - PostgreSQL deployment
- `prometheus-grafana-setup` - Monitoring stack
- `argocd-app-deployment` - GitOps setup

### Development Skills
- `agents-md-gen` - Generate AGENTS.md files
- `fastapi-dapr-agent` - FastAPI microservices
- `nextjs-k8s-deploy` - Next.js deployment
- `mcp-code-execution` - MCP pattern implementation

### Education Skills (18+)
- `reading-basics` - Reading fundamentals
- `vocabulary-building` - Vocabulary exercises
- `story-comprehension` - Comprehension tests
- `creative-writing` - Writing exercises
- And 14+ more...

**Token Efficiency**:
- Traditional MCP: 50,000+ tokens loaded
- Skills approach: ~150 tokens total
- **Savings**: 99.7%

---

## 📁 Project Structure

```
reusable-intelligence-hackathon3/
├── .claude/skills/          # 25+ Skills (MCP Code Execution)
├── .github/workflows/       # CI/CD pipelines
├── backend/                 # FastAPI + AI agents
│   ├── src/agents/         # 4 specialist agents
│   ├── src/routers/        # API endpoints
│   └── src/services/       # Business logic
├── frontend/                # Next.js application
├── k8s/                     # Kubernetes manifests
│   ├── app/                # Application deployments
│   ├── argocd/             # ArgoCD configurations
│   ├── deploy-*.sh         # Infrastructure scripts
│   └── storyforge-schema.sql
├── monitoring/              # Prometheus + Grafana
├── history/prompts/         # Prompt History Records (PHR)
├── docker-compose.yml       # Simple dev setup
├── docker-compose.production.yml  # Full stack
├── AGENTS.md                # AI agent guide
├── DEPLOYMENT_COMPLETE.md   # Docker Compose deployment
├── CLOUD_DEPLOYMENT_GUIDE.md # Cloud deployment
└── README.md                # This file
```

---

## 🚀 Deployment Options

### Option 1: Docker Compose (Local/Development)

**Best for**: Local development, testing

```bash
# Deploy full stack
python .claude/skills/docker-compose-deploy/scripts/deploy.py \
  --file docker-compose.production.yml

# 8 services: Backend, Frontend, PostgreSQL, Kafka, Redis, Prometheus, Grafana, Zookeeper
```

**Cost**: $0 (runs locally)

### Option 2: Cloud Kubernetes (Production)

**Best for**: Production deployments

**AWS EKS**:
```bash
python .claude/skills/k8s-cloud-deploy/scripts/deploy.py \
  --provider aws \
  --cluster-name storyforge-prod \
  --region us-east-1
```
**Cost**: ~$165-200/month

**GCP GKE**:
```bash
python .claude/skills/k8s-cloud-deploy/scripts/deploy.py \
  --provider gcp \
  --cluster-name storyforge-prod \
  --region us-central1-a
```
**Cost**: ~$178-220/month

**Azure AKS**:
```bash
python .claude/skills/k8s-cloud-deploy/scripts/deploy.py \
  --provider azure \
  --cluster-name storyforge-prod \
  --region eastus
```
**Cost**: ~$180-230/month

**Oracle OKE** (Budget Option):
- **Cost**: ~$100-150/month
- **Free Tier**: 2 VMs + 200GB storage FREE forever

See [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md) for details.

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

**Triggered on**: Push to `main`, Pull Requests

**Pipeline Stages**:
1. ✅ **Build** - Backend & Frontend images
2. ✅ **Test** - Run test suites
3. ✅ **Security Scan** - Trivy vulnerability scanning
4. ✅ **Push** - Push images to GitHub Container Registry
5. ✅ **Deploy** - Update K8s manifests, ArgoCD syncs

### GitOps with ArgoCD

**Setup**:
```bash
python .claude/skills/k8s-cloud-deploy/scripts/setup_argocd.py
```

**Features**:
- Automated sync from Git repository
- Self-healing deployments
- Rollback support
- Multi-environment management

---

## 📊 Monitoring & Observability

### Metrics (Prometheus)
- API response times
- Agent performance
- Kafka consumer lag
- Database metrics
- Cache hit rates

### Dashboards (Grafana)
- Application overview
- Infrastructure health
- Agent performance
- Kafka topics

**Access Grafana**:
```bash
# Local
http://localhost:3001 (admin/admin)

# Kubernetes
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

---

## 🧪 Testing

```bash
# Backend tests
python test_router.py
python test_story_agent.py

# Health checks
curl http://localhost:8001/health/live

# Using skill
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

---

## 📖 Documentation

### For Users
- [Quick Start Guide](QUICK_START.md)
- [Project Design](PROJECT_DESIGN.md)
- [Skills Completion Summary](SKILLS_COMPLETION_SUMMARY.md)

### For Developers
- [AGENTS.md](AGENTS.md) - AI agent repository guide
- [Deployment Complete](DEPLOYMENT_COMPLETE.md) - Docker Compose deployment
- [Cloud Deployment Guide](CLOUD_DEPLOYMENT_GUIDE.md) - Cloud deployment
- [StoryForge Complete](STORYFORGE_COMPLETE.md) - Implementation details

### For Hackathon Judges
- **Skills Library**: `.claude/skills/` (25+ skills)
- **Token Efficiency**: DEPLOYMENT_COMPLETE.md (99.7% reduction)
- **Cloud Deployment**: CLOUD_DEPLOYMENT_GUIDE.md
- **CI/CD**: `.github/workflows/ci-cd.yaml`
- **GitOps**: `k8s/argocd/application.yaml`

---

## 🏆 Hackathon III Compliance

### Phase 9: Cloud Deployment ✅
- [x] Kubernetes manifests created
- [x] Cloud deployment skill (AWS/GCP/Azure/Oracle)
- [x] Skills-based MCP Code Execution pattern
- [x] Token efficiency (<200 tokens)

### Phase 10: Continuous Deployment ✅
- [x] GitHub Actions CI/CD pipeline
- [x] ArgoCD GitOps configuration
- [x] Automated builds and deployments
- [x] Multi-environment support

### Skills Autonomy ✅
- [x] 25+ Skills created
- [x] MCP Code Execution pattern
- [x] Scripts execute outside context
- [x] Zero manual intervention

### Token Efficiency ✅
- [x] SKILL.md: ~100 tokens
- [x] Scripts: 0 tokens (executed)
- [x] Results: ~50 tokens
- [x] Total: 99.7% reduction

### Documentation ✅
- [x] AGENTS.md for AI agent onboarding
- [x] Comprehensive deployment guides
- [x] Architecture diagrams
- [x] Prompt History Records (PHR)

---

## 🤝 Contributing

### Creating New Skills

```bash
# Create skill directory
mkdir -p .claude/skills/my-skill/scripts

# Create SKILL.md (~100 tokens)
# Create execution scripts (Python/Bash)
# Add REFERENCE.md for detailed docs

# Test
python .claude/skills/my-skill/scripts/deploy.py
```

See [AGENTS.md](AGENTS.md) for full guidelines.

---

## 🔒 Security

- ✅ Secrets management (Kubernetes Secrets)
- ✅ Environment variables (.env)
- ✅ CORS configuration
- ✅ Input validation
- ✅ Security scanning (Trivy)
- ⏳ JWT authentication (TODO for production)
- ⏳ Rate limiting (TODO for production)

---

## 💰 Cost Estimate

### Local Development
**Docker Compose**: $0 (runs on your machine)

### Cloud Production

| Provider | Configuration | Monthly Cost |
|----------|--------------|--------------|
| **AWS EKS** | 3x t3.medium nodes | $165-200 |
| **GCP GKE** | 3x n1-standard-2 nodes | $178-220 |
| **Azure AKS** | 3x Standard_D2s_v3 nodes | $180-230 |
| **Oracle OKE** ⭐ | 3x VM.Standard.E4.Flex | $100-150 |

**Recommended**: Oracle OKE for budget or AWS EKS for enterprise.

---

## 📞 Support

### Logs
```bash
# Docker Compose
docker logs storyforge-backend -f

# Kubernetes
kubectl logs -n storyforge deployment/storyforge-backend -f
```

### Database Access
```bash
# Docker Compose
docker exec -it storyforge-postgres psql -U storyforge_user -d storyforge_db

# Kubernetes
kubectl exec -it -n storyforge storyforge-postgres-0 -- psql -U storyforge_user -d storyforge_db
```

### Health Checks
```bash
# Backend
curl http://localhost:8001/health/live

# All services
python .claude/skills/docker-compose-deploy/scripts/health_check.py
```

---

## 📜 License

This project is created for **Hackathon III: Reusable Intelligence & Cloud-Native Mastery**.

---

## 🙏 Acknowledgments

- **Hackathon III** for the challenge
- **Anthropic** for Claude Code and MCP pattern
- **Agentic AI Foundation (AAIF)** for standards
- **OpenAI** for GPT-4 API

---

## 📊 Project Stats

- **Lines of Code**: ~10,000+
- **Skills Created**: 26
- **Services Deployed**: 8
- **API Endpoints**: 15+
- **Database Tables**: 8 (+ 3 views)
- **Kafka Topics**: 8
- **Token Reduction**: 99.7%

---

**Built with ❤️ for Hackathon III: Reusable Intelligence**

✅ Skills-based MCP Code Execution Pattern
✅ Token-efficient autonomous deployment
✅ Production-ready cloud-native architecture
✅ Complete CI/CD with GitOps

**StoryForge** - Empowering children through AI-powered reading experiences 📚✨

---

## 🚀 Get Started Now

```bash
# Clone and deploy in 3 commands
git clone <your-repo-url>
cd reusable-intelligence-hackathon3
python .claude/skills/docker-compose-deploy/scripts/deploy.py --file docker-compose.production.yml

# Access at http://localhost:3002
```

**Questions?** Check [AGENTS.md](AGENTS.md) or [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)
