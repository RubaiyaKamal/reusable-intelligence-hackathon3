#!/bin/bash
# Build and Deploy Docusaurus Documentation

set -e

SITE_DIR=${1:-.}
IMAGE_NAME=${2:-docs}
IMAGE_TAG=${3:-latest}

echo "🚀 Building Docusaurus documentation..."
echo ""

cd "$SITE_DIR"

# Check if it's a Docusaurus project
if [ ! -f "docusaurus.config.js" ]; then
    echo "✗ Not a Docusaurus project (docusaurus.config.js not found)"
    exit 1
fi

echo "✓ Found Docusaurus project"

# Install dependencies
echo "📦 Installing dependencies..."
npm ci

# Build site
echo "🔨 Building static site..."
npm run build

echo "✓ Build complete: build/"

# Generate Dockerfile if not exists
if [ ! -f "Dockerfile" ]; then
    echo "📝 Generating Dockerfile..."

    cat > Dockerfile << 'EOF'
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built site
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF

    echo "✓ Dockerfile created"
fi

# Generate nginx.conf if not exists
if [ ! -f "nginx.conf" ]; then
    echo "📝 Generating nginx.conf..."

    cat > nginx.conf << 'EOF'
worker_processes auto;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/javascript application/javascript application/json;

    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html;

        location ~* \.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
EOF

    echo "✓ nginx.conf created"
fi

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

echo ""
echo "✓ Docker image built: $IMAGE_NAME:$IMAGE_TAG"
echo ""

# Generate Kubernetes manifests
mkdir -p k8s

cat > k8s/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docs
  namespace: learnflow
spec:
  replicas: 2
  selector:
    matchLabels:
      app: docs
  template:
    metadata:
      labels:
        app: docs
    spec:
      containers:
      - name: nginx
        image: $IMAGE_NAME:$IMAGE_TAG
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
EOF

cat > k8s/service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: docs
  namespace: learnflow
spec:
  selector:
    app: docs
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
EOF

cat > k8s/ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: docs-ingress
  namespace: learnflow
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - docs.learnflow.com
    secretName: docs-tls
  rules:
  - host: docs.learnflow.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: docs
            port:
              number: 80
EOF

echo "✓ Kubernetes manifests generated: k8s/"
echo ""
echo "Next steps:"
echo "  1. Test locally: docker run -p 8080:80 $IMAGE_NAME:$IMAGE_TAG"
echo "  2. Push image: docker push $IMAGE_NAME:$IMAGE_TAG"
echo "  3. Deploy: kubectl apply -f k8s/"
