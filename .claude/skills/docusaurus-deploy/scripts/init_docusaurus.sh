#!/bin/bash
# Initialize Docusaurus Documentation Site

set -e

# Parse arguments
SITE_NAME=${1:-"docs"}
TEMPLATE=${2:-"classic"}

echo "🚀 Initializing Docusaurus site: $SITE_NAME"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found"
    echo "Install Node.js: https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js $(node --version) found"

# Check if npx is available
if ! command -v npx &> /dev/null; then
    echo "✗ npx not found"
    exit 1
fi

# Create Docusaurus site
echo ""
echo "📦 Creating Docusaurus site..."
npx create-docusaurus@latest "$SITE_NAME" "$TEMPLATE" --typescript false

cd "$SITE_NAME"

echo ""
echo "✓ Docusaurus site created: $SITE_NAME"
echo ""

# Install additional plugins
echo "📦 Installing additional plugins..."
npm install --save @easyops-cn/docusaurus-search-local
npm install --save docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs

echo ""
echo "✓ Additional plugins installed"
echo ""

# Create directory structure
echo "📁 Creating documentation structure..."

mkdir -p docs/api
mkdir -p docs/guides
mkdir -p docs/reference
mkdir -p static/img
mkdir -p static/openapi

echo "✓ Directory structure created"
echo ""

# Create sample API documentation
cat > docs/api/overview.md << 'EOF'
---
sidebar_position: 1
---

# API Overview

Welcome to the LearnFlow API documentation.

## Base URL

```
https://api.learnflow.com/v1
```

## Authentication

All API requests require authentication using JWT tokens:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.learnflow.com/v1/endpoint
```

## Rate Limiting

- 1000 requests per hour per API key
- Rate limit info in response headers

## Endpoints

- [Triage API](./triage.md) - Query routing
- [Concepts API](./concepts.md) - Concept explanations
- [Debug API](./debug.md) - Code debugging
- [Exercise API](./exercise.md) - Practice exercises
EOF

# Create sample guide
cat > docs/guides/getting-started.md << 'EOF'
---
sidebar_position: 1
---

# Getting Started

This guide will help you get started with LearnFlow.

## Prerequisites

- Basic Python knowledge
- Internet connection
- Modern web browser

## Quick Start

1. **Sign Up**
   ```bash
   # Visit https://learnflow.com/signup
   ```

2. **Start Learning**
   - Choose a module
   - Complete exercises
   - Track your progress

3. **Get Help**
   - Ask the AI tutor
   - Check documentation
   - Join community

## Next Steps

- [Student Guide](./students.md)
- [Teacher Guide](./teachers.md)
EOF

# Create sample reference
cat > docs/reference/architecture.md << 'EOF'
---
sidebar_position: 1
---

# Architecture

## System Overview

LearnFlow uses a microservices architecture on Kubernetes.

## Components

### Frontend
- Next.js application
- Monaco code editor
- Real-time updates via WebSockets

### Backend Services
- **Triage Service**: Routes queries to appropriate agents
- **Concepts Agent**: Explains Python concepts
- **Debug Agent**: Helps fix code errors
- **Exercise Agent**: Generates practice problems

### Infrastructure
- **Kafka**: Event streaming
- **PostgreSQL**: Data persistence
- **Redis**: Caching
- **Dapr**: Service mesh

## Data Flow

```mermaid
graph LR
    A[Student] --> B[Frontend]
    B --> C[Triage Service]
    C --> D[Concepts Agent]
    C --> E[Debug Agent]
    C --> F[Exercise Agent]
```
EOF

echo "✓ Sample documentation created"
echo ""

# Update docusaurus.config.js with search
echo "🔧 Configuring search..."

cat > temp_config.js << 'EOF'
// @ts-check
const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'LearnFlow Documentation',
  tagline: 'AI-Powered Python Learning Platform',
  favicon: 'img/favicon.ico',

  url: 'https://docs.learnflow.com',
  baseUrl: '/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/learnflow/docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        language: ["en"],
        highlightSearchTermsOnTargetPage: true,
        docsRouteBasePath: '/docs',
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'LearnFlow',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
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
        copyright: `Copyright © ${new Date().getFullYear()} LearnFlow.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['python', 'bash', 'yaml'],
      },
    }),
};

module.exports = config;
EOF

mv temp_config.js docusaurus.config.js

echo "✓ Configuration updated"
echo ""

echo "="
echo "✓ Docusaurus site initialized successfully!"
echo "="
echo ""
echo "Site location: $PWD"
echo ""
echo "Next steps:"
echo "  1. cd $SITE_NAME"
echo "  2. npm start          # Start dev server"
echo "  3. npm run build      # Build for production"
echo ""
echo "Generated:"
echo "  - docs/api/overview.md"
echo "  - docs/guides/getting-started.md"
echo "  - docs/reference/architecture.md"
echo "  - Local search enabled"
echo ""
echo "To deploy:"
echo "  python ../scripts/build_docs.sh"
echo "  kubectl apply -f k8s/"
