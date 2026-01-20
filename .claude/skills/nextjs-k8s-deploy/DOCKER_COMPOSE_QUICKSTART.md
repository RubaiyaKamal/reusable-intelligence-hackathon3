# Docker Compose Quick Start Guide

## Solving Docker Desktop Memory & Space Issues

This guide helps you use Docker Compose efficiently while managing memory and disk space.

## 🚀 Quick Setup

### 1. Generate Configuration

```bash
cd your-nextjs-app
python ../scripts/generate_docker_compose.py --app-name myapp --postgres --redis
```

This creates:
- `docker-compose.yml` - Production configuration
- `docker-compose.dev.yml` - Development with hot reload
- `Dockerfile.dev` - Development Dockerfile
- `.env.local.template` - Environment variables template
- `Makefile` - Convenient command shortcuts

### 2. Configure Environment

```bash
cp .env.local.template .env.local
# Edit .env.local with your actual values
```

### 3. Start Development

```bash
# Option A: Using make
make dev

# Option B: Using docker-compose directly
docker-compose -f docker-compose.dev.yml up
```

Your app will be available at http://localhost:3000

### 4. Start Production

```bash
make build    # Build all images
make up       # Start services in background
make logs     # View logs
```

## 💾 Managing Memory & Space

### Check Current Usage

```bash
python ../scripts/docker_cleanup.py --info
```

Output:
```
📊 Docker Disk Usage:
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          15        5         5.2GB     3.1GB (59%)
Containers      8         3         120MB     45MB (37%)
Local Volumes   5         2         850MB     420MB (49%)
Build Cache     25        0         1.8GB     1.8GB (100%)
```

### Quick Cleanup

```bash
# Remove stopped containers, dangling images, unused volumes
make prune

# Or use cleanup script with more control
python ../scripts/docker_cleanup.py --cleanup
```

### Aggressive Cleanup (When Running Low on Space)

```bash
# ⚠️  WARNING: Removes ALL unused images (including stopped containers' images)
python ../scripts/docker_cleanup.py --cleanup --aggressive
```

This will remove:
- All stopped containers
- All dangling images
- All unused images (even from stopped containers)
- All unused volumes
- All build cache

### Regular Maintenance

Run this weekly to keep Docker healthy:
```bash
make prune
```

## 🔧 Resource Limits

All services have memory limits to prevent Docker from consuming too much RAM:

| Service | Memory Limit | CPU Limit |
|---------|--------------|-----------|
| Next.js | 512MB | 1.0 |
| PostgreSQL | 256MB | 0.5 |
| Redis | 128MB | 0.25 |

Total maximum: ~900MB RAM

## 📋 Useful Commands

### Development

```bash
make dev          # Start dev server with hot reload
make dev-build    # Rebuild and start dev
make shell        # Open shell in container
make logs         # View logs
```

### Production

```bash
make build        # Build images
make up           # Start services
make down         # Stop services
make restart      # Restart services
make ps           # List running containers
make stats        # Show resource usage
```

### Cleanup

```bash
make clean        # Stop and remove volumes
make prune        # Remove all unused Docker data
```

### Monitoring

```bash
make stats        # Real-time resource usage
make logs         # View application logs
```

## 🐛 Troubleshooting

### Problem: Docker Desktop Using Too Much Memory

**Solution 1: Check what's running**
```bash
make stats
```

**Solution 2: Reduce limits in docker-compose.yml**
```yaml
deploy:
  resources:
    limits:
      memory: 256M  # Reduce from 512M
```

**Solution 3: Restart with Resource Saver**
- Docker Desktop → Settings → General → Enable "Resource Saver"

### Problem: Disk Space Full

**Solution 1: Quick cleanup**
```bash
make prune
```

**Solution 2: List large images**
```bash
python ../scripts/docker_cleanup.py --list
```

**Solution 3: Remove specific images**
```bash
docker rmi <image-name>:<tag>
```

**Solution 4: Aggressive cleanup**
```bash
python ../scripts/docker_cleanup.py --cleanup --aggressive
```

### Problem: Logs Taking Too Much Space

Logs are automatically limited in docker-compose.yml:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"    # 10MB per file
    max-file: "3"      # Keep 3 files max
```

Total: Maximum 30MB per container

### Problem: Build Cache Growing

```bash
# View build cache
docker buildx du

# Remove build cache
docker builder prune -af
```

### Problem: Container Won't Start

**Check logs:**
```bash
make logs
# or
docker-compose logs <service-name>
```

**Check resource limits:**
```bash
make stats
```

**Increase memory if needed:**
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 1G  # Increase if app needs more
```

## 🎯 Optimization Tips

### 1. Use .dockerignore

Create `.dockerignore`:
```
node_modules
.next
.git
*.log
.env.local
```

### 2. Multi-stage Builds

Already implemented in generated Dockerfile:
- Stage 1: Dependencies (cached)
- Stage 2: Build
- Stage 3: Runtime (minimal)

Result: 1GB → 150MB

### 3. Regular Cleanup Schedule

Add to your routine:
```bash
# Weekly
make prune

# Monthly
python ../scripts/docker_cleanup.py --cleanup --aggressive
```

### 4. Monitor Resource Usage

```bash
# Check periodically
make stats

# Set up alerts if usage is high
```

### 5. Docker Desktop Settings

Optimize Docker Desktop:
1. **Settings → Resources → Memory**: Set to 4GB (adjust based on needs)
2. **Settings → Resources → Disk**: Set reasonable limit
3. **Settings → General → Resource Saver**: Enable
4. **Settings → Docker Engine**: Add config:
   ```json
   {
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "10m",
       "max-file": "3"
     }
   }
   ```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Next.js Docker Documentation](https://nextjs.org/docs/deployment#docker-image)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🆘 Getting Help

If you encounter issues:

1. Check Docker status:
   ```bash
   docker info
   ```

2. View detailed logs:
   ```bash
   docker-compose logs --tail=100
   ```

3. Restart Docker Desktop

4. Clean everything and start fresh:
   ```bash
   make clean
   make prune
   make build
   make up
   ```
