---
name: argocd-app-deployment
description: Implement GitOps continuous deployment with ArgoCD
version: 1.0.0
author: Hackathon Team
tags: [argocd, gitops, cd, kubernetes]
---

# Argocd App Deployment

## When to Use
- Implement GitOps continuous deployment with ArgoCD
- Need automated argocd operations
- Part of CI/CD or infrastructure automation

## What This Skill Does
Automates argocd app deployment with production-ready scripts and configurations.

## Instructions

1. **Setup/Deploy**
   ```bash
   ./scripts/setup_argocd.sh
   ```

2. **Configure/Create**
   ```bash
   python scripts/create_application.py
   ```

3. **Verify/Test**
   ```bash
   python scripts/sync_app.sh
   ```

## Validation Checklist
- [ ] Setup completed successfully
- [ ] Configuration applied
- [ ] Tests pass
- [ ] Integrated with existing services

## Expected Output
```
✓ argocd-app-deployment configured
✓ All components operational
✓ Tests passed
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and advanced usage.
