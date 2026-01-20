---
name: docusaurus-deploy
description: Deploy Docusaurus documentation sites to Kubernetes
version: 1.0.0
author: Hackathon Team
tags: [docusaurus, documentation, kubernetes, static-site]
---

# Docusaurus Deployment

## When to Use
- Deploying project documentation
- Need searchable, versioned docs
- Want auto-generated API documentation
- Setting up developer portal

## What This Skill Does
Deploys Docusaurus static documentation sites to Kubernetes with:
- Static file serving via Nginx
- Algolia search integration
- Versioning support
- Auto-generation from OpenAPI specs
- CI/CD integration

## Instructions

1. **Initialize Docusaurus Site**
   ```bash
   ./scripts/init_docusaurus.sh --name learnflow-docs
   ```

2. **Generate API Docs from OpenAPI**
   ```bash
   python scripts/generate_api_docs.py --spec openapi.yaml --output docs/api
   ```

3. **Build Static Site**
   ```bash
   ./scripts/build_docs.sh
   ```

4. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/docs/
   ```

5. **Verify Deployment**
   ```bash
   python scripts/verify_docs.py
   ```

## Generated Site Structure
```
docs-site/
├── docs/                    # Markdown documentation
│   ├── intro.md
│   ├── api/                 # Auto-generated API docs
│   ├── guides/
│   └── reference/
├── blog/                    # Optional blog
├── src/                     # Custom React components
├── static/                  # Static assets
├── docusaurus.config.js     # Configuration
└── sidebars.js              # Navigation structure
```

## Kubernetes Deployment
```
k8s/docs/
├── deployment.yaml          # Nginx serving static files
├── service.yaml             # ClusterIP service
├── ingress.yaml             # docs.learnflow.com
└── configmap.yaml           # Nginx configuration
```

## Features
- **Search**: Algolia DocSearch integration
- **Versioning**: Multiple doc versions
- **Dark Mode**: Built-in theme switching
- **Mobile**: Responsive design
- **SEO**: Optimized for search engines

## Validation Checklist
- [ ] Site builds without errors
- [ ] All internal links work
- [ ] Search functionality works
- [ ] API documentation rendered
- [ ] Site accessible via Ingress
- [ ] Mobile responsive

See [REFERENCE.md](./REFERENCE.md) for customization and theming options.
