---
name: docusaurus-search-config
description: Configure search functionality in Docusaurus
version: 1.0.0
author: Hackathon Team
tags: [docusaurus, search, algolia, documentation]
---

# Docusaurus Search Config

## When to Use
- Configure search functionality in Docusaurus
- Need automated docusaurus operations
- Part of CI/CD or infrastructure automation

## What This Skill Does
Automates docusaurus search config with production-ready scripts and configurations.

## Instructions

1. **Setup/Deploy**
   ```bash
   ./scripts/setup_algolia.py
   ```

2. **Configure/Create**
   ```bash
   python scripts/setup_local_search.py
   ```

3. **Verify/Test**
   ```bash
   python scripts/test_search.py
   ```

## Validation Checklist
- [ ] Setup completed successfully
- [ ] Configuration applied
- [ ] Tests pass
- [ ] Integrated with existing services

## Expected Output
```
✓ docusaurus-search-config configured
✓ All components operational
✓ Tests passed
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and advanced usage.
