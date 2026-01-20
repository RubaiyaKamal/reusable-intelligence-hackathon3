#!/bin/bash
# StoryForge Kafka Kubernetes Deployment Script

set -e

echo "🚀 Starting Kafka deployment for StoryForge on Kubernetes..."

# Configuration
NAMESPACE="storyforge"
HELM_RELEASE="storyforge-kafka"

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace if not exists
echo "📁 Ensuring $NAMESPACE namespace exists..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka with Helm
echo "⚙️  Deploying Kafka cluster..."
helm install $HELM_RELEASE bitnami/kafka \
  --namespace $NAMESPACE \
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
  --set metrics.kafka.enabled=true \
  --set metrics.jmx.enabled=true \
  --wait --timeout=10m

echo ""
echo "✓ Kafka deployed to namespace '$NAMESPACE'"
echo ""
echo "Connection details:"
echo "  Internal: $HELM_RELEASE.${NAMESPACE}.svc.cluster.local:9092"
echo "  From same namespace: $HELM_RELEASE:9092"
echo ""
echo "StoryForge Kafka Topics to create:"
echo "  - story.generated       (Stories created by Story Agent)"
echo "  - vocabulary.lookup     (Word definitions requested)"
echo "  - comprehension.question (Questions answered)"
echo "  - student.progress      (Progress updates)"
echo "  - router.events         (Query routing decisions)"
echo "  - agent.metrics         (Agent performance metrics)"
echo ""
echo "Next steps:"
echo "  1. Create topics: bash k8s/create-kafka-topics.sh"
echo "  2. Update backend KAFKA_BOOTSTRAP_SERVERS in .env"
echo ""
