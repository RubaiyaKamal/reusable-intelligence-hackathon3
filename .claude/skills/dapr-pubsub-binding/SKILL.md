---
name: dapr-pubsub-binding
description: Implement Dapr Pub/Sub and Bindings for microservices
version: 1.0.0
author: Hackathon Team
tags: [dapr, pubsub, bindings, microservices]
---

# Dapr Pubsub Binding

## When to Use
- Implement Dapr Pub/Sub and Bindings for microservices
- Need automated dapr operations
- Part of CI/CD or infrastructure automation

## What This Skill Does
Automates dapr pubsub binding with production-ready scripts and configurations.

## Instructions

1. **Setup/Deploy**
   ```bash
   ./scripts/create_pubsub.py
   ```

2. **Configure/Create**
   ```bash
   python scripts/create_binding.py
   ```

3. **Verify/Test**
   ```bash
   python scripts/test_components.py
   ```

## Validation Checklist
- [ ] Setup completed successfully
- [ ] Configuration applied
- [ ] Tests pass
- [ ] Integrated with existing services

## Expected Output
```
✓ dapr-pubsub-binding configured
✓ All components operational
✓ Tests passed
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and advanced usage.
