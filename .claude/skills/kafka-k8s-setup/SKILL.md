---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes using Helm for event-driven microservices
version: 1.0.0
author: Hackathon Team
tags: [kafka, kubernetes, messaging, event-driven]
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka on Kubernetes
- Setting up event-driven microservices architecture
- Need message queue for asynchronous communication
- Implementing pub/sub patterns in distributed systems

## What This Skill Does
Deploys a production-ready Apache Kafka cluster on Kubernetes using the Bitnami Helm chart. Includes ZooKeeper coordination, configurable replicas, and health verification.

## Instructions

1. **Deploy Kafka Cluster**
   ```bash
   ./scripts/deploy.sh
   ```
   This script will:
   - Add Bitnami Helm repository
   - Create kafka namespace
   - Deploy Kafka with ZooKeeper
   - Configure persistent storage

2. **Verify Deployment**
   ```bash
   python scripts/verify.py
   ```
   Checks that all pods are running and healthy.

3. **Create Test Topics** (Optional)
   ```bash
   ./scripts/create_topics.sh
   ```

4. **Test Producer/Consumer** (Optional)
   ```bash
   python scripts/test_kafka.py
   ```

## Configuration Options

Edit deployment parameters in `scripts/deploy.sh`:
- Replica count (default: 1 for development)
- Storage size (default: 8Gi)
- Resource limits
- Network policies

## Validation Checklist
- [ ] All Kafka pods in Running state
- [ ] All ZooKeeper pods in Running state
- [ ] Kafka service is accessible
- [ ] Test topic can be created
- [ ] Producer can send messages
- [ ] Consumer can receive messages

## Expected Output
```
✓ Kafka deployed to namespace 'kafka'
✓ All 3 pods running
✓ Kafka broker accessible on kafka.kafka.svc.cluster.local:9092
```

## Troubleshooting
- If pods stuck in Pending: check storage class and PVC
- If pods crash: verify sufficient memory (min 2Gi per pod)
- Connection refused: ensure service is exposed correctly

See [REFERENCE.md](./REFERENCE.md) for architecture details and advanced configuration.
