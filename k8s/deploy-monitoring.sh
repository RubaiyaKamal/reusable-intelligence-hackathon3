#!/bin/bash
# StoryForge Prometheus + Grafana Monitoring Stack Deployment

set -e

echo "🚀 Deploying Prometheus + Grafana monitoring stack for StoryForge..."
echo ""

# Configuration
NAMESPACE="storyforge"
MONITORING_NAMESPACE="monitoring"

# Add Prometheus Helm repository
echo "📦 Adding Prometheus Community Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create monitoring namespace
echo "📁 Creating monitoring namespace..."
kubectl create namespace $MONITORING_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy kube-prometheus-stack (Prometheus + Grafana + AlertManager)
echo "⚙️  Deploying kube-prometheus-stack..."
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace $MONITORING_NAMESPACE \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.enabled=true \
  --set grafana.adminPassword=admin \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi \
  --set alertmanager.enabled=true \
  --set alertmanager.persistence.size=10Gi \
  --wait --timeout=10m

echo ""
echo "✓ Monitoring stack deployed to namespace '$MONITORING_NAMESPACE'"
echo ""

# Create ServiceMonitor for StoryForge services
echo "📝 Creating ServiceMonitor for StoryForge agents..."

cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: storyforge-agents
  namespace: $MONITORING_NAMESPACE
  labels:
    app: storyforge
    release: prometheus
spec:
  selector:
    matchLabels:
      app: storyforge
  namespaceSelector:
    matchNames:
    - $NAMESPACE
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: storyforge-kafka
  namespace: $MONITORING_NAMESPACE
  labels:
    app: storyforge-kafka
    release: prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kafka
  namespaceSelector:
    matchNames:
    - $NAMESPACE
  endpoints:
  - port: metrics
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: storyforge-postgres
  namespace: $MONITORING_NAMESPACE
  labels:
    app: storyforge-postgres
    release: prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: postgresql
  namespaceSelector:
    matchNames:
    - $NAMESPACE
  endpoints:
  - port: metrics
    interval: 30s
EOF

echo "✓ ServiceMonitors created"
echo ""

# Create PrometheusRule for StoryForge alerts
echo "📝 Creating alert rules for StoryForge..."

cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: storyforge-alerts
  namespace: $MONITORING_NAMESPACE
  labels:
    app: storyforge
    release: prometheus
spec:
  groups:
  - name: storyforge.rules
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ \$value }} errors/sec"

    - alert: SlowResponseTime
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Slow response time"
        description: "95th percentile response time is {{ \$value }}s"

    - alert: StudentFrustrationDetected
      expr: rate(router_engagement_level{level="frustrated"}[5m]) > 5
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "High student frustration detected"
        description: "{{ \$value }} frustrated students in last 5 minutes"

    - alert: AgentHighMemoryUsage
      expr: container_memory_usage_bytes{namespace="$NAMESPACE"} / container_spec_memory_limit_bytes{namespace="$NAMESPACE"} > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Agent using high memory"
        description: "{{ \$labels.pod }} memory usage > 90%"

    - alert: KafkaConsumerLag
      expr: kafka_consumergroup_lag > 1000
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Kafka consumer lag detected"
        description: "Consumer lag is {{ \$value }} messages"

    - alert: PostgreSQLDown
      expr: up{job="storyforge-postgres"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "PostgreSQL is down"
        description: "PostgreSQL database is not responding"
EOF

echo "✓ Alert rules created"
echo ""

# Display access information
echo "================================================================"
echo "StoryForge Monitoring Stack Deployed Successfully!"
echo "================================================================"
echo ""
echo "Access Grafana Dashboard:"
echo "  kubectl port-forward -n $MONITORING_NAMESPACE svc/prometheus-grafana 3000:80"
echo "  URL: http://localhost:3000"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Access Prometheus:"
echo "  kubectl port-forward -n $MONITORING_NAMESPACE svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "  URL: http://localhost:9090"
echo ""
echo "Access AlertManager:"
echo "  kubectl port-forward -n $MONITORING_NAMESPACE svc/prometheus-kube-prometheus-alertmanager 9093:9093"
echo "  URL: http://localhost:9093"
echo ""
echo "Monitored Services:"
echo "  - StoryForge Agents (Router, Story, Vocabulary, Comprehension)"
echo "  - Kafka Event Bus"
echo "  - PostgreSQL Database"
echo ""
echo "Configured Alerts:"
echo "  - High Error Rate"
echo "  - Slow Response Time"
echo "  - Student Frustration Detection"
echo "  - High Memory Usage"
echo "  - Kafka Consumer Lag"
echo "  - PostgreSQL Down"
echo ""
echo "Next steps:"
echo "  1. Import custom StoryForge dashboards"
echo "  2. Configure Slack/Email alert notifications"
echo "  3. Add custom metrics to agents"
echo ""
