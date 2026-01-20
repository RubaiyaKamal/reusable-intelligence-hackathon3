#!/usr/bin/env python3
"""
Generate Docker Compose Configuration for Next.js

Creates an optimized docker-compose.yml with memory limits and volume management.
"""

import sys
import argparse
from pathlib import Path


def generate_docker_compose(
    app_name: str = "frontend",
    include_postgres: bool = False,
    include_redis: bool = False
) -> str:
    """Generate docker-compose.yml with resource limits"""

    compose_content = f'''version: '3.8'

services:
  # Next.js Frontend Service
  {app_name}:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    image: {app_name}:latest
    container_name: {app_name}
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - HOSTNAME=0.0.0.0
      # Add your environment variables here
      - NEXT_PUBLIC_API_URL=${{NEXT_PUBLIC_API_URL:-http://localhost:8000}}
    env_file:
      - .env.local
    # Resource limits to prevent memory issues
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    # Health check
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    # Restart policy
    restart: unless-stopped
    # Logging to prevent disk space issues
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - app-network
'''

    # Add PostgreSQL if requested
    if include_postgres:
        compose_content += f'''
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: {app_name}-postgres
    environment:
      - POSTGRES_USER=${{POSTGRES_USER:-postgres}}
      - POSTGRES_PASSWORD=${{POSTGRES_PASSWORD:-password}}
      - POSTGRES_DB=${{POSTGRES_DB:-{app_name}_db}}
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      # Limit PostgreSQL memory
      - type: tmpfs
        target: /dev/shm
        tmpfs:
          size: 256M
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - app-network
'''

    # Add Redis if requested
    if include_redis:
        compose_content += f'''
  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: {app_name}-redis
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 128M
        reservations:
          cpus: '0.1'
          memory: 64M
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - app-network
'''

    # Networks section
    compose_content += '''
networks:
  app-network:
    driver: bridge
'''

    # Volumes section
    volumes = []
    if include_postgres:
        volumes.append("postgres-data")
    if include_redis:
        volumes.append("redis-data")

    if volumes:
        compose_content += "\nvolumes:\n"
        for volume in volumes:
            compose_content += f"  {volume}:\n    driver: local\n"

    return compose_content


def generate_env_template() -> str:
    """Generate .env.local template"""

    return '''# Next.js Environment Variables
# Copy this to .env.local and fill in your values

# Node Environment
NODE_ENV=production

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
API_SECRET_KEY=your-secret-key-here

# Database (if using PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=frontend_db
DATABASE_URL=postgresql://postgres:your-secure-password@postgres:5432/frontend_db

# Redis (if using Redis)
REDIS_URL=redis://redis:6379

# Session
SESSION_SECRET=your-session-secret-here

# Optional: External Services
# OPENAI_API_KEY=sk-...
# STRIPE_SECRET_KEY=sk_test_...
'''


def generate_docker_compose_dev(app_name: str = "frontend") -> str:
    """Generate docker-compose for development with hot reload"""

    return f'''version: '3.8'

services:
  # Next.js Development Server
  {app_name}-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
      target: development
    image: {app_name}:dev
    container_name: {app_name}-dev
    ports:
      - "3000:3000"
    volumes:
      # Mount source code for hot reload
      - .:/app
      - /app/node_modules
      - /app/.next
    environment:
      - NODE_ENV=development
      - WATCHPACK_POLLING=true
    env_file:
      - .env.local
    # Lower resource limits for dev
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - dev-network
    command: npm run dev

networks:
  dev-network:
    driver: bridge
'''


def generate_dockerfile_dev() -> str:
    """Generate Dockerfile for development"""

    return '''# Development Dockerfile with hot reload
FROM node:18-alpine AS development

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Expose port
EXPOSE 3000

# Start dev server
CMD ["npm", "run", "dev"]
'''


