---
name: mcp-code-execution
description: Implement MCP with code execution pattern for efficient token usage
version: 1.0.0
author: Hackathon Team
tags: [mcp, model-context-protocol, code-execution, efficiency]
---

# MCP Code Execution Pattern

## When to Use
- Building skills that use MCP servers
- Need to minimize context window usage
- Handling large data from MCP tools
- Want 80-98% token reduction

## What This Skill Does
Implements the MCP Code Execution pattern from Anthropic's engineering blog. Instead of loading MCP tools directly into agent context, wraps them in scripts that execute and return only minimal results.

## The Pattern

**Before (Inefficient)**: Direct MCP tool calls
```
Context: 50k tokens (tool definitions) + 50k tokens (data) = 100k tokens
```

**After (Efficient)**: Code execution wrapper
```
Context: ~100 tokens (skill) + ~10 tokens (result) = 110 tokens
```

## Instructions

1. **Create MCP Wrapper Script**
   ```bash
   python scripts/create_mcp_wrapper.py --server kubernetes --output k8s_ops.py
   ```

2. **Wrap in Skill**
   ```bash
   python scripts/create_skill_from_mcp.py --script k8s_ops.py --name k8s-ops
   ```

3. **Test Execution**
   ```bash
   python scripts/test_mcp_skill.py k8s-ops
   ```

## Example: Kubernetes MCP Wrapper

**Direct MCP (Bad)**:
```python
# Loads 15k tokens of tool definitions
# Returns 10k tokens of pod JSON
TOOL_CALL: kubernetes.getPods(namespace="default")
```

**Code Execution (Good)**:
```python
# Script executes, filters data client-side
import subprocess
pods = subprocess.run(["kubectl", "get", "pods", "-o", "json"])
running = [p for p in pods if p.status == "Running"]
print(f"✓ {len(running)} pods running")  # Only this enters context
```

## Validation Checklist
- [ ] MCP server accessible via script
- [ ] Data filtering happens in script
- [ ] Only final result enters context
- [ ] Token usage reduced by 80%+

See [REFERENCE.md](./REFERENCE.md) for detailed implementation guide and examples.
