---
name: fastapi-dapr-agent
description: Create FastAPI microservices with Dapr sidecar and AI agent integration
version: 1.0.0
author: Hackathon Team
tags: [fastapi, dapr, microservices, ai-agents]
---

# FastAPI + Dapr + Agent Microservice

## When to Use
- Creating AI-powered microservices
- Building event-driven FastAPI applications
- Need Dapr pub/sub or state management
- Integrating OpenAI Agents SDK with Kubernetes

## What This Skill Does
Generates a complete FastAPI microservice template with:
- Dapr sidecar configuration
- OpenAI Agents SDK integration
- Pub/sub messaging patterns
- State management via Dapr
- Kubernetes deployment manifests
- Health check endpoints

## Instructions

1. **Generate Service Template**
   ```bash
   python scripts/generate_service.py --name triage-service --port 8000
   ```

2. **Add AI Agent Logic**
   ```bash
   python scripts/add_agent.py --agent-type concepts --service triage-service
   ```

3. **Deploy to Kubernetes**
   ```bash
   ./scripts/deploy_service.sh triage-service
   ```

4. **Test Service**
   ```bash
   python scripts/test_service.py triage-service
   ```

## Service Structure
```
triage-service/
├── src/
│   ├── main.py              # FastAPI app
│   ├── agents/              # AI agent implementations
│   ├── models/              # Pydantic models
│   └── services/            # Business logic
├── k8s/                     # Kubernetes manifests
├── tests/                   # Unit & integration tests
└── requirements.txt
```

## Validation Checklist
- [ ] FastAPI app starts successfully
- [ ] Dapr sidecar attached
- [ ] Health endpoint responds
- [ ] Pub/sub messages flow
- [ ] Agent responses generated

See [REFERENCE.md](./REFERENCE.md) for agent patterns and Dapr configuration.
