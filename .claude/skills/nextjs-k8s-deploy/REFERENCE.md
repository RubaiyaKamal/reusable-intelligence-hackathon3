# Next.js Kubernetes Deployment - Reference Documentation

## Overview

This skill provides production-optimized Next.js deployment to Kubernetes with multi-stage Docker builds, horizontal pod autoscaling, and proper configuration management.

## Next.js on Kubernetes Architecture

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                     │
│  ┌────────────────────────────────────────────────┐ │
│  │  Ingress (nginx/kong)                          │ │
│  │  frontend.learnflow.com → frontend-service     │ │
│  └────────────────┬───────────────────────────────┘ │
│                   │                                 │
│  ┌────────────────▼───────────────────────────────┐ │
│  │  Service: frontend-service (ClusterIP)         │ │
│  │  Port: 80 → 3000                               │ │
│  └────────────────┬───────────────────────────────┘ │
│                   │                                 │
│  ┌────────────────▼───────────────────────────────┐ │
│  │  Deployment: frontend                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │ Next.js  │  │ Next.js  │  │ Next.js  │    │ │
│  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘    │ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  HorizontalPodAutoscaler                       │ │
│  │  Min: 2, Max: 10, CPU: 70%                     │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Multi-Stage Docker Build

### Why Multi-Stage?

Traditional Next.js Dockerfile results in 1GB+ images. Multi-stage builds reduce this to ~150MB.

### Dockerfile Structure

```dockerfile
# Stage 1: Dependencies (Cached Layer)
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runner (Production)
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
```

### Key Optimizations

1. **Layer Caching**: Dependencies installed separately
2. **Standalone Output**: Only necessary files
3. **Non-Root User**: Security best practice
4. **Alpine Linux**: Minimal base image
5. **Static File Optimization**: CDN-ready static assets

## Next.js Configuration

### next.config.js for Kubernetes

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for minimal Docker image
  output: 'standalone',

  // Disable file system cache in containers
  generateBuildId: async () => {
    return process.env.BUILD_ID || 'development'
  },

  // Configure for reverse proxy
  assetPrefix: process.env.ASSET_PREFIX || '',

  // Compression
  compress: true,

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]
  },

  // Environment variables available to browser
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
```

## Environment Variables

### Build-Time Variables

```env
# .env.build
NODE_ENV=production
BUILD_ID=v1.2.3
NEXT_TELEMETRY_DISABLED=1
```

### Runtime Variables

```env
# .env.production
NEXT_PUBLIC_API_URL=https://api.learnflow.com
NEXT_PUBLIC_WS_URL=wss://api.learnflow.com/ws
API_SECRET_KEY=<from-kubernetes-secret>
DATABASE_URL=<from-kubernetes-secret>
```

### Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config
  namespace: learnflow
data:
  API_URL: "http://triage-service.learnflow.svc.cluster.local"
  NODE_ENV: "production"
```

### Kubernetes Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: frontend-secrets
  namespace: learnflow
type: Opaque
stringData:
  API_SECRET_KEY: "your-secret-key"
  SESSION_SECRET: "your-session-secret"
```

## Kubernetes Manifests

### Deployment with Rolling Updates

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: learnflow
  labels:
    app: frontend
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
      - name: nextjs
        image: frontend:latest
        ports:
        - containerPort: 3000
          name: http
        envFrom:
        - configMapRef:
            name: frontend-config
        - secretRef:
            name: frontend-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: learnflow
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
  type: ClusterIP
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: learnflow
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### Ingress (nginx)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: learnflow
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - frontend.learnflow.com
    secretName: frontend-tls
  rules:
  - host: frontend.learnflow.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## Health Check API Route

### pages/api/health.ts

```typescript
import type { NextApiRequest, NextApiResponse } from 'next'

type HealthResponse = {
  status: 'ok' | 'error'
  timestamp: string
  uptime: number
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<HealthResponse>
) {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  })
}
```

## Performance Optimizations

### 1. Image Optimization

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['cdn.learnflow.com'],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
  },
}
```

### 2. Code Splitting

```typescript
// Dynamic imports
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  loading: () => <p>Loading editor...</p>,
  ssr: false
})
```

### 3. Static Generation

```typescript
// Pre-render pages at build time
export async function getStaticProps() {
  const data = await fetchData()
  return {
    props: { data },
    revalidate: 60 // ISR: Regenerate every 60 seconds
  }
}
```

### 4. API Route Caching

```typescript
export default function handler(req, res) {
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate')
  res.json({ data })
}
```

## Build and Deployment Process

### 1. Local Development

```bash
npm run dev
# → http://localhost:3000
```

### 2. Build

```bash
npm run build
npm run start
# Test production build locally
```

### 3. Docker Build

```bash
docker build -t frontend:v1.0.0 .
docker run -p 3000:3000 frontend:v1.0.0
```

### 4. Push to Registry

```bash
docker tag frontend:v1.0.0 registry.example.com/frontend:v1.0.0
docker push registry.example.com/frontend:v1.0.0
```

### 5. Deploy to Kubernetes

```bash
kubectl apply -f k8s/
kubectl rollout status deployment/frontend -n learnflow
```

## Monitoring and Debugging

### View Logs

```bash
# All pods
kubectl logs -l app=frontend -n learnflow

# Specific pod
kubectl logs frontend-xyz -n learnflow

# Follow logs
kubectl logs -f frontend-xyz -n learnflow

# Previous container (if crashed)
kubectl logs frontend-xyz -n learnflow --previous
```

### Check Pod Status

```bash
kubectl get pods -n learnflow -l app=frontend
kubectl describe pod frontend-xyz -n learnflow
```

### Execute Commands in Pod

```bash
kubectl exec -it frontend-xyz -n learnflow -- sh
# Inside pod:
# node --version
# cat .env
# ls -la .next
```

### Port Forward for Testing

```bash
kubectl port-forward -n learnflow svc/frontend 3000:80
# Access at http://localhost:3000
```

## Troubleshooting

### Issue: Image Pull Errors

```bash
# Check image exists
docker pull registry.example.com/frontend:v1.0.0

# Check credentials
kubectl get secret regcred -n learnflow -o yaml

# Add imagePullSecret to deployment
spec:
  template:
    spec:
      imagePullSecrets:
      - name: regcred
```

### Issue: Pod CrashLoopBackOff

```bash
# Check logs
kubectl logs frontend-xyz -n learnflow

# Common causes:
# - Missing environment variables
# - Port already in use
# - Out of memory
```

### Issue: Slow Performance

```bash
# Check resource usage
kubectl top pod frontend-xyz -n learnflow

# Increase resources
spec:
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
```

## Best Practices

1. **Use Standalone Output**: Reduces image size by 80%
2. **Non-Root User**: Security requirement
3. **Health Checks**: Enable rolling updates without downtime
4. **Resource Limits**: Prevent OOM kills
5. **HPA**: Auto-scale based on traffic
6. **Immutable Tags**: Never use `latest` in production
7. **ConfigMaps for Config**: Externalize configuration
8. **Secrets for Sensitive Data**: Never commit secrets
9. **Multiple Replicas**: High availability
10. **Monitoring**: Add APM and error tracking

## Resources

- [Next.js Deployment Documentation](https://nextjs.org/docs/deployment)
- [Next.js Standalone Output](https://nextjs.org/docs/advanced-features/output-file-tracing)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
