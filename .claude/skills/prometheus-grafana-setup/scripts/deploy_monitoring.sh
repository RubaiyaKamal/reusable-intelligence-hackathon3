#!/bin/bash
# Deploy Prometheus and Grafana Monitoring Stack

set -e

echo "🚀 Deploying Prometheus + Grafana monitoring stack..."
echo ""

# Add Prometheus Helm repository
echo "📦 Adding Prometheus Community Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create monitoring namespace
echo "📁 Creating monitoring namespace..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Deploy kube-prometheus-stack (Prometheus + Grafana + AlertManager)
echo "⚙️  Deploying kube-prometheus-stack..."
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set grafana.enabled=true \
  --set grafana.adminPassword=admin \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi \
  --set alertmanager.enabled=true \
  --set alertmanager.persistence.size=10Gi \
  --wait --timeout=10m

echo ""
echo "✓ Monitoring stack deployed to namespace 'monitoring'"
echo ""

# Create ServiceMonitor for application metrics
echo "📝 Creating ServiceMonitor CRDs..."

cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: learnflow-services
  namespace: monitoring
  labels:
    app: learnflow
spec:
  selector:
    matchLabels:
      app: learnflow
  namespaceSelector:
    matchNames:
    - learnflow
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
EOF

echo "✓ ServiceMonitor created"
echo ""

# Display access information
echo "="*60
echo "Prometheus + Grafana deployed successfully!"
echo "="*60
echo ""
echo "Access Grafana:"
echo "  kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
echo "  URL: http://localhost:3000"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Access Prometheus:"
echo "  kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "  URL: http://localhost:9090"
echo ""
echo "Access AlertManager:"
echo "  kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093"
echo "  URL: http://localhost:9093"
echo ""
echo "Next steps:"
echo "  1. Import dashboards: python scripts/import_dashboards.py"
echo "  2. Configure alerts: ./scripts/configure_alerts.sh"
echo "  3. Add ServiceMonitors: python scripts/configure_monitors.py"
