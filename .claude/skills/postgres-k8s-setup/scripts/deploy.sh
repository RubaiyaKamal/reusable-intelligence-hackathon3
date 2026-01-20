#!/bin/bash
# PostgreSQL Kubernetes Deployment Script

set -e

echo "🚀 Starting PostgreSQL deployment on Kubernetes..."

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create postgres namespace
echo "📁 Creating postgres namespace..."
kubectl create namespace postgres --dry-run=client -o yaml | kubectl apply -f -

# Generate secure password
DB_PASSWORD=$(openssl rand -base64 20)
echo "🔐 Generated database password (save this!): $DB_PASSWORD"

# Create secret for credentials
kubectl create secret generic postgres-credentials \
  --from-literal=postgres-password="$DB_PASSWORD" \
  --from-literal=password="$DB_PASSWORD" \
  --namespace postgres \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL with Helm
echo "⚙️  Deploying PostgreSQL..."
helm install postgres-postgresql bitnami/postgresql \
  --namespace postgres \
  --set auth.username=learnflow_user \
  --set auth.database=learnflow \
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
echo "✓ PostgreSQL deployed to namespace 'postgres'"
echo ""
echo "Connection details:"
echo "  Host: postgres-postgresql.postgres.svc.cluster.local"
echo "  Port: 5432"
echo "  Database: learnflow"
echo "  Username: learnflow_user"
echo "  Password: $DB_PASSWORD"
echo ""
echo "To get password later:"
echo "  kubectl get secret postgres-credentials -n postgres -o jsonpath='{.data.password}' | base64 --decode"
echo ""
echo "Next steps:"
echo "  1. Verify deployment: python scripts/verify.py"
echo "  2. Run migrations: python scripts/migrate.py"
echo "  3. Test connection: python scripts/test_connection.py"
