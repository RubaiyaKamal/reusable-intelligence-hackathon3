---
name: local-k8s-deploy
description: Deploy applications to local Kubernetes (Kind, k3s, Minikube)
version: 1.0.0
author: Hackathon Team
tags: [kubernetes, kind, k3s, minikube, local, development]
---

# Local Kubernetes Deployment

## When to Use
- User asks to deploy to local Kubernetes
- Need to test K8s manifests locally
- Want K8s experience without cloud costs
- Docker Desktop K8s not available/insufficient

## What This Skill Does
Deploys applications to local Kubernetes clusters (Kind, k3s, or Minikube) with automatic cluster creation, infrastructure deployment, and application setup.

## Instructions

### 1. **Choose Platform and Deploy**
```bash
# Kind (Kubernetes in Docker) - Recommended for low memory
python scripts/deploy.py --platform kind

# k3s (Lightweight Kubernetes) - Fastest, most efficient
python scripts/deploy.py --platform k3s

# Minikube (Full Kubernetes) - Most features
python scripts/deploy.py --platform minikube --memory 3072
```

### 2. **Deploy Infrastructure**
```bash
python scripts/deploy_infrastructure.py
```

### 3. **Deploy Application**
```bash
python scripts/deploy_app.py --namespace storyforge
```

### 4. **Verify Deployment**
```bash
python scripts/verify.py --namespace storyforge
```

### 5. **Access Application**
```bash
python scripts/expose.py --namespace storyforge
```

## Platform Comparison

**Kind (Kubernetes in Docker)**:
- Memory: 2GB minimum
- Speed: Fast startup (~1 min)
- Best for: CI/CD, multi-node testing
- Pros: Lightweight, multi-node support
- Cons: Requires Docker

**k3s (Lightweight Kubernetes)**:
- Memory: 512MB minimum
- Speed: Very fast (~30 sec)
- Best for: Resource-constrained systems
- Pros: Smallest footprint, production-grade
- Cons: Some features simplified

**Minikube (Full Kubernetes)**:
- Memory: 2GB+ recommended
- Speed: Slower startup (~2-3 min)
- Best for: Full K8s feature testing
- Pros: Most complete, many drivers
- Cons: Higher resource usage

## Configuration

**Default Settings**:
- Cluster name: `storyforge-local`
- Namespace: `storyforge`
- Registry: Local registry (localhost:5000)
- LoadBalancer: MetalLB (for local LB)

## Validation Checklist
- [ ] Platform installed (kind/k3s/minikube)
- [ ] Cluster created and running
- [ ] kubectl configured
- [ ] Infrastructure deployed (Postgres, Kafka, Redis)
- [ ] Application pods running (backend, frontend)
- [ ] Services accessible
- [ ] Ingress working (if applicable)

## Expected Output
```
✓ Cluster created: storyforge-local (kind/k3s/minikube)
✓ kubectl configured
✓ Namespace: storyforge
✓ PostgreSQL: Running (1/1)
✓ Kafka: Running (1/1)
✓ Redis: Running (1/1)
✓ Backend: Running (2/2)
✓ Frontend: Running (2/2)

Access URLs:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Grafana: http://localhost:3001
```

See [REFERENCE.md](./REFERENCE.md) for troubleshooting and advanced configuration.
