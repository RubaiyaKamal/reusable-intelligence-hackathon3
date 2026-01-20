---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes using Helm with migration support
version: 1.0.0
author: Hackathon Team
tags: [postgresql, kubernetes, database, persistence]
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL on Kubernetes
- Need a relational database for microservices
- Setting up persistent data storage
- Requires ACID transactions and SQL queries

## What This Skill Does
Deploys a production-ready PostgreSQL database on Kubernetes using the Bitnami Helm chart. Includes persistent storage, connection testing, and migration support.

## Instructions

1. **Deploy PostgreSQL**
   ```bash
   ./scripts/deploy.sh
   ```

2. **Verify Deployment**
   ```bash
   python scripts/verify.py
   ```

3. **Run Migrations** (Optional)
   ```bash
   python scripts/migrate.py
   ```

4. **Test Connection**
   ```bash
   python scripts/test_connection.py
   ```

## Configuration

Default settings in `scripts/deploy.sh`:
- Database: `learnflow`
- Username: `learnflow_user`
- Password: Auto-generated (stored in Secret)
- Storage: 10Gi PVC

## Validation Checklist
- [ ] PostgreSQL pod in Running state
- [ ] PVC bound successfully
- [ ] Database connection successful
- [ ] Test query executes correctly

## Expected Output
```
✓ PostgreSQL deployed to namespace 'postgres'
✓ Pod running
✓ Connection successful
✓ Database: learnflow_user
```

See [REFERENCE.md](./REFERENCE.md) for schema design and advanced configuration.
