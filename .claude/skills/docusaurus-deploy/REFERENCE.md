# Docusaurus Deployment - Reference Documentation

## Overview

Docusaurus is a modern static site generator optimized for documentation websites. This skill automates deployment to Kubernetes with search integration, versioning, and API documentation generation.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                     │
│  ┌────────────────────────────────────────────────┐ │
│  │  Ingress: docs.learnflow.com                   │ │
│  └────────────────┬───────────────────────────────┘ │
│                   │                                 │
│  ┌────────────────▼───────────────────────────────┐ │
│  │  Service: docs-service                         │ │
│  └────────────────┬───────────────────────────────┘ │
│                   │                                 │
│  ┌────────────────▼───────────────────────────────┐ │
│  │  Deployment: docs                              │ │
│  │  ┌──────────────────────────────────────────┐ │ │
│  │  │  nginx:alpine serving static files       │ │ │
│  │  │  /usr/share/nginx/html/                  │ │ │
│  │  │  - index.html                            │ │ │
│  │  │  - assets/                               │ │ │
│  │  │  - docs/                                 │ │ │
│  │  └──────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Docusaurus Features

### 1. Documentation Structure

```
docs-site/
├── docs/                    # Documentation pages
│   ├── intro.md            # Getting started
│   ├── api/                # API documentation
│   │   ├── triage.md
│   │   ├── concepts.md
│   │   └── exercise.md
│   ├── guides/             # User guides
│   │   ├── students.md
│   │   └── teachers.md
│   └── reference/          # Technical reference
│       ├── architecture.md
│       └── deployment.md
├── blog/                   # Optional blog
│   └── 2025-01-10-release.md
├── src/                    # Custom components
│   ├── components/
│   ├── css/
│   └── pages/
├── static/                 # Static assets
│   ├── img/
│   └── files/
├── docusaurus.config.js    # Configuration
├── sidebars.js             # Navigation
└── package.json
```

### 2. Configuration

**docusaurus.config.js:**
```javascript
const config = {
  title: 'LearnFlow Documentation',
  tagline: 'AI-Powered Python Learning Platform',
  url: 'https://docs.learnflow.com',
  baseUrl: '/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  favicon: 'img/favicon.ico',

  organizationName: 'learnflow',
  projectName: 'learnflow-docs',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/learnflow/docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/learnflow/docs/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'LearnFlow',
      logo: {
        alt: 'LearnFlow Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/learnflow/learnflow',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
            {
              label: 'API Reference',
              to: '/docs/api',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/learnflow',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} LearnFlow.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
      additionalLanguages: ['python', 'bash', 'yaml'],
    },
  },
};

module.exports = config;
```

### 3. Sidebar Configuration

**sidebars.js:**
```javascript
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/triage',
        'api/concepts',
        'api/debug',
        'api/exercise',
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/students',
        'guides/teachers',
      ],
    },
    {
      type: 'category',
      label: 'Technical Reference',
      items: [
        'reference/architecture',
        'reference/deployment',
        'reference/kubernetes',
      ],
    },
  ],
};

module.exports = sidebars;
```

## Search Integration

### Algolia DocSearch

```javascript
// In docusaurus.config.js
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'learnflow',
    contextualSearch: true,
    searchParameters: {},
  },
}
```

### Local Search (Alternative)

```bash
npm install --save @easyops-cn/docusaurus-search-local
```

```javascript
// In docusaurus.config.js
themes: [
  [
    require.resolve("@easyops-cn/docusaurus-search-local"),
    {
      hashed: true,
      language: ["en"],
      highlightSearchTermsOnTargetPage: true,
    },
  ],
],
```

## API Documentation from OpenAPI

### Using docusaurus-openapi-docs

```bash
npm install docusaurus-plugin-openapi-docs
npm install docusaurus-theme-openapi-docs
```

```javascript
// In docusaurus.config.js
plugins: [
  [
    'docusaurus-plugin-openapi-docs',
    {
      id: "api",
      docsPluginId: "classic",
      config: {
        learnflow: {
          specPath: "openapi/learnflow-api.yaml",
          outputDir: "docs/api",
          sidebarOptions: {
            groupPathsBy: "tag",
          },
        },
      },
    },
  ],
],
themes: ["docusaurus-theme-openapi-docs"],
```

Generate API docs:
```bash
npm run docusaurus gen-api-docs all
```

