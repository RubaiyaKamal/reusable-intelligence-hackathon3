#!/bin/bash
# StoryForge PostgreSQL Kubernetes Deployment Script

set -e

echo "🚀 Starting PostgreSQL deployment for StoryForge on Kubernetes..."

# Configuration
NAMESPACE="storyforge"
DB_NAME="storyforge_db"
DB_USER="storyforge_user"
HELM_RELEASE="storyforge-postgres"

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace
echo "📁 Creating $NAMESPACE namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Generate secure password
DB_PASSWORD=$(openssl rand -base64 20)
echo "🔐 Generated database password (save this!): $DB_PASSWORD"

# Create secret for credentials
kubectl create secret generic postgres-credentials \
  --from-literal=postgres-password="$DB_PASSWORD" \
  --from-literal=password="$DB_PASSWORD" \
  --namespace $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL with Helm
echo "⚙️  Deploying PostgreSQL..."
helm install $HELM_RELEASE bitnami/postgresql \
  --namespace $NAMESPACE \
  --set auth.username=$DB_USER \
  --set auth.database=$DB_NAME \
  --set auth.existingSecret=postgres-credentials \
  --set primary.persistence.enabled=true \
  --set primary.persistence.size=10Gi \
  --set primary.resources.requests.memory=256Mi \
  --set primary.resources.requests.cpu=250m \
  --set primary.resources.limits.memory=1Gi \
  --set primary.resources.limits.cpu=1000m \
  --set metrics.enabled=true \
  --wait --timeout=10m

echo ""
echo "✓ PostgreSQL deployed to namespace '$NAMESPACE'"
echo ""
echo "Connection details:"
echo "  Host: $HELM_RELEASE.${NAMESPACE}.svc.cluster.local"
echo "  Port: 5432"
echo "  Database: $DB_NAME"
echo "  Username: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo ""
echo "To get password later:"
echo "  kubectl get secret postgres-credentials -n $NAMESPACE -o jsonpath='{.data.password}' | base64 --decode"
echo ""
echo "Connection string for backend:"
echo "  postgresql://$DB_USER:$DB_PASSWORD@$HELM_RELEASE.${NAMESPACE}.svc.cluster.local:5432/$DB_NAME"
echo ""
