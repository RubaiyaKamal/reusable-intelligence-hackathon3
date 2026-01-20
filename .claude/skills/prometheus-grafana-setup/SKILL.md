---
name: prometheus-grafana-setup
description: Deploy Prometheus and Grafana monitoring stack on Kubernetes
version: 1.0.0
author: Hackathon Team
tags: [prometheus, grafana, monitoring, observability, metrics]
---

# Prometheus + Grafana Monitoring Setup

## When to Use
- Need application and infrastructure monitoring
- Want visualization dashboards for metrics
- Setting up alerting rules and notifications
- Tracking SLOs and performance metrics
- Monitoring Kubernetes clusters

## What This Skill Does
Deploys a complete monitoring stack with:
- Prometheus for metrics collection and storage
- Grafana for visualization dashboards
- AlertManager for notifications
- ServiceMonitor CRDs for auto-discovery
- Pre-configured dashboards for Kubernetes and applications

## Instructions

1. **Deploy Monitoring Stack**
   ```bash
   ./scripts/deploy_monitoring.sh
   ```

2. **Configure ServiceMonitors for Your Apps**
   ```bash
   python scripts/configure_monitors.py --namespace learnflow
   ```

3. **Import Dashboards**
   ```bash
   python scripts/import_dashboards.py --dashboards ./dashboards
   ```

4. **Setup Alerts**
   ```bash
   ./scripts/configure_alerts.sh
   ```

5. **Access Grafana**
   ```bash
   kubectl port-forward -n monitoring svc/grafana 3000:80
   # Open http://localhost:3000
   # Default credentials: admin/admin
   ```

## Pre-configured Dashboards
- Kubernetes Cluster Overview
- Pod Resources (CPU/Memory/Network)
- Kafka Broker Metrics
- PostgreSQL Performance
- FastAPI Application Metrics
- Request Latency & Error Rates
- Custom Application Dashboards

## Validation Checklist
- [ ] Prometheus collecting metrics
- [ ] Grafana accessible and configured
- [ ] Dashboards displaying data
- [ ] Alerts configured and firing correctly
- [ ] ServiceMonitors detecting targets
- [ ] Data retention configured

## Expected Output
```
✓ Prometheus deployed to namespace 'monitoring'
✓ Grafana deployed and accessible
✓ AlertManager configured
✓ ServiceMonitors created for 5 services
✓ 10 dashboards imported
✓ All targets healthy
```

See [REFERENCE.md](./REFERENCE.md) for custom metrics, alert rules, and dashboard creation.
