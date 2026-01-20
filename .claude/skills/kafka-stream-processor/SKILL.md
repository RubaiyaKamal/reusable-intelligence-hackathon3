---
name: kafka-stream-processor
description: Deploy Kafka Streams applications for real-time processing
version: 1.0.0
author: Hackathon Team
tags: [kafka, streaming, real-time, processing]
---

# Kafka Stream Processor

## When to Use
- Deploy Kafka Streams applications for real-time processing
- Need automated kafka operations
- Part of CI/CD or infrastructure automation

## What This Skill Does
Automates kafka stream processor with production-ready scripts and configurations.

## Instructions

1. **Setup/Deploy**
   ```bash
   ./scripts/deploy_stream_app.sh
   ```

2. **Configure/Create**
   ```bash
   python scripts/create_processor.py
   ```

3. **Verify/Test**
   ```bash
   python scripts/verify_stream.py
   ```

## Validation Checklist
- [ ] Setup completed successfully
- [ ] Configuration applied
- [ ] Tests pass
- [ ] Integrated with existing services

## Expected Output
```
✓ kafka-stream-processor configured
✓ All components operational
✓ Tests passed
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and advanced usage.