def generate_makefile(app_name: str) -> str:
    """Generate Makefile for common Docker Compose commands"""

    return f'''# Makefile for {app_name} Docker Compose

.PHONY: help build up down restart logs clean prune dev

help: ## Show this help message
\t@echo 'Usage: make [target]'
\t@echo ''
\t@echo 'Available targets:'
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {{FS = ":.*?## "}}; {{printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}}'

build: ## Build Docker images
\tdocker-compose build

up: ## Start services in detached mode
\tdocker-compose up -d

down: ## Stop and remove containers
\tdocker-compose down

restart: ## Restart services
\tdocker-compose restart

logs: ## View logs
\tdocker-compose logs -f

ps: ## List running containers
\tdocker-compose ps

clean: ## Stop containers and remove volumes
\tdocker-compose down -v

prune: ## Remove unused Docker data
\tdocker system prune -af --volumes

dev: ## Start development environment
\tdocker-compose -f docker-compose.dev.yml up

dev-build: ## Build and start development
\tdocker-compose -f docker-compose.dev.yml up --build

stats: ## Show container resource usage
\tdocker stats

shell: ## Open shell in frontend container
\tdocker-compose exec {app_name} sh

# Production commands
prod-up: ## Start production environment
\tdocker-compose -f docker-compose.yml up -d

prod-logs: ## View production logs
\tdocker-compose -f docker-compose.yml logs -f
'''


def main():
    parser = argparse.ArgumentParser(
        description="Generate Docker Compose configuration for Next.js"
    )
    parser.add_argument(
        "--app-name",
        default="frontend",
        help="Application name (default: frontend)"
    )
    parser.add_argument(
        "--postgres",
        action="store_true",
        help="Include PostgreSQL service"
    )
    parser.add_argument(
        "--redis",
        action="store_true",
        help="Include Redis service"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        print("🚀 Generating Docker Compose configuration...")
        print()

        # Generate production docker-compose.yml
        compose_content = generate_docker_compose(
            app_name=args.app_name,
            include_postgres=args.postgres,
            include_redis=args.redis
        )
        compose_path = output_dir / "docker-compose.yml"
        compose_path.write_text(compose_content)
        print(f"✓ Created {compose_path}")

        # Generate development docker-compose
        compose_dev_content = generate_docker_compose_dev(args.app_name)
        compose_dev_path = output_dir / "docker-compose.dev.yml"
        compose_dev_path.write_text(compose_dev_content)
        print(f"✓ Created {compose_dev_path}")

        # Generate Dockerfile.dev
        dockerfile_dev_content = generate_dockerfile_dev()
        dockerfile_dev_path = output_dir / "Dockerfile.dev"
        dockerfile_dev_path.write_text(dockerfile_dev_content)
        print(f"✓ Created {dockerfile_dev_path}")

        # Generate .env.local template
        env_content = generate_env_template()
        env_path = output_dir / ".env.local.template"
        env_path.write_text(env_content)
        print(f"✓ Created {env_path}")

        # Generate Makefile
        makefile_content = generate_makefile(args.app_name)
        makefile_path = output_dir / "Makefile"
        makefile_path.write_text(makefile_content)
        print(f"✓ Created {makefile_path}")

        print()
        print("📋 Configuration Summary:")
        print(f"  App Name: {args.app_name}")
        print(f"  PostgreSQL: {'✓' if args.postgres else '✗'}")
        print(f"  Redis: {'✓' if args.redis else '✗'}")
        print()
        print("🔧 Resource Limits:")
        print(f"  Next.js: 512MB RAM, 1 CPU")
        if args.postgres:
            print(f"  PostgreSQL: 256MB RAM, 0.5 CPU")
        if args.redis:
            print(f"  Redis: 128MB RAM, 0.25 CPU")
        print()
        print("📦 Next steps:")
        print(f"  1. cd {output_dir}")
        print("  2. cp .env.local.template .env.local")
        print("  3. Edit .env.local with your values")
        print()
        print("🚀 Quick Start:")
        print("  Production:")
        print("    make build    # Build images")
        print("    make up       # Start services")
        print("    make logs     # View logs")
        print()
        print("  Development:")
        print("    make dev      # Start dev server with hot reload")
        print()
        print("💾 Memory Management:")
        print("  make prune    # Clean up unused Docker data")
        print("  make stats    # Monitor resource usage")
        print()
        print("⚠️  Remember:")
        print("  - All logs are limited to 30MB (3 files × 10MB)")
        print("  - Containers have memory limits to prevent issues")
        print("  - Volumes persist data across restarts")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
