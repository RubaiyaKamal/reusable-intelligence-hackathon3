#!/bin/bash
# Kafka Kubernetes Deployment Script
# Deploys Apache Kafka using Bitnami Helm chart

set -e  # Exit on error

echo "🚀 Starting Kafka deployment on Kubernetes..."

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create kafka namespace
echo "📁 Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka with Helm
echo "⚙️  Deploying Kafka cluster..."
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=1 \
  --set zookeeper.replicaCount=1 \
  --set persistence.size=8Gi \
  --set resources.requests.memory=2Gi \
  --set resources.requests.cpu=500m \
  --set resources.limits.memory=4Gi \
  --set resources.limits.cpu=2000m \
  --set logRetentionHours=168 \
  --set defaultReplicationFactor=1 \
  --set offsetsTopicReplicationFactor=1 \
  --set transactionStateLogReplicationFactor=1 \
  --wait --timeout=10m

echo ""
echo "✓ Kafka deployed to namespace 'kafka'"
echo ""
echo "Connection details:"
echo "  Internal: kafka.kafka.svc.cluster.local:9092"
echo "  From same namespace: kafka:9092"
echo ""
echo "Next steps:"
echo "  1. Verify deployment: python scripts/verify.py"
echo "  2. Create topics: ./scripts/create_topics.sh"
echo "  3. Test connectivity: python scripts/test_kafka.py"
