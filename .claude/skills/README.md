# Claude Code Skills Library

This directory contains reusable skills for AI coding agents (Claude Code, Goose, Codex) following the MCP Code Execution pattern from Hackathon III.

## Skills Overview

## 📊 Completion Status

**All 16 Skills Complete!** ✅

| Category | Skills | Status |
|----------|--------|--------|
| Core Infrastructure | 3 | ✅ Complete |
| Service Development | 2 | ✅ Complete |
| Frontend & Documentation | 2 | ✅ Complete |
| Observability | 2 | ✅ Complete |
| Advanced Features | 7 | ✅ Complete |
| **Total** | **16** | **✅ 100%** |

### Core Infrastructure Skills

#### 1. **agents-md-gen** - AGENTS.md Generator ✅
Generates repository documentation for AI agents.
- **When to use**: Setting up new repositories
- **Key scripts**: `generate_agents_md.py`
- **Token cost**: ~100 tokens
- **Status**: Complete with full Python script

#### 2. **kafka-k8s-setup** - Kafka on Kubernetes ✅
Deploys Apache Kafka cluster using Helm.
- **When to use**: Event-driven architectures
- **Key scripts**: `deploy.sh`, `verify.py`, `create_topics.sh`, `test_kafka.py`
- **Token cost**: ~120 tokens
- **Status**: Complete with 4 production scripts + comprehensive REFERENCE.md

#### 3. **postgres-k8s-setup** - PostgreSQL on Kubernetes ✅
Deploys PostgreSQL with migrations.
- **When to use**: Relational database needs
- **Key scripts**: `deploy.sh`, `verify.py`, `migrate.py`, `test_connection.py`
- **Token cost**: ~110 tokens
- **Status**: Complete with LearnFlow schema + 4 scripts + REFERENCE.md

### Service Development Skills

#### 4. **fastapi-dapr-agent** - FastAPI Microservice with AI ✅
Generates FastAPI services with Dapr and AI agents.
- **When to use**: Building AI-powered microservices
- **Key scripts**: `generate_service.py`, `add_agent.py`, `deploy_service.sh`
- **Token cost**: ~150 tokens
- **Status**: Complete with service generator + agent templates + REFERENCE.md

#### 5. **mcp-code-execution** - MCP Efficiency Pattern ✅
Implements MCP with code execution for 80-98% token reduction.
- **When to use**: Optimizing MCP tool usage
- **Key scripts**: `mcp_client.py`, `create_mcp_wrapper.py`, `create_skill_from_mcp.py`, `test_mcp_skill.py`
- **Token cost**: ~100 tokens
- **Status**: Complete with 4 scripts + comprehensive pattern documentation

### Frontend & Documentation Skills

#### 6. **nextjs-k8s-deploy** - Next.js Deployment ✅
Deploys Next.js apps with optimized Docker builds and Docker Compose.
- **When to use**: Frontend deployment, Docker memory/space issues
- **Key scripts**: `generate_dockerfile.py`, `generate_docker_compose.py`, `docker_cleanup.py`
- **Token cost**: ~130 tokens
- **Status**: Complete with Docker Compose + cleanup + quickstart guide

#### 7. **docusaurus-deploy** - Documentation Sites ✅
Deploys Docusaurus documentation to Kubernetes.
- **When to use**: Project documentation
- **Key scripts**: `init_docusaurus.sh`, `generate_api_docs.py`, `build_docs.sh`
- **Token cost**: ~110 tokens
- **Status**: Complete with 3 scripts + OpenAPI integration

### Observability Skills

#### 8. **prometheus-grafana-setup** - Monitoring Stack ✅
Deploys Prometheus and Grafana for observability.
- **When to use**: Monitoring and alerting
- **Key scripts**: `deploy_monitoring.sh`, `configure_monitors.py`, `import_dashboards.py`
- **Token cost**: ~120 tokens
- **Status**: Complete with kube-prometheus-stack deployment

#### 9. **argocd-app-deployment** - GitOps Deployment ✅
Implements continuous deployment with ArgoCD.
- **When to use**: GitOps workflows
- **Key scripts**: `setup_argocd.sh`, `create_application.py`, `sync_app.sh`
- **Token cost**: ~130 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

### Advanced Skills

#### 10. **agent-testing-framework** - Agent Testing ✅
Automated testing for AI agent interactions.
- **Key scripts**: `create_test.py`, `run_tests.py`, `generate_report.py`
- **Token cost**: ~100 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

#### 11. **kafka-stream-processor** - Stream Processing ✅
Kafka Streams application deployment.
- **Key scripts**: `deploy_stream_app.sh`, `create_processor.py`, `verify_stream.py`
- **Token cost**: ~120 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

#### 12. **pg-data-backup-restore** - Database Backup ✅
Automated PostgreSQL backup and recovery.
- **Key scripts**: `backup_db.sh`, `restore_db.sh`, `schedule_backups.py`
- **Token cost**: ~110 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

#### 13. **dapr-pubsub-binding** - Dapr Patterns ✅
Implementing Dapr Pub/Sub and Bindings.
- **Key scripts**: `create_pubsub.py`, `create_binding.py`, `test_components.py`
- **Token cost**: ~120 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

#### 14. **mcp-state-management** - MCP State ✅
Durable state management in MCP pattern.
- **Key scripts**: `create_state_wrapper.py`, `test_state.py`
- **Token cost**: ~110 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 2 scripts

#### 15. **nextjs-perf-optimize** - Next.js Performance ✅
Performance optimization techniques.
- **Key scripts**: `analyze_bundle.py`, `optimize_images.py`, `generate_report.py`
- **Token cost**: ~120 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

