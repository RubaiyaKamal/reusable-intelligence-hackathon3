---
name: nextjs-k8s-deploy
description: Deploy Next.js applications to Kubernetes or Docker Compose with optimized builds
version: 1.0.0
author: Hackathon Team
tags: [nextjs, kubernetes, docker-compose, frontend, deployment]
---

# Next.js Kubernetes & Docker Compose Deployment

## When to Use
- Deploying Next.js applications to Kubernetes or Docker
- Need containerized frontend with SSR support
- Want optimized Docker builds for Next.js
- Managing memory and disk space with Docker Desktop
- Setting up production-ready Next.js infrastructure

## What This Skill Does
Creates production-optimized Next.js deployments with:
- Multi-stage Docker builds (~150MB vs 1GB+)
- Docker Compose with resource limits
- Static asset caching
- Environment variable injection
- Horizontal pod autoscaling (Kubernetes)
- Memory and disk space management

## Instructions

### Option A: Docker Compose (Recommended for Development)

1. **Generate Docker Compose Configuration**
   ```bash
   python scripts/generate_docker_compose.py --app-name frontend --postgres --redis
   ```

2. **Setup Environment**
   ```bash
   cp .env.local.template .env.local
   # Edit .env.local with your values
   ```

3. **Start Services**
   ```bash
   make build    # Build images
   make up       # Start services
   make logs     # View logs
   ```

4. **Development with Hot Reload**
   ```bash
   make dev      # Start dev server
   ```

5. **Cleanup (if space/memory issues)**
   ```bash
   python scripts/docker_cleanup.py --cleanup
   make prune    # Remove unused data
   ```

### Option B: Kubernetes Deployment

1. **Generate Dockerfile**
   ```bash
   python scripts/generate_dockerfile.py --app-dir ./frontend
   ```

2. **Create Kubernetes Manifests**
   ```bash
   python scripts/generate_k8s_manifests.py --app frontend --port 3000
   ```

3. **Build and Push Image**
   ```bash
   ./scripts/build_and_push.sh frontend
   ```

4. **Deploy to Cluster**
   ```bash
   kubectl apply -f k8s/frontend/
   ```

5. **Verify Deployment**
   ```bash
   python scripts/verify_deployment.py frontend
   ```

## Generated Files
```
frontend/
├── Dockerfile               # Multi-stage optimized build
├── .dockerignore
├── k8s/
│   ├── deployment.yaml      # Next.js deployment
│   ├── service.yaml         # ClusterIP service
│   ├── ingress.yaml         # External access
│   └── hpa.yaml             # Auto-scaling
└── .env.production          # Environment variables
```

## Dockerfile Optimization
- **Stage 1**: Dependencies (cached layer)
- **Stage 2**: Build (generates .next/)
- **Stage 3**: Production (minimal runtime)
- Final size: ~150MB (vs 1GB+ unoptimized)

## Docker Desktop Memory/Space Management

**Common Issues:**
- Docker Desktop using too much memory
- Disk space running out
- Build cache consuming storage

**Solutions:**

1. **Check Current Usage**
   ```bash
   python scripts/docker_cleanup.py --info
   ```

2. **List What Can Be Cleaned**
   ```bash
   python scripts/docker_cleanup.py --list
   ```

3. **Cleanup Unused Resources**
   ```bash
   python scripts/docker_cleanup.py --cleanup
   # or
   make prune
   ```

4. **Aggressive Cleanup** (removes ALL unused images)
   ```bash
   python scripts/docker_cleanup.py --cleanup --aggressive
   ```

5. **Optimization Tips**
   ```bash
   python scripts/docker_cleanup.py --optimize-tips
   ```

**Resource Limits in docker-compose.yml:**
- Next.js: 512MB RAM, 1 CPU
- PostgreSQL: 256MB RAM, 0.5 CPU
- Redis: 128MB RAM, 0.25 CPU
- Logs: Limited to 30MB (3 files × 10MB)

## Validation Checklist
- [ ] Docker image builds successfully
- [ ] Image size < 200MB
- [ ] Containers start with resource limits
- [ ] Health checks pass
- [ ] Application accessible at http://localhost:3000
- [ ] Static assets load correctly
- [ ] Memory usage under limits

## Expected Output

**Docker Compose:**
```
✓ Created docker-compose.yml
✓ Created docker-compose.dev.yml
✓ Created Dockerfile.dev
✓ Created .env.local.template
✓ Created Makefile

Next.js: 512MB RAM, 1 CPU
PostgreSQL: 256MB RAM, 0.5 CPU
Redis: 128MB RAM, 0.25 CPU
```

**Cleanup:**
```
✓ Stopped containers removed
✓ Dangling images removed
✓ Unused volumes removed
✓ Build cache removed
Reclaimed: 2.5GB
```

See [REFERENCE.md](./REFERENCE.md) for performance tuning and advanced configuration.
