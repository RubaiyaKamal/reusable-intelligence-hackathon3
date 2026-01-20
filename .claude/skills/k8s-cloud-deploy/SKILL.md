---
name: k8s-cloud-deploy
description: Deploy applications to cloud Kubernetes (AWS EKS, GCP GKE, Azure AKS, Oracle OKE)
version: 1.0.0
author: Hackathon Team
tags: [kubernetes, cloud, aws, gcp, azure, oracle, deployment]
---

# Kubernetes Cloud Deployment

## When to Use
- User asks to deploy to cloud (AWS, GCP, Azure, Oracle)
- Need to deploy Kubernetes application to production
- Setting up cloud-native infrastructure
- Deploying with ArgoCD GitOps

## What This Skill Does
Deploys applications to managed Kubernetes services on major cloud providers (AWS EKS, GCP GKE, Azure AKS, Oracle OKE) with infrastructure provisioning, application deployment, and ArgoCD GitOps setup.

## Instructions

### 1. **Choose Cloud Provider**
```bash
python scripts/deploy.py --provider <aws|gcp|azure|oracle> --cluster-name storyforge-prod
```

### 2. **Provision Infrastructure**
```bash
python scripts/provision_infra.py --provider <cloud> --cluster-name storyforge-prod --region us-east-1
```

### 3. **Deploy Infrastructure Services**
```bash
# PostgreSQL
python scripts/deploy_postgres.py

# Kafka
python scripts/deploy_kafka.py

# Monitoring
python scripts/deploy_monitoring.py
```

### 4. **Deploy Application**
```bash
python scripts/deploy_app.py --namespace storyforge
```

### 5. **Setup ArgoCD**
```bash
python scripts/setup_argocd.py
```

### 6. **Verify Deployment**
```bash
python scripts/verify.py --namespace storyforge
```

## Configuration

**AWS EKS**:
- Node type: t3.medium (2 vCPU, 4GB RAM)
- Nodes: 3 (auto-scaling 2-5)
- Cost: ~$165-200/month

**GCP GKE**:
- Node type: n1-standard-2 (2 vCPU, 7.5GB RAM)
- Nodes: 3 (auto-scaling 2-5)
- Cost: ~$178-220/month

**Azure AKS**:
- Node type: Standard_D2s_v3 (2 vCPU, 8GB RAM)
- Nodes: 3 (auto-scaling 2-5)
- Cost: ~$180-230/month

**Oracle OKE**:
- Node type: VM.Standard.E4.Flex (2 OCPU, 16GB RAM)
- Nodes: 3
- Cost: ~$100-150/month (Oracle Cloud Free Tier available)

## Validation Checklist
- [ ] Cloud CLI installed and authenticated
- [ ] Kubernetes cluster created
- [ ] kubectl configured
- [ ] Namespace created
- [ ] Secrets configured
- [ ] Infrastructure services deployed (Postgres, Kafka, Redis)
- [ ] Application pods running
- [ ] Ingress configured with TLS
- [ ] ArgoCD installed and syncing
- [ ] Monitoring stack operational

## Expected Output
```
✓ Cluster created: storyforge-prod
✓ kubectl configured
✓ Namespace: storyforge created
✓ Secrets: storyforge-secrets created
✓ PostgreSQL: Running (1/1 pods)
✓ Kafka: Running (1/1 pods)
✓ Redis: Running (1/1 pods)
✓ Backend: Running (2/2 pods)
✓ Frontend: Running (2/2 pods)
✓ Ingress: Configured
✓ ArgoCD: Synced

Access URLs:
- Frontend: https://storyforge.example.com
- Backend API: https://api.storyforge.example.com
- ArgoCD: https://argocd.storyforge.example.com
- Grafana: https://grafana.storyforge.example.com
```

See [REFERENCE.md](./REFERENCE.md) for detailed cloud provider setup and troubleshooting.