#### 16. **docusaurus-search-config** - Documentation Search ✅
Configuring Docusaurus search functionality.
- **Key scripts**: `setup_algolia.py`, `setup_local_search.py`, `test_search.py`
- **Token cost**: ~100 tokens
- **Status**: Complete with SKILL.md + REFERENCE.md + 3 scripts

## MCP Code Execution Pattern

All skills follow the efficient pattern:

```
BEFORE (Inefficient - Direct MCP):
- MCP tool definitions: 50k tokens
- Intermediate results: 50k tokens
- Total: 100k tokens (41% of context)

AFTER (Efficient - Skills + Scripts):
- SKILL.md: ~100 tokens
- Script output: ~10 tokens
- Total: ~110 tokens (3% of context)

SAVINGS: 80-98% token reduction
```

## Usage with AI Agents

### Claude Code
```bash
# Skills auto-discovered from .claude/skills/
claude "deploy kafka to kubernetes"
# → Automatically uses kafka-k8s-setup skill
```

### Goose
```bash
# Goose reads .claude/skills/ directly
goose "setup postgresql with migrations"
# → Uses postgres-k8s-setup skill
```

### OpenAI Codex
```bash
# Codex also supports .claude/skills/
codex "generate fastapi service with dapr"
# → Uses fastapi-dapr-agent skill
```

## Skill Structure

Each skill follows this pattern:

```
skill-name/
├── SKILL.md              # Instructions (~100 tokens)
├── REFERENCE.md          # Detailed docs (loaded on-demand)
└── scripts/              # Executable code (0 tokens in context)
    ├── deploy.sh
    ├── verify.py
    └── test.py
```

### SKILL.md Template
```markdown
---
name: skill-name
description: Brief description
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## What This Skill Does
One paragraph explanation.

## Instructions
1. Step 1: `./scripts/step1.sh`
2. Step 2: `python scripts/step2.py`

## Validation Checklist
- [ ] Check 1
- [ ] Check 2

## Expected Output
```
Expected result
```

See [REFERENCE.md](./REFERENCE.md) for details.
```

## Development Guidelines

### Creating New Skills

1. **Choose Appropriate Scope**
   - Single responsibility
   - Reusable across projects
   - Clear trigger conditions

2. **Optimize for Tokens**
   - SKILL.md: Keep under 200 tokens
   - Move details to REFERENCE.md
   - Executable logic in scripts/

3. **Write Robust Scripts**
   - Handle errors gracefully
   - Return minimal output
   - Include verification steps

4. **Document Clearly**
   - "When to Use" section is critical
   - Provide exact commands
   - Include troubleshooting

### Testing Skills

Test with both Claude Code and Goose:

```bash
# Test with Claude Code
claude "test kafka skill"

# Test with Goose
goose "verify postgres deployment skill"
```

## Token Efficiency Metrics

| Approach | Tokens | Context % | Efficiency |
|----------|--------|-----------|------------|
| Direct MCP (5 servers) | 50,000+ | 41%+ | ❌ Poor |
| Skills + Scripts | ~110 | 3% | ✅ Excellent |
| **Improvement** | **~450x less** | **~14x less** | **98% reduction** |

## LearnFlow Application

These skills work together to build the LearnFlow platform:

```
Phase 1: Infrastructure
├── kafka-k8s-setup → Event streaming
├── postgres-k8s-setup → Database
└── prometheus-grafana-setup → Monitoring

Phase 2: Backend Services
├── fastapi-dapr-agent → Triage Service
├── fastapi-dapr-agent → Concepts Service
├── fastapi-dapr-agent → Debug Service
└── fastapi-dapr-agent → Exercise Service

Phase 3: Frontend
└── nextjs-k8s-deploy → Student/Teacher UI

Phase 4: Documentation
└── docusaurus-deploy → API Documentation

Phase 5: Deployment
└── argocd-app-deployment → GitOps CD
```

## Best Practices

1. **Single Prompt Deployment**: Aim for one prompt → full deployment
2. **Verify Everything**: Always include verification scripts
3. **Fail Fast**: Exit immediately on errors with clear messages
4. **Minimal Output**: Return only essential information
5. **Idempotent Operations**: Scripts should be safe to run multiple times
6. **Cross-Platform**: Test on Linux, macOS, and Windows/WSL
7. **Documentation**: Keep REFERENCE.md comprehensive
8. **Versioning**: Use semantic versioning for skills
9. **Testing**: Test with multiple AI agents
10. **Feedback Loop**: Improve skills based on agent performance

## Troubleshooting

### Skill Not Loading
```bash
# Check skill syntax
cat .claude/skills/skill-name/SKILL.md

# Verify YAML frontmatter
head -n 10 .claude/skills/skill-name/SKILL.md
```

### Script Execution Fails
```bash
# Make scripts executable
chmod +x .claude/skills/*/scripts/*.sh

# Test script directly
./claude/skills/skill-name/scripts/deploy.sh
```

### High Token Usage
```bash
# Profile skill token usage
# Move content from SKILL.md to REFERENCE.md
# Ensure scripts return minimal output
```

## Contributing

When creating new skills:

1. Follow the established patterns
2. Optimize for token efficiency
3. Test with Claude Code and Goose
4. Document thoroughly
5. Include verification scripts
6. Add to this README

## Resources

- [AAIF Standards](https://aaif.io/)
- [Claude Code Skills Docs](https://code.claude.com/docs/skills)
- [Goose Documentation](https://block.github.io/goose/)
- [MCP Code Execution Pattern](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Hackathon III Docs](../docs/)

## License

MIT License - See repository root for details.

## Maintainers

Hackathon III Team - 2025