## Deployment

### Docker Build

**Dockerfile:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf:**
```nginx
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
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        # Enable browser caching for static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # SPA fallback
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
    }
}
```

### Kubernetes Deployment

**deployment.yaml:**
```yaml
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
        image: docs:latest
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
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

**service.yaml:**
```yaml
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
```

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: docs-ingress
  namespace: learnflow
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
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
```

## Versioning

### Enable Versioning

```bash
npm run docusaurus docs:version 1.0.0
```

This creates:
- `versioned_docs/version-1.0.0/` - Snapshot of docs
- `versioned_sidebars/version-1.0.0-sidebars.json` - Sidebar config
- `versions.json` - List of versions

### Version Dropdown

Automatically appears in navbar when versions exist.

### Configuration

```javascript
// docusaurus.config.js
presets: [
  [
    'classic',
    {
      docs: {
        lastVersion: 'current',
        versions: {
          current: {
            label: '2.0.0 (Next)',
            path: 'next',
          },
          '1.0.0': {
            label: '1.0.0',
            path: '1.0.0',
          },
        },
      },
    },
  ],
],
```

## Custom Components

### Interactive Code Examples

```jsx
// src/components/CodeExample.js
import React, { useState } from 'react';
import CodeBlock from '@theme/CodeBlock';

export default function CodeExample({ code, language = 'python' }) {
  const [output, setOutput] = useState('');

  const runCode = async () => {
    // Call code execution API
    const response = await fetch('/api/execute', {
      method: 'POST',
      body: JSON.stringify({ code, language }),
    });
    const result = await response.json();
    setOutput(result.output);
  };

  return (
    <div>
      <CodeBlock language={language}>{code}</CodeBlock>
      <button onClick={runCode}>Run Code</button>
      {output && <pre>{output}</pre>}
    </div>
  );
}
```

Usage in markdown:
```mdx
import CodeExample from '@site/src/components/CodeExample';

<CodeExample
  code={`print("Hello, World!")`}
  language="python"
/>
```

## Best Practices

### 1. File Organization

```
docs/
├── intro.md              # Clear starting point
├── getting-started/      # Tutorial-style guides
├── api/                  # API reference (auto-generated)
├── guides/               # How-to guides
├── reference/            # Technical details
└── troubleshooting/      # Common issues
```

### 2. Markdown Features

**Admonitions:**
```markdown
:::tip
Use environment variables for configuration
:::

:::warning
This feature is experimental
:::

:::danger
Never commit API keys
:::
```

**Code Blocks with Highlighting:**
````markdown
```python {2-4}
def greet(name):
    # This line is highlighted
    message = f"Hello, {name}!"
    return message
```
````

**Tabs:**
```mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="npm" label="npm">
    npm install docusaurus
  </TabItem>
  <TabItem value="yarn" label="Yarn">
    yarn add docusaurus
  </TabItem>
</Tabs>
```

### 3. SEO Optimization

```markdown
---
title: Getting Started
description: Learn how to set up LearnFlow
keywords: [python, learning, ai, tutorial]
image: /img/social-card.png
---
```

### 4. Performance

- **Enable compression** in nginx
- **Lazy load images**
- **Optimize assets** before committing
- **Use CDN** for static assets

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Docs

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'docusaurus.config.js'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Build Docker image
        run: docker build -t docs:${{ github.sha }} .

      - name: Push to registry
        run: |
          docker tag docs:${{ github.sha }} registry.example.com/docs:latest
          docker push registry.example.com/docs:latest

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/docs nginx=registry.example.com/docs:latest -n learnflow
```

## Troubleshooting

### Build Errors

```bash
# Clear cache
npm run docusaurus clear

# Clean install
rm -rf node_modules package-lock.json
npm install

# Build with debug
npm run build -- --debug
```

### Broken Links

```bash
# Check for broken links
npm run docusaurus build
# Docusaurus will fail build on broken internal links
```

### Search Not Working

1. Check Algolia credentials
2. Verify index is updated
3. Test with local search plugin as fallback

## Resources

- [Docusaurus Documentation](https://docusaurus.io/)
- [Docusaurus Showcase](https://docusaurus.io/showcase)
- [OpenAPI Plugin](https://github.com/PaloAltoNetworks/docusaurus-openapi-docs)
- [Algolia DocSearch](https://docsearch.algolia.com/)
