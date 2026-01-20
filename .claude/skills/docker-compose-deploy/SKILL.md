---
name: docker-compose-deploy
description: Deploy multi-service applications using Docker Compose with health checks
version: 1.0.0
author: Hackathon Team
tags: [docker, docker-compose, deployment, microservices]
---

# Docker Compose Deployment

## When to Use
- User asks to deploy application stack with Docker Compose
- Need to orchestrate multiple containers locally
- Setting up development or staging environment
- Requires PostgreSQL, Kafka, Redis, and monitoring

## What This Skill Does
Deploys a complete application stack using Docker Compose, including backend services, databases, message queues, caching, and monitoring infrastructure.

## Instructions

1. **Deploy Full Stack**
   ```bash
   python scripts/deploy.py --file docker-compose.production.yml
   ```

2. **Verify All Services**
   ```bash
   python scripts/verify.py
   ```

3. **Check Service Health**
   ```bash
   python scripts/health_check.py
   ```

4. **View Service Logs**
   ```bash
   python scripts/logs.py --service <service-name>
   ```

5. **Stop All Services**
   ```bash
   python scripts/stop.py
   ```

## Configuration

The deployment includes:
- **Backend**: FastAPI with AI agents (Port 8001)
- **Frontend**: Next.js UI (Port 3002)
- **PostgreSQL**: Database (Port 5432)
- **Kafka**: Event streaming (Port 9092/9093)
- **Redis**: Caching (Port 6379)
- **Prometheus**: Metrics (Port 9090)
- **Grafana**: Dashboards (Port 3000)

## Validation Checklist
- [ ] All containers running
- [ ] Health checks passing
- [ ] Database initialized with schema
- [ ] Kafka topics created
- [ ] Backend API responding
- [ ] Frontend accessible
- [ ] Prometheus scraping metrics
- [ ] Grafana connected to Prometheus

## Expected Output
```
✓ PostgreSQL: Running (healthy)
✓ Kafka: Running (healthy)
✓ Backend: Running (healthy)
✓ Frontend: Running (healthy)
✓ Redis: Running (healthy)
✓ Prometheus: Running
✓ Grafana: Running

Access URLs:
- Frontend: http://localhost:3002
- Backend API: http://localhost:8001/docs
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
```

See [REFERENCE.md](./REFERENCE.md) for advanced configuration and troubleshooting.
