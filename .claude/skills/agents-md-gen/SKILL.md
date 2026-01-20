---
name: agents-md-gen
description: Generate AGENTS.md files for repositories to help AI agents understand codebase structure
version: 1.0.0
author: Hackathon Team
tags: [documentation, agents, automation]
---

# AGENTS.md Generator

## When to Use
- Starting a new repository that AI agents will work with
- User asks to "create AGENTS.md" or "document repo for agents"
- Setting up agentic development workflows
- Need to onboard AI agents to existing codebase

## What This Skill Does
Generates comprehensive AGENTS.md files that describe repository structure, conventions, and guidelines so AI coding agents (Claude Code, Goose, Codex) can understand how to work with the codebase effectively.

## Instructions

1. **Analyze Repository Structure**
   ```bash
   python scripts/generate_agents_md.py --analyze
   ```

2. **Generate AGENTS.md**
   ```bash
   python scripts/generate_agents_md.py --output AGENTS.md
   ```

3. **Verify Output**
   - Check that AGENTS.md exists in repository root
   - Verify all sections are populated with relevant information
   - Confirm file paths and structure are accurate

## Validation Checklist
- [ ] AGENTS.md file created in repository root
- [ ] Repository structure documented
- [ ] Tech stack clearly identified
- [ ] Development conventions specified
- [ ] Getting started instructions included
- [ ] File passes markdown linting

## Expected Output
File with sections:
- Repository Overview
- Directory Structure
- Technology Stack
- Development Conventions
- Getting Started
- Common Tasks
- Architecture Decisions

See [REFERENCE.md](./REFERENCE.md) for AGENTS.md format specification and examples.
